'''
Chat endpoint
'''
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from ai_process import chat

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['GET', 'POST'])
@jwt_required()
def reply():
    '''
    ollama response module
    :returns: ollama generator of strings
    '''
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    msg = data['message']
    def generate():
        for val in chat(msg):
            yield val
    return generate(), {'Content-Type': 'application/json'}