from __future__ import absolute_import

import unittest
import urllib
import json

from app import APP, AuthToken
from lib.aws import get_timestamp
from test.requests.request_setup import RequestHeaders


class LogUploadWithoutAuthTest(unittest.TestCase):
    def setUp(self):
        with APP.app_context():
            self.app = APP.test_client()
            self.request_headers = RequestHeaders({'Authorization': 'None'})

    def test_upload_with_cell_plate_number_with_no_api_token(self):
        response = self.app.post(
            'http://localhost:8080/logs',
            data=None,
            headers={'Content-Type': 'application/octet-stream'})
        assert response.status_code == 401


class LogUploadTest(unittest.TestCase):
    def setUp(self):
        with APP.app_context():
            self.app = APP.test_client()
            self.request_headers = RequestHeaders(
                {'Authorization': 'Bearer ' + AuthToken.generate('testsource')})
            self.log_file = 'test/fixtures/example-1.log'
            self.log_data = open(self.log_file, 'rb').read()

    def test_upload_log(self):
        response = self.app.post(
                'http://localhost:8080/logs',
            data=self.log_data,
            headers=self.request_headers.append({'Content-Type': 'application/octet-stream'}))

        response_data = json.loads(response.get_data())
        assert response_data['ingested'] == False
        assert response.status_code == 201
