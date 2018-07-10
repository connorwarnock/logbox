import unittest
import json
import dateutil.parser

from app import APP
from models import LogEvent


class LogTest(unittest.TestCase):
    def test_set_duration(self):
        start_time = dateutil.parser.parse('2018-07-05T19:30:53.854089+00:00')
        end_time = dateutil.parser.parse('2018-07-05T19:30:59.854089+00:00')
        log_event = LogEvent(start_time=start_time, end_time=end_time)
        log_event.set_duration()
        assert log_event.duration_in_seconds == 6
