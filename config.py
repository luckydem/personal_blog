class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'supersecretkey'
    FIRESTORE_PROJECT = 'my-personal-blog-cs50'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    SECRET_KEY = 'evenmoresupersecretkey'
    FIRESTORE_PROJECT = 'prod-firestore-project'

class TestingConfig(Config):
    TESTING = True
    FIRESTORE_PROJECT = 'test-firestore-project'