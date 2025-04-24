import sys
import os

# Добавляем путь к папке src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    # Проверка несуществующего пользователя
    response = client.get("/api/v1/user", params={'email': 'invalid@mail.com'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

def test_create_user_with_valid_email():
    # Создание нового пользователя
    new_user = {
        'name': 'New User',
        'email': 'new@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)  # Проверяем, что возвращается ID

    # Проверка, что пользователь добавлен
    check_response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert check_response.status_code == 200

def test_create_user_with_invalid_email():
    # Попытка создать пользователя с существующим email
    existing_email = users[0]['email']
    response = client.post("/api/v1/user", json={'name': 'Test', 'email': existing_email})
    assert response.status_code == 409
    assert response.json() == {'detail': 'User with this email already exists'}

def test_delete_user():
    # Удаление существующего пользователя
    email_to_delete = users[1]['email']
    response = client.delete("/api/v1/user", params={'email': email_to_delete})
    assert response.status_code == 204

    # Проверка, что пользователь удалён
    check_response = client.get("/api/v1/user", params={'email': email_to_delete})
    assert check_response.status_code == 404