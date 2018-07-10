from __future__ import absolute_import

import unittest

from app import APP


class HealthTest(unittest.TestCase):
    def setUp(self):
        self.app = APP.test_client()

    def test_health_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/health')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_health_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/health')

        # assert the response data
        self.assertEqual(result.data, "OK")
