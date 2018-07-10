import unittest
import json

from app import APP
from models import Log


class LogTest(unittest.TestCase):
    def test_ingest(self):
        log_file_path = 'test/fixtures/example-1.log'
        log = Log(source='test_source', path=log_file_path)
        log.save()
        assert log.ingested == False
        log.ingest()
        assert log.ingested == True
        assert len(log.log_events) == 5
