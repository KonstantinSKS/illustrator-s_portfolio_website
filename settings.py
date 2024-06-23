import os

# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "db.sqlite3")}'

#     SQLALCHEMY_DATABASE_URI = 'postgresql://{username}:{password}@localhost:5432/{dbname}'


class Config(object):
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.environ.get('DB_ENGINE', default='postgresql'),
        os.environ.get('POSTGRES_USER', default='postgres'),
        os.environ.get('POSTGRES_PASSWORD', default='qwerty'),
        os.environ.get('DB_HOST', default='localhost'),
        os.environ.get('DB_PORT', default=5432),
        os.environ.get('POSTGRES_DB', default='flaskdb')
    )
#     SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = 'media/'
    USER_IMAGES = 'user_images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
