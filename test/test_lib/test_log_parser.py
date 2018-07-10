from __future__ import absolute_import
import unittest

from lib.log_parser import LogParser


class LogParserTest(unittest.TestCase):
    def test_parse(self):
        log_file_path = 'test/fixtures/example-1.log'
        log_parser = LogParser(log_file_path)
        parsed = log_parser.parse()
        assert len(parsed) == 5
