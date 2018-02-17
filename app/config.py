import os

class Config(object):

    """
    Common configurations
    """

    DEBUG = False

class Development(Config):
    """
    Development Configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class Testing(Config):
    """
    Testing Configurations
    """

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://marlone911:@localhost/test_bev'

class Production(Config):
    """
    Production Configurations
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
