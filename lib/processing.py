# pylint: disable=bare-except
import logging
import multiprocessing
import os
import random
from multiprocessing.pool import ThreadPool
from threading import Timer

multiprocessing.log_to_stderr(logging.INFO)


def backoff_jitter():
    return random.randint(0, 1000) / 1000.0


def get_backoff_delay_seconds(retry_count):
    return (2 ** retry_count) + backoff_jitter()


class Background(object):
    def __init__(self, sentry=None):
        self.sentry = sentry
        if os.getenv('THREAD_POOL_SIZE'):
            self.pool = ThreadPool(processes=int(os.getenv('THREAD_POOL_SIZE')))
        else:
            self.pool = ThreadPool(processes=10)

    def setup_sentry(self, f):
        def wrapper(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except:
                self.sentry.captureException()

        if self.sentry:
            return wrapper
        else:
            return f

    def run(self, target, args=()):
        if os.environ.get('ENV') in ['test', 'circleci']:
            return target(*args)
        self.pool.apply_async(target, args)

    def run_delayed(self, delay, target, args=()):
        Timer(delay, self.setup_sentry(target), args).start()
