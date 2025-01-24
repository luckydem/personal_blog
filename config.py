import logging

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'supersecretkey'
    FIRESTORE_PROJECT = 'my-personal-blog-cs50'
    POSTS = 'posts'
    LOGGING_LEVEL = logging.DEBUG

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    POSTS = 'secret_posts' # 'dev_posts'
    LOGGING_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    SECRET_KEY = 'evenmoresupersecretkey'
    FIRESTORE_PROJECT = 'my-personal-blog-cs50'
    POSTS = 'posts'
    LOGGING_LEVEL = logging.INFO

class TestingConfig(Config):
    TESTING = True
    FIRESTORE_PROJECT = 'my-personal-blog-cs50'
    
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig    
}