class Config(object):
    DEBUG = False
    TESTING = False
    MONGO_URI = 'mongodb://localhost/'
    DB = "flaskr"
    COLLECTION = "flaskr"


class ProductionConfig(Config):
    DATABASE_URI = 'mongodb://localhost/'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DB = "test_db_flaskr"
    COLLECTION = "test_collection_flaskr"
