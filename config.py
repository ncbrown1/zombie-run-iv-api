import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # SERVER_NAME = '0.0.0.0:80'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'zriv.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'zriv-test.db')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL'
    )


config = {
    'production': ProductionConfig,
    'testing': TestingConfig,
    'development': Config,
    'default': Config,
}
