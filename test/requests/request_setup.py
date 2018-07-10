class RequestHeaders(object):
    def __init__(self, headers):
        self.headers = headers

    def append(self, headers):
        self.headers = dict(self.headers.items() + headers.items())
        return self.headers
