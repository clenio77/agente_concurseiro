import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.base import Base
from app.main import app
from app.api.deps import get_db
from app.core.config import settings

# Configurar banco de dados de teste
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def db_engine():
    """Fixture para criar engine do banco de dados de teste."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    # Limpar após os testes
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Fixture para criar sessão do banco de dados de teste."""
    connection = db_engine.connect()
    transaction = connection.begin()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestingSessionLocal()
    
    yield session
    
    # Limpar após cada teste
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Fixture para criar cliente de teste."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db_session):
    """Fixture para criar usuário de teste."""
    from app.db.models.user import User
    from app.core.security import get_password_hash
    
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_admin(db_session):
    """Fixture para criar usuário administrador de teste."""
    from app.db.models.user import User
    from app.core.security import get_password_hash
    
    admin = User(
        email="admin@example.com",
        username="adminuser",
        hashed_password=get_password_hash("admin123"),
        full_name="Admin User",
        is_active=True,
        is_admin=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture(scope="function")
def token_headers(client, test_user):
    """Fixture para criar cabeçalhos com token de autenticação."""
    login_data = {
        "username": test_user.username,
        "password": "password123"
    }
    response = client.post(f"{settings.API_PREFIX}/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

@pytest.fixture(scope="function")
def admin_token_headers(client, test_admin):
    """Fixture para criar cabeçalhos com token de administrador."""
    login_data = {
        "username": test_admin.username,
        "password": "admin123"
    }
    response = client.post(f"{settings.API_PREFIX}/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}