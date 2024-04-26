'''
Application run file
'''
from flask import render_template
from extensions import db
from factory import create_app

app = create_app()
app.app_context().push()
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
