# 📖 Documentação Técnica - Agente Concurseiro v2.0

## 🏗️ Arquitetura Detalhada

### **Estrutura de Diretórios**

```
agente_concurseiro/
├── app/                          # Código fonte principal
│   ├── components/               # Componentes Streamlit (11 módulos)
│   │   ├── voice_assistant.py    # Assistente de voz
│   │   ├── behavioral_analysis.py # Análise comportamental
│   │   ├── trend_prediction.py   # Predição de tendências
│   │   ├── augmented_reality.py  # Realidade aumentada
│   │   ├── ai_predictor.py       # IA preditiva
│   │   ├── spaced_repetition.py  # Revisão espaçada
│   │   ├── collaborative_features.py # Recursos colaborativos
│   │   ├── mobile_companion.py   # Mobile companion
│   │   ├── dashboard.py          # Dashboard principal
│   │   ├── gamification.py       # Sistema de gamificação
│   │   └── chatbot.py           # Assistente virtual
│   ├── agents/                   # Agentes CrewAI (8 agentes)
│   ├── api/                      # Endpoints FastAPI
│   ├── core/                     # Configurações centrais
│   ├── db/                       # Modelos SQLAlchemy
│   ├── utils/                    # Utilitários
│   └── app.py                    # Aplicação principal
├── tools/                        # Ferramentas especializadas (13 tools)
├── tests/                        # Testes automatizados (47 testes)
├── data/                         # Dados e configurações
├── docs/                         # Documentação
└── scripts/                      # Scripts de automação
```

### **Padrões de Arquitetura**

- **Component-Based:** Cada funcionalidade é um componente independente
- **Session State Management:** Estado persistente entre interações
- **Enum-Based Types:** Type safety com enumerações
- **Mock Data Generation:** Dados simulados para demonstração
- **Modular Testing:** Testes isolados por componente

## 🧪 Sistema de Testes

### **Estrutura de Testes**

```python
# Exemplo de estrutura de teste
class TestVoiceAssistant:
    def setup_method(self):
        # Limpar session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        self.voice_assistant = VoiceAssistant()

    def test_initialization(self):
        assert self.voice_assistant is not None
        assert 'voice_settings' in st.session_state

    def test_command_processing(self):
        result = self.voice_assistant.process_voice_command("ler questão")
        assert result['success'] == True
```

### **Cobertura de Testes**

- **Voice Assistant:** 15 testes (100% passando)
- **Behavioral Analysis:** 16 testes (100% passando)
- **Trend Prediction:** 16 testes (100% passando)
- **Total:** 47 testes automatizados

### **Executar Testes**

```bash
# Todos os testes
pytest -v

# Testes específicos
pytest test_voice_assistant.py -v
pytest test_behavioral_analysis.py -v
pytest test_trend_prediction.py -v

# Com cobertura
pytest --cov=app --cov-report=html
```

## 🔧 APIs e Integrações

### **FastAPI Endpoints**

```python
# Estrutura de endpoints
/api/v1/
├── /auth/                    # Autenticação JWT
├── /users/                   # Gestão de usuários
├── /study-plans/            # Planos de estudo
├── /quizzes/                # Simulados
├── /flashcards/             # Revisão espaçada
├── /performance/            # Métricas
├── /gamification/           # Sistema de pontos
└── /analytics/              # Analytics avançado
```

### **Agentes CrewAI**

```python
# 8 Agentes especializados
agents = {
    'SearchAgent': 'Busca inteligente de provas',
    'StudyPlanAgent': 'Criação de planos personalizados',
    'MockExamAgent': 'Geração de simulados',
    'WritingAgent': 'Avaliação de redações',
    'CoordinatorAgent': 'Coordenação de tarefas',
    'SpacedRepetitionAgent': 'Sistema de repetição',
    'PerformancePredictionAgent': 'Análise preditiva',
    'QuestionAgent': 'Gestão de questões'
}
```

### **Ferramentas Especializadas**

```python
# 13 Tools implementadas
tools = [
    'MockExamTool',           # Simulados adaptativos
    'WebSearchTool',          # Busca de provas
    'QuestionAPITool',        # Banco de questões
    'StudyPlanTool',          # Planos personalizados
    'SpacedRepetitionTool',   # Algoritmo SM-2
    'PerformanceAnalysisTool', # Análise de desempenho
    'WritingTool',            # Avaliação de redações
    'RecommendationTool',     # Recomendações IA
    'ProgressTrackingTool',   # Acompanhamento
    'CalendarIntegrationTool', # Integração calendário
    'ExamAnalysisTool',       # Análise de provas
    'CoordinationTool',       # Coordenação
    'PerformancePredictionTool' # Predições ML
]
```

