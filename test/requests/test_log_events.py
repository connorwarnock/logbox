from __future__ import absolute_import

import unittest
import urllib
import json

from test.setup import BaseDatabaseTest
from app import APP, AuthToken
from lib.aws import get_timestamp
from test.requests.request_setup import RequestHeaders
from models import Log


class LogEventsTest(BaseDatabaseTest):
    def setUp(self):
        with APP.app_context():
            self.app = APP.test_client()
            self.request_headers = RequestHeaders(
                {'Authorization': 'Bearer ' + AuthToken.generate('testsource')})

    def create_log_events(self, log_file_path):
        log = Log(source='example', path=log_file_path)
        log.save()
        log.ingest()

    def test_fetch_all(self):
        self.create_log_events('test/fixtures/example-50.log')
        response = self.app.get(
            'http://localhost:8080/log-events',
            headers=self.request_headers.headers)

        assert response.status_code == 200
        response_data = json.loads(response.get_data())
        assert len(response_data) == 10

    def test_fetch_with_limit(self):
        self.create_log_events('test/fixtures/example-50.log')
        response = self.app.get(
            'http://localhost:8080/log-events?limit=20',
            headers=self.request_headers.headers)

        assert response.status_code == 200
        response_data = json.loads(response.get_data())
        assert len(response_data) == 20

    def test_fetch_by_generation(self):
        self.create_log_events('test/fixtures/example-generations.log')
        response = self.app.get(
            'http://localhost:8080/log-events?drone_generation=16',
            headers=self.request_headers.headers)

        assert response.status_code == 200
        response_data = json.loads(response.get_data())
        assert len(response_data) == 7

    def test_fetch_from_date_to_date(self):
        self.create_log_events('test/fixtures/example-dates.log')
        response = self.app.get(
            'http://localhost:8080/log-events?\
            from_time=2018-07-01T19:12:42.854089+00:00&to_time=2018-07-03T19:12:42.854089+00:00',
            headers=self.request_headers.headers)

        assert response.status_code == 200
        response_data = json.loads(response.get_data())
        assert len(response_data) == 3

    def test_fetch_by_max_duration(self):
        self.create_log_events('test/fixtures/example-duration.log')
        duration = 15 * 60
        response = self.app.get(
            'http://localhost:8080/log-events?max_duration=' + str(duration),
            headers=self.request_headers.headers)

        assert response.status_code == 200
        response_data = json.loads(response.get_data())
        assert len(response_data) == 2

    def test_fetch_by_max_duration_with_error(self):
        self.create_log_events('test/fixtures/example-duration.log')
        response = self.app.get(
            'http://localhost:8080/log-events?max_duration=20seconds',
            headers=self.request_headers.headers)

        assert response.status_code == 400
        response_data = json.loads(response.get_data())
        assert response_data['errors'] == ['Max duration must be a integer, in seconds']

    def test_fetch_by_bounded_rectangle(self):
        self.create_log_events('test/fixtures/example-bounded.log')
        params = {
            'top_left_lat': 33.985453,
            'top_left_lon': 118.472729,
            'bottom_right_lat': 33.985433,
            'bottom_right_lon': 118.472749
        }
        encoded_params = urllib.urlencode(params, True)
        response = self.app.get(
            'http://localhost:8080/log-events?' + encoded_params,
            headers=self.request_headers.headers)

        assert response.status_code == 200
        response_data = json.loads(response.get_data())
        assert len(response_data) == 2
