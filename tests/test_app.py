from starlette.testclient import TestClient

from app import app

client = TestClient(app)


def test_api():
    response = client.get('/api')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert response.json() == {'hello': 'asgi'}


def test_ws():
    with client.websocket_connect('/ws') as websocket:
        data = websocket.receive_json()
        assert data == {'hello': 'asgi'}
        data = websocket.receive_json()
        assert data == {'goodbye': 'asgi'}


def test_404_handler():
    response = client.get('/not_found')
    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/json'
    assert response.json() == {'detail': 'not found'}


def test_static():
    response = client.get('/static/asgi.html')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert response.content == b'<a href="https://asgi.readthedocs.io/en/latest/">ASGI docs</a>\n'
