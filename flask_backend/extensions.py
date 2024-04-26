'''
Setting up database and other necessary configuration to get the application running
'''
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt_manager = JWTManager()

def to_dict(self):
    '''
    Returns a dictionary representation of a database model list query
    :param: Database model row
    :returns: dictionary of model
    '''
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
