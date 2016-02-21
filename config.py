import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SERVER_NAME = '0.0.0.0:80'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'zriv.db')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'APP_PRODUCTION_DATABASE_URI'
    )


config = {
    'production': ProductionConfig,
    'development': Config,
    'default': Config,
}
