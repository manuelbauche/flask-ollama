'''
File to define and create the app settings
'''
import os
from dotenv import load_dotenv
from flask import Flask
from extensions import db, jwt_manager
from api.auth import auth
from api.chat import chat_bp
from api.views import api

def create_app():
    '''
    This function defines the app settings and returns the created flask app. Change settings if needed
    :returns: Flask App
    '''
    load_dotenv()

    app = Flask(__name__)
    DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME = os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'), \
                                                os.getenv('DB_HOST'), os.getenv('DB_NAME')
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    db.init_app(app)
    jwt_manager.init_app(app)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(api, url_prefix='/api')

    return app
