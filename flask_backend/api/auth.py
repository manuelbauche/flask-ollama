'''
Authentication logic
'''

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User
from extensions import db, to_dict
from sqlalchemy import exc

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    :data: {username: str, password: str}
    :return: Success or error message and commit new user to db.
    '''
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({'message': 'Username registered successfully'}), 200
    except exc.IntegrityError:
        return jsonify({'message': 'Username already exists'}), 400 # Rollback on error default is true

@auth.route('/login', methods=['POST'])
def login():
    '''
    :data: {username: str, password: str}
    :return: Success or error message and access token.
    '''
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Incorrect login data'}), 401
    token = create_access_token(identity=user.id)
    return jsonify({'token': token, 'user': to_dict(user)}), 200
