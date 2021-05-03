"""Error handlers."""
import traceback

from flask import Blueprint, current_app, jsonify, make_response, request

errors = Blueprint('errors', __name__)


class FailedRequest(Exception):
    """General failed error."""

    status_code = 400
    title = 'There is an error in the request'
    payload = 'There is an error in the request. Please check request payload.'

    def __init__(self, status_code=400, title='Error', payload=''):
        Exception.__init__(self)
        self.status_code = status_code
        self.title = title
        self.payload = payload


def build_error(code: int = 500, title: str = 'Request Error', payload: str = ''):
    """
    Build error message.

    :param code:
    :param title:
    :param payload:
    :return:
    """
    e_obj = {
        'errors': {
            'status': code,
            'source': {'pointer': request.full_path},
            'title': title,
            'detail': payload
        }
    }

    return make_response(jsonify(e_obj), code)


@errors.app_errorhandler(404)
def not_found(error):
    """
    Code 404 handler.

    :param error:
    :return:
    """
    current_app.logger.warning(error)
    return build_error(
        code=404, title='Resource not found.',
        payload='The specified resource is not found on the server.')


@errors.app_errorhandler(405)
def nto_allowed(error):
    """
    Code 405 handler.

    :param error:
    :return:
    """
    current_app.logger.warning(error)
    return build_error(
        code=405, title='Resource not found.',
        payload='The specified resource is not found on the server.')


@errors.app_errorhandler(500)
def handler500(error):
    """
    Code 500 handler.

    :param error:
    :return:
    """
    current_app.logger.error(error)
    return build_error(
        code=500, title='Server error.',
        payload='Something went wrong while processing request')


@errors.app_errorhandler(Exception)
def exception_encountered(error):
    """
    General exception handling.

    :param error:
    :return:
    """
    current_app.logger.fatal(repr(error))
    current_app.logger.error(traceback.format_exc())
    return build_error(
        code=500, title='Server error.',
        payload='Something went wrong while processing request')


@errors.app_errorhandler(FailedRequest)
def general_error(error):
    """
    Main error handler feature.

    :param error:
    :return:
    """
    current_app.logger.warning(error.title)
    return build_error(
        code=error.status_code, title=error.title,
        payload=error.payload)
