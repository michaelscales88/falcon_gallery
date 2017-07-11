from os import urandom, path, environ


class Config(object):
    WTF_CSRF_ENABLED = True
    SECRET_KEY = urandom(24)     # Generate a random session key

    BASEDIR = path.abspath(path.dirname(__file__))
    PACKAGEDIR = path.dirname(BASEDIR)
    PACKAGE_NAME = path.basename(PACKAGEDIR)

    GALLERY_ROOT_DIR = path.join(PACKAGEDIR, 'instance', 'gallery')
    UPLOAD_DIR = path.join(PACKAGEDIR, 'instance', 'uploads')
    ALLOWED_EXTENSIONS = (
        'jpg',
        'jpeg',
        'png',
        'gif',
    )

    # Model database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASEDIR, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = path.join(BASEDIR, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Turn this off to reduce overhead

    # indexing service
    WHOOSH_BASE = path.join(BASEDIR, 'tmp/whoosh')
    ENABLE_SEARCH = True

    # email server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')

    # administrator list
    ADMINS = ['your-gmail-username@gmail.com']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    WIPE_SESSION = True
    MAX_RECORDS = 3000
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # Turn this off to reduce overhead
    CLIENTS = ['Torie', 'Sean', 'Susan', 'Debbie']


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + ':memory:'
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
