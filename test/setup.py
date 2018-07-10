import os
import unittest

from app import APP
from lib import db_session
from lib.database import Model

if os.environ.get('CI') is None:
    os.environ['ENV'] = 'test'
else:
    os.environ['ENV'] = 'circleci'

TEST_APP = APP.test_client()


class BaseDatabaseTest(unittest.TestCase):
    def tearDown(self):
        for table in reversed(Model.metadata.tables.keys()):
            db_session.execute('truncate %s cascade' % table)
        db_session.commit()
