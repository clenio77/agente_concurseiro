import pytest
from fastapi import status

from app.core.config import settings

def test_create_user(client):
    """Teste de criação de usuário."""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123",
        "full_name": "New User"
    }
    response = client.post(f"{settings.API_PREFIX}/users/", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["username"] == user_data["username"]
    assert created_user["full_name"] == user_data["full_name"]
    assert "password" not in created_user

def test_create_user_existing_email(client, test_user):
    """Teste de criação de usuário com email existente."""
    user_data = {
        "email": test_user.email,
        "username": "anotheruser",
        "password": "password123",
        "full_name": "Another User"
    }
    response = client.post(f"{settings.API_PREFIX}/users/", json=user_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_get_users(client, admin_token_headers, test_user, test_admin):
    """Teste de obtenção de lista de usuários (apenas admin)."""
    response = client.get(
        f"{settings.API_PREFIX}/users/",
        headers=admin_token_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) >= 2  # Pelo menos o usuário de teste e o admin

def test_get_users_normal_user(client, token_headers):
    """Teste de obtenção de lista de usuários com usuário normal (deve falhar)."""
    response = client.get(
        f"{settings.API_PREFIX}/users/",
        headers=token_headers
    )
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_user(client, token_headers, test_user):
    """Teste de obtenção de usuário por ID."""
    response = client.get(
        f"{settings.API_PREFIX}/users/{test_user.id}",
        headers=token_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["id"] == str(test_user.id)
    assert user["email"] == test_user.email
   