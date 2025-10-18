# backend/tests/test_comments.py
import json
import pytest # type: ignore
from app import create_app, db
from app.config import TestConfig
from app.models import Comment

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_comment(client):
    payload = {"task_id": 1, "text": "First comment", "author": "alice"}
    resp = client.post('/api/comments/', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['task_id'] == 1
    assert data['text'] == "First comment"
    assert data['author'] == "alice"
    assert 'id' in data

def test_get_comments_by_task(client):
    # create two comments
    c1 = Comment(task_id=10, text="c1")
    c2 = Comment(task_id=10, text="c2")
    db.session.add_all([c1, c2])
    db.session.commit()

    resp = client.get('/api/comments/task/10')
    assert resp.status_code == 200
    arr = resp.get_json()
    assert isinstance(arr, list)
    assert len(arr) == 2
    assert arr[0]['text'] == 'c1'

def test_update_comment(client):
    c = Comment(task_id=5, text="old text", author="bob")
    db.session.add(c)
    db.session.commit()
    payload = {"text": "new text", "author": "bobby"}
    resp = client.put(f'/api/comments/{c.id}', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['text'] == "new text"
    assert data['author'] == "bobby"

def test_delete_comment(client):
    c = Comment(task_id=2, text="to delete")
    db.session.add(c)
    db.session.commit()
    resp = client.delete(f'/api/comments/{c.id}')
    assert resp.status_code == 204
    # ensure it is gone
    assert Comment.query.get(c.id) is None

def test_create_invalid_payload(client):
    # missing text
    resp = client.post('/api/comments/', json={"task_id": 1})
    assert resp.status_code == 400
