'''
Chat endpoint
'''
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from models import User, Message
from extensions import db
from .ai_process import chat

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['GET', 'POST'])
@jwt_required()
def reply():
    '''
    ollama response module
    :returns: ollama generator of strings
    '''
    # Perform user identity
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Request user message and commit to db
    data = request.get_json()
    msg = data['message']
    user_message = Message(user_id=user.id, text=msg, is_user=True)
    db.session.add(user_message)
    try:
        db.session.commit()
    except exc.IntegrityError:
        return jsonify({'message': 'We are having issues sending your message.'}), 400
 
    # Request bot message and commit to db
    def generate():
        response_parts = []
        for val in chat(msg):
            response_parts.append(val)
            yield val
        bot_message = Message(user_id=user.id, text=''.join(response_parts), is_user=False)
        db.session.add(bot_message)
        try:
            db.session.commit()
        except exc.IntegrityError:
            return jsonify({'message': 'We are having issues comminicating with Ollama.'}), 400
    return generate(), {'Content-Type': 'application/json'}
