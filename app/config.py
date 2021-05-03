"""Main config file."""
import os


class FlaskConfig:
    """Flask config."""
    APP_NAME = 'Weekly menu'

    # Flask basic config
    ALLOWED_HEADERS = [
        'Access-Token', 'Content-Type', 'referrer',
        'Authorization', 'Cache-Control', 'X-Requested-With'
    ]

    ALLOWED_ORIGINS = '*'
    ALLOWED_METHODS = [
        'GET', 'HEAD', 'POST', 'OPTIONS',
        'PUT', 'PATCH', 'DELETE'
    ]

    LOGGING = {
        'LEVEL': 'DEBUG',
        'FORMAT': '[%(asctime)s] %(levelname)s '
                  '%(name)s %(funcName)s():%(lineno)d\t%(message)s',
        'CONTEXT_SETTINGS': {
            'LEVEL': "DEBUG",
            'FORMAT': '[%(asctime)s] %(levelname)s '
                      '%(name)s %(funcName)s():%(lineno)d\t%(message)s',
            'FILE': '/opt/local/tmp/{}_{}.log',
            'SUFFIX': '%Y%m%d'
        }
    }

    LOG_PATH = '/tmp/app.log'
    FATAL_ERROR_LOG_PATH = '/tmp/app-error.log'

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
    #     os.environ.get('DB_USER', 'root'),
    #     os.environ.get('DB_PASS', ''),
    #     os.environ.get('DB_HOST', '127.0.0.1'),
    #     os.environ.get('DB_PORT', '3306'),
    #     os.environ.get('DB_NAME', 'weekly_menu'))

    DB_DRIVER = os.environ.get('DB_DRIVER', 'mysql')
    DB_NAME = os.environ.get('DB_NAME', 'weekly_menu')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASS = os.environ.get('DB_PASS', 'useruser')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
