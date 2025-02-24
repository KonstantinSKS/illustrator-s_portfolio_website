from flask import Flask, g
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

from settings import Config

cache = Cache()

app = Flask(__name__)
app.config.from_object(Config)
cache.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = LoginManager(app)


@app.before_request
def before_request():
    g.user = current_user


@app.context_processor
def inject_user():
    return dict(user=g.user)

from . import admin_routes, models, admin, cli_commands, error_handlers, routes  # noqa
