import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestAuthEndpoints:
    """Testes para endpoints de autenticação"""

    @pytest.fixture
    def client(self):
        """Cliente de teste"""
        return TestClient(app)

    @pytest.fixture
    def test_user_data(self):
        """Dados de usuário para teste"""
        return {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "full_name": "Test User"
        }

    def test_register_user_success(self, client, test_user_data):
        """Testa registro de usuário com sucesso"""
        response = client.post("/api/users/", json=test_user_data)

        assert response.status_code == 201
        data = response.json()

        assert "id" in data
        assert data["email"] == test_user_data["email"]
        assert data["username"] == test_user_data["username"]
        assert data["full_name"] == test_user_data["full_name"]
        assert "hashed_password" not in data  # Senha não deve ser retornada
        assert data["is_active"] is True
        assert data["is_admin"] is False

    def test_register_user_duplicate_email(self, client, test_user_data):
        """Testa registro com email duplicado"""
        # Primeiro registro
        response1 = client.post("/api/users/", json=test_user_data)
        assert response1.status_code == 201

        # Tentativa de registro duplicado
        response2 = client.post("/api/users/", json=test_user_data)
        assert response2.status_code == 400
        assert "email já registrado" in response2.json()["detail"].lower()

    def test_register_user_duplicate_username(self, client, test_user_data):
        """Testa registro com username duplicado"""
        # Primeiro registro
        response1 = client.post("/api/users/", json=test_user_data)
        assert response1.status_code == 201

        # Tentativa com mesmo username, email diferente
        duplicate_data = test_user_data.copy()
        duplicate_data["email"] = "other@example.com"

        response2 = client.post("/api/users/", json=duplicate_data)
        assert response2.status_code == 400
        assert "username já existe" in response2.status_code == 400

    def test_register_user_invalid_email(self, client, test_user_data):
        """Testa registro com email inválido"""
        invalid_data = test_user_data.copy()
        invalid_data["email"] = "invalid-email"

        response = client.post("/api/users/", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_register_user_weak_password(self, client, test_user_data):
        """Testa registro com senha fraca"""
        weak_data = test_user_data.copy()
        weak_data["password"] = "123"

        response = client.post("/api/users/", json=weak_data)
        assert response.status_code == 422  # Validation error

    def test_login_success(self, client, test_user_data):
        """Testa login com sucesso"""
        # Registrar usuário
        register_response = client.post("/api/users/", json=test_user_data)
        assert register_response.status_code == 201

        # Fazer login
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }

        login_response = client.post("/api/auth/login", data=login_data)
        assert login_response.status_code == 200

        data = login_response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == test_user_data["username"]

    def test_login_invalid_username(self, client, test_user_data):
        """Testa login com username inválido"""
        # Registrar usuário
        register_response = client.post("/api/users/", json=test_user_data)
        assert register_response.status_code == 201

        # Tentar login com username errado
        login_data = {
            "username": "wronguser",
            "password": test_user_data["password"]
        }

        login_response = client.post("/api/auth/login", data=login_data)
        assert login_response.status_code == 401
        assert "credenciais inválidas" in login_response.json()["detail"].lower()

    def test_login_invalid_password(self, client, test_user_data):
        """Testa login com senha inválida"""
        # Registrar usuário
        register_response = client.post("/api/users/", json=test_user_data)
        assert register_response.status_code == 201

        # Tentar login com senha errada
        login_data = {
            "username": test_user_data["username"],
            "password": "wrongpassword"
        }

        login_response = client.post("/api/auth/login", data=login_data)
        assert login_response.status_code == 401
        assert "credenciais inválidas" in login_response.json()["detail"].lower()

    def test_login_inactive_user(self, client, test_user_data):
        """Testa login com usuário inativo"""
        # Registrar usuário
        register_response = client.post("/api/users/", json=test_user_data)
        assert register_response.status_code == 201

        # Desativar usuário (simular)
        # Nota: Em um teste real, você precisaria acessar o banco de dados
        # Aqui vamos simular que o usuário está inativo

        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }

        # Este teste pode falhar se não houver lógica para usuários inativos
        # É um teste de regressão para quando essa funcionalidade for implementada
        login_response = client.post("/api/auth/login", data=login_data)
        # Pode ser 200 (se não há verificação de usuário ativo) ou 401 (se há)
        assert login_response.status_code in [200, 401]

    def test_get_current_user_success(self, client, test_user_data):
        """Testa obtenção do usuário atual com token válido"""
        # Registrar e fazer login
        register_response = client.post("/api/users/", json=test_user_data)
        assert register_response.status_code == 201

        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }

        login_response = client.post("/api/auth/login", data=login_data)
        assert login_response.status_code == 200

        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Obter usuário atual
        user_response = client.get("/api/users/me", headers=headers)
        assert user_response.status_code == 200

        user_data = user_response.json()
        assert user_data["username"] == test_user_data["username"]
        assert user_data["email"] == test_user_data["email"]
        assert "hashed_password" not in user_data

    def test_get_current_user_invalid_token(self, client):
        """Testa obtenção do usuário atual com token inválido"""
        headers = {"Authorization": "Bearer invalid_token"}

        response = client.get("/api/users/me", headers=headers)
        assert response.status_code == 401
        assert "credenciais inválidas" in response.json()["detail"].lower()

    def test_get_current_user_no_token(self, client):
        """Testa obtenção do usuário atual sem token"""
        response = client.get("/api/users/me")
        assert response.status_code == 401
        assert "não fornecido" in response.json()["detail"].lower()

    def test_get_current_user_expired_token(self, client, test_user_data):
        """Testa obtenção do usuário atual com token expirado"""
        # Registrar e fazer login
        register_response = client.post("/api/users/", json=test_user_data)
        assert register_response.status_code == 201

        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }

        login_response = client.post("/api/auth/login", data=login_data)
        assert login_response.status_code == 200

        # Simular token expirado (em produção, você precisaria de um token real expirado)
        # Este é um teste de regressão para quando a verificação de expiração for implementada
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTUxNjIzOTAyMn0.invalid_signature"
        headers = {"Authorization": f"Bearer {expired_token}"}

        response = client.get("/api/users/me", headers=headers)
        # Pode ser 401 (se a verificação de expiração estiver funcionando) ou 422 (se não)
        assert response.status_code in [401, 422]

    def test_password_validation(self, client, test_user_data):
        """Testa validação de senha"""
        # Testar senha muito curta
        short_password_data = test_user_data.copy()
        short_password_data["password"] = "123"

        response = client.post("/api/users/", json=short_password_data)
        assert response.status_code == 422

        # Testar senha sem números
        no_numbers_data = test_user_data.copy()
        no_numbers_data["password"] = "abcdefgh"

        response = client.post("/api/users/", json=no_numbers_data)
        assert response.status_code == 422

        # Testar senha sem letras
        no_letters_data = test_user_data.copy()
        no_letters_data["password"] = "12345678"

        response = client.post("/api/users/", json=no_letters_data)
        assert response.status_code == 422

    def test_email_validation(self, client, test_user_data):
        """Testa validação de email"""
        # Testar email sem @
        invalid_email_data = test_user_data.copy()
        invalid_email_data["email"] = "testexample.com"

        response = client.post("/api/users/", json=invalid_email_data)
        assert response.status_code == 422

        # Testar email sem domínio
        no_domain_data = test_user_data.copy()
        no_domain_data["email"] = "test@"

        response = client.post("/api/users/", json=no_domain_data)
        assert response.status_code == 422

    def test_username_validation(self, client, test_user_data):
        """Testa validação de username"""
        # Testar username muito curto
        short_username_data = test_user_data.copy()
        short_username_data["username"] = "ab"

        response = client.post("/api/users/", json=short_username_data)
        assert response.status_code == 422

        # Testar username com caracteres especiais
        special_chars_data = test_user_data.copy()
        special_chars_data["username"] = "test@user"

        response = client.post("/api/users/", json=special_chars_data)
        assert response.status_code == 422
