'''
Application run file
'''
import os
from dotenv import load_dotenv
from flask import Flask, render_template
from extensions import db, jwt_manager
from api.auth import auth
from api.chat import chat_bp
from api.views import api

load_dotenv()

app = Flask(__name__)
DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME = os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'), \
                                            os.getenv('DB_HOST'), os.getenv('DB_NAME')
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
db.init_app(app)
jwt_manager.init_app(app)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(chat_bp, url_prefix='/api')
app.register_blueprint(api, url_prefix='/api')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    '''
    :returns: Main template used for the homepage
    '''
    return render_template('index.html')

@app.route('/conversation')
def conversation():
    '''
    :returns: Main template used for the chat interface
    '''
    return render_template('chat.html')
    
# Run with python app.py
if __name__ == '__main__':
    app.run(debug=True)
