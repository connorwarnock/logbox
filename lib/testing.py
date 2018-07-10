import os

from freezegun import freeze_time


def time_stubbed(func):
    def wrapper(*args, **kwargs):
        if os.environ.get('ENV') in ['test', 'circleci']:
            if func.__name__ == 'get_timestamp':
                return '1326542401000'
            else:
                freezer = freeze_time("2012-01-14 12:00:01")
                freezer.start()
                func(*args, **kwargs)
                freezer.stop()

        return func(*args, **kwargs)

    return wrapper
