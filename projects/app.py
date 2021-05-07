"""Main app"""

from pathlib import Path
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from projects.model import DB
from projects.cfg import config
from projects.api import api
from flask_script import Manager


def create_app(test_db=None):
    """creates a new app instance"""
    new_app = Flask(__name__)
    new_app.config["SQLALCHEMY_DATABASE_URI"] = config.database.url(
        default=test_db or "sqlite:///test.db")
    new_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    new_app.config["ERROR_404_HELP"] = False
    DB.init_app(new_app)
    api.init_app(new_app)
    Migrate(new_app, DB, directory=Path(__file__).parent / "migrations")
    new_app.wsgi_app = ProxyFix(
        new_app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1
    )  # remove after flask-restx > 0.2.0 is released
    CORS(new_app)
    return new_app
