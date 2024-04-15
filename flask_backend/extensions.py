'''
Setting up database and other necessary configuration to get the application running
'''
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_jwt_extended import JWTManager
jwt_manager = JWTManager()
