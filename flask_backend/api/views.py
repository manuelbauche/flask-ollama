'''
Definition of all API endpoints except the AI. 
'''
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from models import User, Message
from extensions import db, to_dict

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_all_users():
    '''
    Returns all users in the database
    '''
    users = User.query.all()

    return jsonify([to_dict(user) for user in users]), 200

@api.route('/messages', methods=['GET'])
@jwt_required()
def get_messages():
    '''
    Gets all messages for an authenticated user
    :returns: All messages
    '''
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    messages = Message.query.filter_by(user_id=user.id).order_by(Message.timestamp).all()
    return jsonify([to_dict(message) for message in messages]), 200


@api.route('/clear', methods=['POST'])
@jwt_required()
def clear():
    '''
    Clear user messages in the chat module
    :returns: Success message
    '''
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    Message.query.filter_by(user_id=user.id).delete()
    try:
        db.session.commit()
    except exc.IntegrityError:
        return jsonify({'message': 'Message could not be deleted.'}), 400
    return jsonify({'message': 'Conversation cleared'}), 200