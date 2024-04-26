'''
Definition of all API endpoints except the AI. 
'''
import logging
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Message
from extensions import db, to_dict

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_all_users():
    '''
    TEST FUNCTION ONLY
    Returns all users in the database
    '''
    users = User.query.all()
    return jsonify([to_dict(user) for user in users]), 200

@api.route('/allmessages', methods=['GET'])
def get_all_messages():
    '''
    TEST FUNCTION ONLY
    Returns all users in the database
    '''
    messages = Message.query.all()
    return jsonify([to_dict(message) for message in messages]), 200

@api.route('/messages', methods=['GET'])
@jwt_required()
def get_messages():
    '''
    Gets all messages for an authenticated user
    :returns: All messages
    '''
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    messages = Message.query.filter(Message.user_id == user.id).order_by(Message.timestamp).all()
    if not messages:
        return jsonify({'message': f'No messages found for {user.username}'}), 200
    return jsonify([to_dict(message) for message in messages]), 200


@api.route('/clear', methods=['DELETE'])
@jwt_required()
def clear():
    '''
    Clear user messages in the chat module
    :Returns: A dictionary containing the success message.
    :Raises Exception: If an error occurs while clearing the conversation.
    '''
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    num_messages_deleted = Message.query.filter(Message.user_id == user.id).delete()
    try:
        db.session.commit()
        logging.info("User %d cleared %d messages.", current_user_id, num_messages_deleted)
    except Exception as e:
        return jsonify({'message': f'Error occurred while clearing conversation: {str(e)}'}), 500
    return jsonify({'message': 'Conversation cleared'}), 200