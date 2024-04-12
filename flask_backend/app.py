'''
Application run file
'''
import logging
from flask import Flask, request, render_template
from api.ai_process import chat

app = Flask(__name__)

@app.route('/')
def index():
    '''
    :returns: Main template used for the homepage
    '''
    return render_template('chat.html')


@app.route('/get', methods=['GET', 'POST'])
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
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run()
