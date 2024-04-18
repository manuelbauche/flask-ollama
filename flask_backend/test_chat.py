'''
Functionality testing
'''
import pytest
from app import app
from models import User
from extensions import db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    db.session.remove()
    db.drop_all()

def test_chat(client):
    # Register a test user
    response = client.post('/api/register', json={'username': 'john', 'password': 'doe'})
    assert response.status_code == 200

    # Login the test user
    response = client.post('/api/login', json={'username': 'john', 'password': 'doe'})
    assert response.status_code == 200
    token = response.get_json()['token']

    # Send a chat message
    response = client.post('/api/chat', headers={'Authorization': f'Bearer {token}'}, json={'message': 'Hello'})
    assert response.status_code == 200
    assert 'Hello' in response.get_data(as_text=True)