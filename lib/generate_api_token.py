import sys

from app import APP, AuthToken


def generate_api_token(client):
    with APP.app_context():
        return AuthToken.generate(client)


if __name__ == '__main__':
    name = sys.argv[1] if sys.argv[1] else sys.argv[0]
    if not name:
        raise Exception('Must provide a name for the client.')
    api_token = generate_api_token(name)

    print ''
    print ''
    print 'Logbox API access for ' + name
    print ''
    print ''
    print 'API token:'
    print api_token
    print ''
    print 'Use API token in \'Authorization\' http header like this:'
    print 'Bearer ' + api_token
    print ''
    print 'If the Logbox SECRET_KEY ever changes, a new API token will need to be generated.'
    print ''
