"""Creates logger for app."""
import logging
from logging.handlers import RotatingFileHandler


def create_logger(app):
    """
    Creates logger from app.

    :param app:
    :return:
    """
    logging_config = app.config['LOGGING']

    logging.addLevelName(
        logging.WARNING,
        "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(
        logging.ERROR,
        "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

    _level = logging.FATAL

    if 'LEVEL' in logging_config:
        _level = getattr(logging, logging_config['LEVEL'])

    app.logger.setLevel(_level)

    _format = '[%(asctime)s] %(levelname)s %(name)s %(funcName)s():%(lineno)d\t%(message)s'
    if 'FORMAT' in logging_config:
        _format = logging_config['FORMAT']

    _formatter = logging.Formatter(_format)

    _file_logger = RotatingFileHandler(app.config['LOG_PATH'],
                                       maxBytes=10000,
                                       backupCount=1)

    _file_logger.setLevel(_level)
    _file_logger.setFormatter(_formatter)

    fatal_handler = logging.FileHandler(app.config['FATAL_ERROR_LOG_PATH'], mode='w')
    fatal_handler.setFormatter(_formatter)
    fatal_handler.setLevel(logging.FATAL)
    app.logger.addHandler(fatal_handler)

    app.logger.addHandler(_file_logger)
