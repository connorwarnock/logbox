import unittest

from app import APP, AuthToken


class AuthTokenTest(unittest.TestCase):
    def test_generate_auth_token(self):
        with APP.app_context():
            auth_token = AuthToken.generate('client')
            assert len(auth_token) == 148

    def test_verify_auth_token_succeeds(self):
        with APP.app_context():
            auth_token = AuthToken.generate('client')
            response = AuthToken.verify(auth_token)
            self.assertTrue(response)

    def test_verify_auth_token_fails(self):
        with APP.app_context():
            self.assertFalse(AuthToken.verify('thisisfake'))
