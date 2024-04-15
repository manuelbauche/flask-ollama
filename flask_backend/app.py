'''
Application run file
'''
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
from api.ai_process import chat
from flask_jwt_extended import JWTManager
from api.auth import auth
from setup import db
from models import User

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = app.secret_key  # change this
db.init_app(app)
jwt_manager = JWTManager(app)
app.register_blueprint(auth, url_prefix='/api')

@app.route('/')
def index():
    '''
    :returns: Main template used for the homepage
    '''
    return render_template('chat.html')


@app.route('/chat', methods=['GET', 'POST'])
def reply():
    '''
    ollama response module
    :returns: ollama generator of strings
    '''
    data = request.get_json()
    msg = data['message']
    def generate():
        for val in chat(msg):
            yield val
    return generate(), {'Content-Type': 'application/json'}

    
# Run with python app.py
if __name__ == '__main__':
    app.run(debug=True)
