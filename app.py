import os
import types
import datetime
from functools import wraps
from urlparse import urlsplit
import dateutil.parser

from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import or_, and_

from lib import APP, API, background, celery
from lib.aws import s3_upload, s3_hash_list, destination_path
from lib.upload_functions import upload_log
from models import Log, LogEvent, AuthToken
from schemas import log_schema, logs_schema, log_event_schema, log_events_schema


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls

    return wrapper


def missing_parameters(*params):
    for param in params:
        if isinstance(param, str) and request.args.get(param) is None or param is None:
            return True


def not_authenticated():
    message = {'message': 'Valid API token required'}
    response = jsonify(message)

    response.status_code = 401
    return response


def requires_authentication(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return not_authenticated()

        else:
            token = auth.split('Bearer ')[-1]
            if not AuthToken.verify(token):
                return not_authenticated()
            return f(*args, **kwargs)

    return wrapper


API.route = types.MethodType(api_route, API)


def extract_query_params(*params):
    if len(params) == 1:
        return request.args.get(params[0])
    else:
        return tuple(request.args.get(param) for param in params)


@APP.route('/health')
def health():
    try:
        # pylint: disable=no-member
        Log.query.limit(1).all()
        return 'OK', 200
    except Exception:
        return 'No database connection', 500


@API.route('/logs')
class Upload(Resource):
    @staticmethod
    @requires_authentication
    def post():
        if request.headers['Content-Type'] != 'application/octet-stream':
            return {'error': "Unsupported Media Type"}, 415

        now = datetime.datetime.now()

        auth = request.headers.get('Authorization', None)
        token = auth.split('Bearer ')[-1]
        source = AuthToken.verify(token)

        log = Log(source=source)
        log.save()

        path = destination_path(now, source)
        background.run(upload_log, (request.get_data(), path))
        response = log_schema.dump(log).data
        return response, 201


@API.route('/logs/<string:log_id>')
class FetchLog(Resource):
    @staticmethod
    @requires_authentication
    def get(log_id):
        return {}, 201


@API.route('/log-events')
class FetchLogEvents(Resource):
    @staticmethod
    @requires_authentication
    def get():
        limit = extract_query_params('limit') or 10
        filter_keys = ['drone_generation',
                       'from_time',
                       'to_time',
                       'max_duration',
                       'top_left_lat',
                       'top_left_lon',
                       'bottom_right_lat',
                       'bottom_right_lon']
        filter_values = extract_query_params(*filter_keys)
        filters = zip(filter_keys, filter_values)
        query = LogEvent.query
        errors = []
        for key, value in filters:
            if value is not None:
                if key == 'from_time':
                    try:
                        from_time = dateutil.parser.parse(value)
                    except ValueError as e:
                        errors.append('Improperly formatted from_time, use ISO 8601 format')
                        break
                    query = query.filter(or_(LogEvent.start_time >= from_time,
                                             and_(LogEvent.start_time <= from_time, LogEvent.end_time >= from_time)))

                elif key == 'to_time':
                    try:
                        to_time = dateutil.parser.parse(value)
                    except ValueError as e:
                        errors.append('Improperly formatted to_time, use ISO 8601 format')
                        break
                    query = query.filter(or_(LogEvent.end_time <= to_time,
                                             and_(LogEvent.end_time >= to_time, LogEvent.start_time <= to_time)))
                elif key == 'max_duration':
                    try:
                        max_duration = int(value)
                    except ValueError as e:
                        errors.append('Max duration must be a integer, in seconds')
                        break
                    query = query.filter(LogEvent.duration_in_seconds <= max_duration)
                elif key == 'top_left_lat':
                    try:
                        lat = float(value)
                    except ValueError as e:
                        errors.append('Top left lon should be provided as a float')
                        break
                    query = query.filter(LogEvent.lat <= lat)
                elif key == 'top_left_lon':
                    try:
                        lon = float(value)
                    except ValueError as e:
                        errors.append('Top left lon should be provided as a float')
                        break
                    query = query.filter(LogEvent.lon >= lon)
                elif key == 'bottom_right_lat':
                    try:
                        lat = float(value)
                    except ValueError as e:
                        errors.append('Bottom left lat should be provided as a float')
                        break
                    query = query.filter(LogEvent.lat >= lat)
                elif key == 'bottom_right_lon':
                    try:
                        lon = float(value)
                    except ValueError as e:
                        errors.append('Bottom left lon should be provided as a float')
                        break
                    query = query.filter(LogEvent.lon <= lon)
                else:
                    d = { key: value }
                    query = query.filter_by(**d)
        if len(errors) > 0:
            return { 'errors': errors }, 400
        else:
            result = query.limit(limit).all()
            json_response = log_events_schema.dump(result).data
            return json_response, 200


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080)
