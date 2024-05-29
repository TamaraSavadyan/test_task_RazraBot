import pytest
from todo_app.app import app, db
from todo_app.models import Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_add_task(client):
    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task'
    })
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['title'] == 'Test Task'
    assert json_data['description'] == 'This is a test task'

def test_get_tasks(client):
    client.post('/tasks', json={'title': 'Task 1', 'description': 'First task'})
    client.post('/tasks', json={'title': 'Task 2', 'description': 'Second task'})
    response = client.get('/tasks')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2
    assert json_data[0]['title'] == 'Task 1'
    assert json_data[1]['title'] == 'Task 2'

def test_get_task(client):
    response = client.post('/tasks', json={'title': 'Test Task', 'description': 'This is a test task'})
    task_id = response.get_json()['id']
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['title'] == 'Test Task'
    assert json_data['description'] == 'This is a test task'

def test_update_task(client):
    response = client.post('/tasks', json={'title': 'Old Title', 'description': 'Old description'})
    task_id = response.get_json()['id']
    response = client.put(f'/tasks/{task_id}', json={'title': 'New Title', 'description': 'New description'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['title'] == 'New Title'
    assert json_data['description'] == 'New description'

def test_delete_task(client):
    response = client.post('/tasks', json={'title': 'Task to delete', 'description': 'This will be deleted'})
    task_id = response.get_json()['id']
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 404
