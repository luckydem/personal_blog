from flask import Flask
# import logging
from config import config
from .routes import bp as routes_bp



def create_app(config_name):    
    
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    # logging.basicConfig(level=app.config['LOGGING_LEVEL'])
    
    app.register_blueprint(routes_bp)
    
    return app
    