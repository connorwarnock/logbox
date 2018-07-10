import os

from lib import celery
from lib.aws import s3_upload, get_timestamp, without_s3_metadata


@celery.task()
def upload_log(file_data, path):
    if os.environ['ENV'] in ['test', 'circleci', 'development']:
        file_name = path.split('/')[-1]
        with open('/tmp/' + file_name, 'wb') as f:
            f.write(file_data)
            f.close()
    else:
        s3_upload(file_data, path)