## 🗄️ Modelo de Dados

### **Tabelas Principais**

```sql
-- Usuários e Autenticação
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Planos de Estudo
CREATE TABLE study_plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    target_exam VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Simulados
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    total_questions INTEGER,
    score DECIMAL(5,2),
    completed_at TIMESTAMP
);

-- Sistema de Repetição Espaçada
CREATE TABLE flashcards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    difficulty VARCHAR(50),
    next_review TIMESTAMP
);

-- Registros de Performance
CREATE TABLE performance_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    activity_type VARCHAR(100),
    score DECIMAL(5,2),
    duration_minutes INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **Relacionamentos**

- User → StudyPlan (1:N)
- User → Quiz (1:N)
- User → Flashcard (1:N)
- User → PerformanceRecord (1:N)
- Quiz → QuizQuestion (1:N)
- Flashcard → FlashcardReview (1:N)

## 🚀 Deploy e DevOps

### **Docker Configuration**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501 8000

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Docker Compose**

```yaml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "8501:8501"
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/agente_concurseiro
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: agente_concurseiro
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### **Vercel Configuration**

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "PYTHONPATH": ".",
    "STREAMLIT_SERVER_PORT": "8501"
  }
}
```

## 🔒 Segurança

### **Autenticação JWT**

```python
from fastapi_users.authentication import JWTAuthentication

jwt_authentication = JWTAuthentication(
    secret=SECRET_KEY,
    lifetime_seconds=3600,
    tokenUrl="auth/jwt/login",
)
```

### **Validação de Dados**

```python
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v
```

### **Rate Limiting**

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/upload")
@limiter.limit("5/minute")
async def upload_file(request: Request):
    pass
```

## 📊 Monitoramento

### **Health Checks**

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "2.0.0",
        "database": check_database_connection(),
        "redis": check_redis_connection()
    }
```

### **Logging Estruturado**

```python
import structlog

logger = structlog.get_logger()

def log_user_action(user_id: str, action: str, details: dict):
    logger.info(
        "User action",
        user_id=user_id,
        action=action,
        details=details,
        timestamp=datetime.utcnow()
    )
```

### **Métricas de Performance**

```python
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time

        logger.info(
            "Function performance",
            function=func.__name__,
            duration=duration,
            args_count=len(args)
        )
        return result
    return wrapper
```

## 🔧 Configuração de Desenvolvimento

### **Ambiente Virtual**

```bash
# Criar ambiente
python -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements-dev.txt
```

### **Variáveis de Ambiente**

```env
# .env para desenvolvimento
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite:///./data/app.db
OPENAI_API_KEY=sk-test-key
SECRET_KEY=dev-secret-key
REDIS_URL=redis://localhost:6379
```

### **Scripts de Desenvolvimento**

```bash
# Executar aplicação
python app.py

# Executar testes
pytest -v

# Executar com hot reload
streamlit run app.py --server.runOnSave=true

# Executar API separadamente
uvicorn app.main:app --reload --port 8000
```

## 🐛 Troubleshooting

### **Problemas Comuns**

#### **Erro de Importação**

```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Ou instalar em modo desenvolvimento
pip install -e .
```

#### **Erro de Banco de Dados**

```bash
# Verificar conexão
python -c "from app.db import engine; print(engine.execute('SELECT 1').scalar())"

# Executar migrations
alembic upgrade head
```

#### **Erro de Memória**

```python
# Otimizar uso de memória
import gc
gc.collect()

# Limitar cache do Streamlit
@st.cache_data(max_entries=100)
def cached_function():
    pass
```

### **Debug e Profiling**

```python
# Debug com pdb
import pdb; pdb.set_trace()

# Profiling de performance
import cProfile
cProfile.run('main_function()')

# Memory profiling
from memory_profiler import profile

@profile
def memory_intensive_function():
    pass
```

## 📚 Recursos Adicionais

### **Documentação de APIs**

- FastAPI Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### **Ferramentas de Desenvolvimento**

- **Black:** Formatação de código
- **Flake8:** Linting
- **MyPy:** Type checking
- **Pytest:** Testes automatizados
- **Pre-commit:** Hooks de commit

### **Comandos Úteis**

```bash
# Formatação de código
black app/ tests/

# Linting
flake8 app/ tests/

# Type checking
mypy app/

# Executar pre-commit
pre-commit run --all-files
```

---

**📅 Última atualização:** 04/08/2025  
**👨‍💻 Mantido por:** Equipe Agente Concurseiro  
**📧 Contato técnico:** dev@agenteconcurseiro.com
