from flask import Flask
from .routes import bp as routes_bp
# from extensions.my_firestore import init_app as init_firestore

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    # init_firestore(app)
    
    app.register_blueprint(routes_bp)
    
    return app
    