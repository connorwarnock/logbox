import hashlib
import os.path
import time

import boto
from werkzeug.utils import secure_filename

from config import Config
from lib.testing import time_stubbed


def init_s3_connection():
    conn = boto.connect_s3(Config.S3_KEY, Config.S3_SECRET)
    bucket = conn.get_bucket(Config.S3_BUCKET, validate=False)
    return bucket


def md5(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest()


@time_stubbed
def get_timestamp():
    return str(int(time.time() * 1000))


def version_timestamp(s3_prefix):
    return s3_prefix.name[:-1].split('/')[-1]


def is_version_dir(s3_prefix):
    return version_timestamp(s3_prefix).isdigit()


def without_s3_metadata(s3_filename):
    plain, extension = os.path.splitext(s3_filename)
    return plain.split('-')[0] + extension


def file_name_matches(s3_key, file_name):
    return without_s3_metadata(s3_key.name) == file_name


def destination_path(timestamp, source_name):
    upload_dir = Config.S3_UPLOAD_DIRECTORY
    directory = timestamp.strftime('%Y-%m-%d')
    filename_base = '-'.join([source_name, timestamp.isoformat()])
    filename = '.'.join([filename_base, 'log'])
    path_list = [upload_dir, directory, filename]
    return '/'.join(path_list)


def s3_upload(source_file, path):
    acl = 'public-read'
    bucket = init_s3_connection()

    md5_string = md5(source_file)
    plain_path, file_extension = os.path.splitext(path)
    clean_plain_path = plain_path.replace('.', '').replace('-', '_')
    final_path = clean_plain_path + '-' + md5_string + '-' + get_timestamp() + file_extension

    key = bucket.new_key(final_path)
    key.set_contents_from_string(source_file)
    key.set_acl(acl)
    s3_path = key.name

    return s3_path, md5_string


def list_path(*path):
    upload_dir = Config.S3_UPLOAD_DIRECTORY
    prefix_path = '/'.join([upload_dir] + list(path))
    bucket = init_s3_connection()
    return [key.name for key in bucket.list(prefix=prefix_path)]
