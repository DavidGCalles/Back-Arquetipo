import pytest
from flask import Flask
from app.routes.demo_crud import crud_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(crud_bp)
    with app.test_client() as client:
        yield client

def test_get_all_items(client, mocker):
    mocker.patch('app.dao.generic_dao.BaseDAO.generic_get_all', return_value=[{"id": 1, "name": "Item 1"}])
    response = client.get('/demo_crud')
    assert response.status_code == 200
    assert response.json == [{"id": 1, "name": "Item 1"}]

def test_insert_item(client, mocker):
    mocker.patch('app.dao.generic_dao.BaseDAO.generic_insert', return_value=True)
    response = client.post('/demo_crud', json={"name": "New Item"})
    assert response.status_code == 201
    assert response.json == {"message": "New item inserted"}

def test_get_item_by_id(client, mocker):
    mocker.patch('app.dao.generic_dao.BaseDAO.generic_get_by_field', return_value={"id": 1, "name": "Item 1"})
    response = client.get('/demo_crud/item/1')
    assert response.status_code == 200
    assert response.json == {"id": 1, "name": "Item 1"}

def test_update_item(client, mocker):
    mocker.patch('app.dao.generic_dao.BaseDAO.generic_update', return_value=True)
    response = client.patch('/demo_crud/item/1', json={"id": 1, "name": "Updated Item"})
    assert response.status_code == 200
    assert response.json == {}