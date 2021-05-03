"""Flask server."""

from app.commons.database import db, create_tables
from app.commons.errors import errors
from app.commons.logger import create_logger
from app.config import FlaskConfig
from app.router import router
from flask import Flask


def create_app(config=None):
    """App initialization."""
    # Declare app
    app = Flask(FlaskConfig.APP_NAME)

    # Load config
    app.config.from_object(FlaskConfig)
    # Loads config file if there are any config included
    if config:
        app.config.from_object(config)

    # Handle CORS properly
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Origin',
            app.config['ALLOWED_ORIGINS'])
        response.headers.add(
            'Access-Control-Allow-Headers',
            ','.join(app.config['ALLOWED_HEADERS']))
        response.headers.add(
            'Access-Control-Allow-Methods',
            ','.join(app.config['ALLOWED_METHODS']))
        return response
    app.after_request(after_request)

    # Register the available routes
    app.register_blueprint(router, url_prefix='/api')
    # Register error handlers
    app.register_blueprint(errors)

    # Init database
    @app.before_request
    def before_request():
        db.connect()

    @app.after_request
    def after_request(response):
        db.close()
        return response

    # Create logger for app
    create_logger(app)
    create_tables()
    return app
