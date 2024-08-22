import os


class Config(object):
    """Application configuration."""

    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() in ['true', '1', 't']

    if DEBUG:
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                            default='sqlite:///db.sqlite3')
    else:
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            os.environ.get('DB_ENGINE', default='postgresql'),
            os.environ.get('POSTGRES_USER', default='postgres'),
            os.environ.get('POSTGRES_PASSWORD', default='qwerty'),
            os.environ.get('DB_HOST', default='localhost'),
            os.environ.get('DB_PORT', default=5432),
            os.environ.get('POSTGRES_DB', default='flaskdb')
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = 'media/'
    USER_IMAGES = 'user_images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
