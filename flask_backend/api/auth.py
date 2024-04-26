'''
Authentication logic
'''

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from sqlalchemy import exc
from models import User
from extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    Register a new user.
    :data: {username: str, password: str}
    :return: Success or error message and commit new user to db.
    :raises IntegrityError: If the username already exists
    '''
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No user data inputed'}), 400
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid input data'}), 400
    
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
    Logins a user and gives them a JWT token to access protected features.
    :data: {username: str, password: str}
    :return: Success or error message and access token.
    '''
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No user data inputed'}), 400
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid input data'}), 400
    
    user = User.query.filter(User.username == data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Incorrect login data'}), 401
    token = create_access_token(identity=user.id)
    return jsonify({'token': token}), 200

@auth.route('/password', methods=['PATCH'])
@jwt_required()
def change_password():
    '''
    Allows authenticated user to change their password.
    :data: {"current_password": str, "new_password": str}
    :return: Success or error message if current password is incorrect.
    '''
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No user data inputed'}), 400
    if 'current_password' not in data or 'new_password' not in data:
        return jsonify({'message': 'Invalid input data'}), 400
    
    if not user or not check_password_hash(user.password, data['current_password']):
        return jsonify({'message': 'Incorrect current password'}), 401

    hashed_password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
    user.password = hashed_password
    try:
        db.session.commit()
    except exc.IntegrityError:
        return jsonify({'message': 'Could not change password'}), 400

    return jsonify({'message': 'Password changed successfully'}), 200