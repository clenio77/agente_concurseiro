import pytest
from fastapi import status

from app.core.config import settings

def test_login_success(client, test_user):
    """Teste de login com credenciais válidas."""
    login_data = {
        "username": test_user.username,
        "password": "password123"
    }
    response = client.post(f"{settings.API_PREFIX}/auth/login", data=login_data)
    
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_user):
    """Teste de login com credenciais inválidas."""
    login_data = {
        "username": test_user.username,
        "password": "wrong_password"
    }
    response = client.post(f"{settings.API_PREFIX}/auth/login", data=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_inactive_user(client, db_session, test_user):
    """Teste de login com usuário inativo."""
    # Desativar usuário
    test_user.is_active = False
    db_session.commit()
    
    login_data = {
        "username": test_user.username,
        "password": "password123"
    }
    response = client.post(f"{settings.API_PREFIX}/auth/login", data=login_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_test_token(client, token_headers):
    """Teste de validação de token."""
    response = client.post(
        f"{settings.API_PREFIX}/auth/test-token",
        headers=token_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["email"] == "test@example.com"
    assert user_data["username"] == "testuser"

def test_test_token_invalid(client):
    """Teste de validação de token inválido."""
    response = client.post(
        f"{settings.API_PREFIX}/auth/test-token",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED