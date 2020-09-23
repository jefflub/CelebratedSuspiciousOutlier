from main import app

def test_hello_world():
    client = app.test_client()
    rv = client.get('/')
    data = rv.get_json()
    assert data['name'] == 'Hello, World!'

def test_count():
    client = app.test_client()
    rv = client.get('/count')
    data = rv.get_json()
    assert data['count'] == 3

def test_add_card():
    client= app.test_client()
    rv = client.post('/add_card', json={ 'title': 'New Card', 'notes': 'Hello!' })
    data = rv.get_json()
    print(data)
    assert rv.status_code == 200
    assert data['title'] == 'New Card'