import os

from dotenv import load_dotenv, find_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(find_dotenv())


class Config(object):
    S3_UPLOAD_DIRECTORY = 'upload_files'
    S3_BUCKET = os.environ.get('S3_BUCKET')
    S3_KEY = os.environ.get('S3_KEY')
    S3_SECRET = os.environ.get('S3_SECRET')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'


class Development(Config):
    DEBUG = True
    DATABASE_URL = "postgresql://postgres:password@db/logbox"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class Test(Config):
    DEBUG = True
    DATABASE_URL = "postgresql://postgres:password@db/logbox_test"
    S3_BUCKET = 'logbox-dev'


class Circleci(Test):
    DATABASE_URL = "postgresql://ubuntu:@localhost/circle_test"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class Staging(Config):
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class Production(Config):
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


def flask_env_config():
    klass_name = 'development' if os.environ.get('ENV') == None else os.environ.get('ENV')
    return "config.{0}".format(klass_name.capitalize())
