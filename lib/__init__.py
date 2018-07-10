import logging
import logging.config
import logging.handlers
import os

import loggly.handlers
from celery import Celery
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config
from lib.processing import Background


def log_handler():
    formatter = logging.Formatter(
        '{"loggerName":"%(name)s", "asciTime":"%(asctime)s", "pathName":"%(pathname)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}')
    handler.formatter = formatter
    logger = APP.logger
    logger.setLevel(logging.INFO)
    root_log = logging.getLogger('')
    root_log.setLevel(logging.INFO)
    gu_error_logger = logging.getLogger('gunicorn.error')
    gu_access_logger = logging.getLogger('gunicorn.access')
    gu_access_logger.addHandler(handler)


def make_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'],
                    include=['lib.upload_functions']
                    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    if os.environ.get('ENV') in ['circleci', 'test']:
        celery.conf.update(CELERY_ALWAYS_EAGER=True)

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


APP = Flask(__name__)
API = Api(APP)
APP.config.from_object(config.flask_env_config())
celery = make_celery(APP)
db = SQLAlchemy(APP)
engine = create_engine(APP.config['DATABASE_URL'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

if os.getenv('ENV') in ['production', 'staging']:
    log_handler()
    background = Background()
else:
    background = Background()
