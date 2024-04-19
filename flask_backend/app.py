'''
Application run file
'''
import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, jwt_manager
from models import User, Message
from api.auth import auth
from api.chat import chat_bp

load_dotenv()

app = Flask(__name__)
DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME = os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'), \
                                            os.getenv('DB_HOST'), os.getenv('DB_NAME')
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
db.init_app(app)
jwt_manager.init_app(app)
app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')

@app.route('/')
def index():
    '''
    :returns: Main template used for the homepage
    '''
    return render_template('index.html')

@app.route('/chat')
@jwt_required()
def chat():
    '''
    :returns: Main template used for the chat interface
    '''
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    messages = Message.query.filter_by(user_id=user.id).order_by(Message.timestamp).all()
    return render_template('chat.html', messages=messages)
    
# Run with python app.py
if __name__ == '__main__':
    app.run(debug=True)
