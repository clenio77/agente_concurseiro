import asyncio
import os
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.db.base import Base
from app.main import app

# Configurar banco de dados de teste
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Cria event loop para testes assíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

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

@pytest.fixture
def client(db_session):
    """Fixture para criar cliente de teste da API."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user():
    """Fixture para criar usuário de teste."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }

@pytest.fixture
def auth_headers(client, test_user):
    """Fixture para criar headers de autenticação."""
    # Criar usuário
    response = client.post("/api/users/", json=test_user)
    assert response.status_code == 201

    # Fazer login
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_openai():
    """Mock para OpenAI API."""
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {
            "choices": [{
                "message": {
                    "content": "Resposta simulada da IA"
                }
            }]
        }
        yield mock

@pytest.fixture
def mock_redis():
    """Mock para Redis."""
    with patch('redis.Redis') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def sample_essay():
    """Texto de redação de exemplo para testes."""
    return """
    A sustentabilidade ambiental é um tema de extrema relevância na sociedade contemporânea. 
    O desenvolvimento econômico deve ser equilibrado com a preservação dos recursos naturais 
    para garantir um futuro viável para as próximas gerações.
    
    Em primeiro lugar, é fundamental reconhecer que os recursos naturais são finitos. 
    A exploração desenfreada pode levar ao esgotamento de matérias-primas essenciais, 
    comprometendo não apenas o meio ambiente, mas também a própria economia.
    
    Além disso, as mudanças climáticas representam um desafio global que requer 
    ações coordenadas entre países e setores da sociedade. A implementação de 
    políticas públicas eficazes é essencial para mitigar os impactos ambientais.
    
    Portanto, é necessário buscar um modelo de desenvolvimento que concilie 
    crescimento econômico com responsabilidade ambiental, através de tecnologias 
    limpas e práticas sustentáveis.
    """

@pytest.fixture
def sample_study_plan():
    """Plano de estudo de exemplo para testes."""
    return {
        "title": "Plano de Estudos - Analista TRF",
        "description": "Plano personalizado para concurso TRF",
        "cargo": "Analista Judiciário",
        "concurso": "TRF",
        "banca": "CESPE",
        "cidade": "Brasília",
        "study_hours_per_week": 20,
        "duration_months": 6,
        "content": {
            "subjects": {
                "Português": {"hours": 4, "priority": "Alta"},
                "Matemática": {"hours": 3, "priority": "Média"},
                "Direito": {"hours": 8, "priority": "Alta"},
                "Informática": {"hours": 2, "priority": "Baixa"}
            },
            "schedule": {
                "segunda": ["Português", "Direito"],
                "terca": ["Matemática", "Direito"],
                "quarta": ["Português", "Informática"],
                "quinta": ["Direito"],
                "sexta": ["Matemática", "Direito"]
            }
        }
    }
