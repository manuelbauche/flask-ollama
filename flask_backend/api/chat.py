'''
Chat endpoint
'''
from flask import Blueprint, request, jsonify, stream_with_context, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from models import User, Message
from extensions import db
from api.ai_process import get_response

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['GET', 'POST'])
@jwt_required()
def reply():
    '''
    ollama response module
    :returns: ollama generator of strings
    :raises IntegrityError: If there are any issues commiting the changes with the user message or bot reply
    '''
    # Perform user identity
    current_user_id = get_jwt_identity() # Get the current user ID
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Request user message and commit to db
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No user data inputed'}), 400
    if 'message' not in data:
        return jsonify({'message': 'Invalid input data'}), 400

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
        for val in get_response(msg):
            response_parts.append(val)
            yield val
        bot_message = Message(user_id=user.id, text=''.join(response_parts), is_user=False)
        db.session.add(bot_message)
        try:
            db.session.commit()
        except Exception as e:
            return jsonify({'message': f'Error occurred while getting a reply: {str(e)}'}), 500

    return Response(stream_with_context(generate()), content_type='application/json')
