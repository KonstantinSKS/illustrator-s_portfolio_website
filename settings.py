import os

# basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "db.sqlite3")}'
    SQLALCHEMY_DATABASE_URI = os.getenv(
         'DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = 'postgres://postgres:123@localhost/db'
    UPLOAD_FOLDER = 'media/'
    USER_IMAGES = 'user_images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
