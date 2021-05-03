"""Response class."""
# Import global context
from functools import wraps

from flask import Response as rp
from flask import jsonify, make_response


def json_response(func):
    """
    Formats the json response.

    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = Response()
        # You can set custom headers here

        return func(res=response, *args, **kwargs)

    return wrapper


class Response:
    """Response class."""

    def __init__(self):
        self.headers = {}

    def set_header(self, key, value):
        """
        Set headers.

        :param key:
        :param value:
        :return:
        """
        self.headers[key] = value

    def send(self, data, status: int = 200):
        """
        Send data.

        :param status:
        :param data:
        :return:
        """
        response = make_response(jsonify({'data': data}))

        # set this later in config
        response.mimetype = 'application/json'

        response.status = str(status)

        for key in self.headers:
            response.headers.add(key, self.headers[key])

        return response

    def stream(self, data, mimetype='application/octet-stream'):
        """
        Stream data.

        :param data:
        :param mimetype:
        :return:
        """
        response = rp(data)

        response.mimetype = mimetype
        response.status = '200'

        for key in self.headers:
            response.headers.add(key, self.headers[key])

        return response

    # @staticmethod
    # def redirect(url, params):
    #     response = make_response(
    #         redirect(url + '?' + utils.encode_params(params)))
    #
    #     return response
