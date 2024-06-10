# import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_security import (Security,
#                             SQLAlchemyUserDatastore)
from flask_login import LoginManager

from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = LoginManager(app)

from . import models, admin, admin_views, cli_commands, error_handlers, views  # noqa

# db.create_all()
