from __future__ import absolute_import

import datetime

import jwt
from flask import current_app as app


class AuthToken(object):
    @classmethod
    def verify(cls, auth_token):
        """
        Decodes the auth token
        :param token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    @classmethod
    def generate(cls, subject):
        """
        Generates the Auth Token
        :param subject: a string name for the machine or user
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365 * 100),
            'iat': datetime.datetime.utcnow(),
            'sub': subject
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
