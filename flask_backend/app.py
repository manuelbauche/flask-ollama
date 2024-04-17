'''
Application run file
'''
import os
from dotenv import load_dotenv
from flask import Flask, render_template
from extensions import db, jwt_manager
from api.auth import auth
from api.chat import chat_bp
from models import User

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}'
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
    return render_template('chat.html')
    
# Run with python app.py
if __name__ == '__main__':
    app.run(debug=True)
