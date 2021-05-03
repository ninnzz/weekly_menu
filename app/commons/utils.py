"""Util functions."""
from cerberus import Validator
from app.commons.errors import FailedRequest


def validate_input(data: dict, schema: dict) -> dict:
    """
    Validates input.

    Returns the validated data after

    :param data:
    :param schema:
    :return:
    """
    request_validator = Validator()

    if not request_validator.validate(data, schema):
        raise FailedRequest(401, 'Problem with request parameters', request_validator.errors)

    return data
