class Config(object):

    """
    Common configurations
    """

class Development(Config):
    """
    Development Configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class Testing(Config):
    """
    Testing Configurations
    """

    DEBUG = True
    TESTING = True

class Production(Config):
    """
    Production Configurations
    """

    DEBUG = False


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
