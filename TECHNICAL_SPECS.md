# 🔧 Especificações Técnicas - Agente Concurseiro

## 📋 Visão Geral Técnica

### **Arquitetura do Sistema**
- **Padrão**: Microserviços com API REST
- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI (Python 3.11+)
- **Banco de Dados**: PostgreSQL 15+ / SQLite (desenvolvimento)
- **Cache**: Redis 7+
- **Containerização**: Docker + Docker Compose
- **Monitoramento**: Prometheus + Grafana

### **Estrutura de Diretórios**
```
agente-concurseiro/
├── app/                          # Aplicação principal
│   ├── api/                      # API REST (FastAPI)
│   │   ├── main.py              # Aplicação FastAPI
│   │   └── routers/             # Endpoints organizados
│   ├── auth/                     # Sistema de autenticação
│   │   └── auth_manager.py      # Gerenciador JWT + bcrypt
│   ├── db/                       # Banco de dados
│   │   ├── models.py            # Modelos SQLAlchemy
│   │   └── database.py          # Configuração e conexão
│   ├── ai/                       # Integração IA
│   │   └── openai_integration.py # OpenAI GPT-4
│   ├── monitoring/               # Monitoramento
│   │   └── metrics.py           # Métricas Prometheus
│   ├── backup/                   # Sistema de backup
│   │   └── backup_manager.py    # Backup automático
│   ├── pages/                    # Páginas Streamlit
│   │   ├── redacao.py           # Sistema de redação
│   │   ├── analytics.py         # Analytics avançados
│   │   └── simulado.py          # Simulados
│   ├── utils/                    # Utilitários
│   │   ├── gamification.py      # Sistema de gamificação
│   │   ├── performance_predictor.py # Predição IA
│   │   ├── notifications.py     # Notificações
│   │   ├── dashboard.py         # Dashboard
│   │   └── config.py            # Configurações
│   └── app.py                   # Aplicação Streamlit principal
├── tools/                        # Ferramentas especializadas
│   ├── mock_exam_tool.py        # Geração de simulados
│   ├── writing_tool.py          # Avaliação de redação
│   ├── web_search_tool.py       # Busca de provas
│   ├── question_api_tool.py     # API de questões
│   └── recommendation_tool.py   # Recomendações IA
├── data/                         # Dados da aplicação
│   ├── users/                   # Dados de usuários
│   ├── questions/               # Banco de questões
│   └── dashboard/               # Dados do dashboard
├── config/                       # Configurações
├── scripts/                      # Scripts de deploy
├── monitoring/                   # Configurações de monitoramento
├── nginx/                        # Configuração Nginx
├── .github/workflows/            # CI/CD GitHub Actions
├── Dockerfile                    # Container principal
├── docker-compose.yml           # Orquestração
├── deploy.sh                    # Script de deploy
└── requirements-prod.txt        # Dependências produção
```

---

## 🗄️ Modelo de Dados

### **Entidades Principais**

#### **User (Usuário)**
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    
    -- Perfil do candidato
    target_exam VARCHAR(255),
    target_position VARCHAR(255),
    target_banca VARCHAR(50),
    target_city VARCHAR(100),
    education_level VARCHAR(50),
    experience_level VARCHAR(50) DEFAULT 'beginner',
    
    -- Configurações
    weekly_study_hours INTEGER DEFAULT 20,
    study_months INTEGER DEFAULT 6,
    exam_date TIMESTAMP,
    preferences JSON,
    notification_settings JSON,
    
    -- Metadados
    is_active BOOLEAN DEFAULT TRUE,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

#### **StudyPlan (Plano de Estudos)**
```sql
CREATE TABLE study_plans (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    banca VARCHAR(50) NOT NULL,
    cargo VARCHAR(255) NOT NULL,
    total_weeks INTEGER NOT NULL,
    weekly_hours INTEGER NOT NULL,
    
    -- Conteúdo estruturado
    subjects JSON NOT NULL,
    schedule JSON NOT NULL,
    milestones JSON DEFAULT '[]',
    
    -- Progresso
    is_active BOOLEAN DEFAULT TRUE,
    progress_percentage FLOAT DEFAULT 0.0,
    current_week INTEGER DEFAULT 1,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### **MockExam (Simulados)**
```sql
CREATE TABLE mock_exams (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    
    -- Configuração
    banca VARCHAR(50) NOT NULL,
    subjects JSON NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'medium',
    total_questions INTEGER NOT NULL,
    time_limit_minutes INTEGER,
    
    -- Conteúdo
    questions JSON NOT NULL,
    user_answers JSON DEFAULT '{}',
    
    -- Resultados
    score FLOAT,
    correct_answers INTEGER DEFAULT 0,
    time_spent_minutes INTEGER,
    subject_scores JSON DEFAULT '{}',
    
    -- Status
    status VARCHAR(20) DEFAULT 'created',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **Essay (Redações)**
```sql
CREATE TABLE essays (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    
    -- Configuração
    banca VARCHAR(50) NOT NULL,
    essay_type VARCHAR(50) NOT NULL,
    theme VARCHAR(500),
    
    -- Conteúdo
    text TEXT NOT NULL,
    word_count INTEGER,
    
    -- Avaliação
    final_score FLOAT,
    criterion_scores JSON DEFAULT '{}',
    feedback JSON DEFAULT '{}',
    strengths JSON DEFAULT '[]',
    weaknesses JSON DEFAULT '[]',
    suggestions JSON DEFAULT '[]',
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **UserStats (Estatísticas)**
```sql
CREATE TABLE user_stats (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id) UNIQUE,
    
    -- Gamificação
    level INTEGER DEFAULT 1,
    experience_points INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    
    -- Estudos
    total_study_hours FLOAT DEFAULT 0.0,
    current_streak INTEGER DEFAULT 0,
    max_streak INTEGER DEFAULT 0,
    study_days_count INTEGER DEFAULT 0,
    
    -- Performance
    mock_exams_completed INTEGER DEFAULT 0,
    best_mock_score FLOAT DEFAULT 0.0,
    average_mock_score FLOAT DEFAULT 0.0,
    essays_completed INTEGER DEFAULT 0,
    best_essay_score FLOAT DEFAULT 0.0,
    
    -- Atividade
    last_activity TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔧 APIs e Endpoints

### **Autenticação**
```http
POST   /auth/register          # Registrar usuário
POST   /auth/login             # Login
POST   /auth/change-password   # Alterar senha
GET    /auth/me                # Perfil atual
POST   /auth/verify-token      # Verificar token
```

### **Usuários**
```http
GET    /users/profile          # Obter perfil
PUT    /users/profile          # Atualizar perfil
GET    /users/stats            # Estatísticas
DELETE /users/account          # Desativar conta
```

### **Planos de Estudo**
```http
GET    /study-plans            # Listar planos
POST   /study-plans            # Criar plano
GET    /study-plans/{id}       # Obter plano
PUT    /study-plans/{id}       # Atualizar plano
DELETE /study-plans/{id}       # Excluir plano
GET    /study-plans/{id}/progress # Progresso
```

### **Simulados**
```http
GET    /mock-exams             # Listar simulados
POST   /mock-exams             # Criar simulado
GET    /mock-exams/{id}        # Obter simulado
POST   /mock-exams/{id}/submit # Submeter respostas
GET    /mock-exams/{id}/results # Resultados
```

### **Redações**
```http
GET    /essays                 # Listar redações
POST   /essays/evaluate        # Avaliar redação
GET    /essays/{id}            # Obter redação
GET    /essays/themes          # Temas disponíveis
GET    /essays/tips/{banca}    # Dicas por banca
```

### **Analytics**
```http
GET    /analytics/performance  # Análise de performance
GET    /analytics/predictions  # Predições
GET    /analytics/recommendations # Recomendações
GET    /analytics/metrics      # Métricas detalhadas
POST   /analytics/simulate     # Simular cenários
```

---

## 🤖 Integração com IA

### **OpenAI GPT-4**
```python
# Configuração
OPENAI_CONFIG = {
    "model": "gpt-4-turbo-preview",
    "max_tokens": 2000,
    "temperature": 0.7,
    "timeout": 30
}

# Uso para avaliação de redação
async def evaluate_essay_with_ai(text: str, banca: str) -> dict:
    prompt = f"""
    Avalie esta redação seguindo critérios da {banca}:
    
    {text}
    
    Retorne JSON com:
    - final_score (0-10)
    - criteria_scores (dict)
    - detailed_feedback (dict)
    - strengths (list)
    - weaknesses (list)
    - suggestions (list)
    """
    
    response = await openai_client.chat.completions.create(
        model=OPENAI_CONFIG["model"],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=OPENAI_CONFIG["max_tokens"]
    )
    
    return json.loads(response.choices[0].message.content)
```

### **Sistema de Fallback**
```python
# Quando OpenAI não está disponível
def fallback_essay_evaluation(text: str, banca: str) -> dict:
    # Usar algoritmos locais
    from tools.writing_tool import WritingTool
    tool = WritingTool()
    return tool.evaluate_essay_by_banca(text, banca)
```

---

## 📊 Sistema de Métricas

### **Métricas Prometheus**
```python
# Métricas de aplicação
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')
ACTIVE_USERS = Gauge('active_users', 'Active users')

# Métricas de negócio
MOCK_EXAMS_COMPLETED = Counter('mock_exams_completed_total', 'Mock exams completed')
ESSAYS_EVALUATED = Counter('essays_evaluated_total', 'Essays evaluated')
USER_REGISTRATIONS = Counter('user_registrations_total', 'User registrations')
```

### **Dashboards Grafana**
```json
{
  "dashboard": {
    "title": "Agente Concurseiro - Overview",
    "panels": [
      {
        "title": "Usuários Ativos",
        "type": "stat",
        "targets": [{"expr": "agente_concurseiro_active_users"}]
      },
      {
        "title": "Requests por Segundo",
        "type": "graph",
        "targets": [{"expr": "rate(agente_concurseiro_requests_total[5m])"}]
      },
      {
        "title": "Simulados Completados",
        "type": "stat",
        "targets": [{"expr": "increase(agente_concurseiro_mock_exams_completed_total[24h])"}]
      }
    ]
  }
}
```

---

## 🔐 Segurança

### **Autenticação JWT**
```python
# Configuração JWT
JWT_CONFIG = {
    "algorithm": "HS256",
    "access_token_expire_minutes": 60 * 24 * 7,  # 7 dias
    "secret_key": os.getenv("JWT_SECRET_KEY")
}

# Geração de token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_CONFIG["access_token_expire_minutes"])
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_CONFIG["secret_key"], algorithm=JWT_CONFIG["algorithm"])
```

### **Hash de Senhas**
```python
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

### **Validação de Dados**
```python
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        return v
```

---

## 🚀 Deploy e DevOps

### **Docker Configuration**
```dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Configurar aplicação
WORKDIR /app
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . .
RUN chown -R appuser:appuser /app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **CI/CD Pipeline**
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements-prod.txt
      - name: Run tests
        run: pytest tests/ --cov=app
      - name: Security scan
        run: bandit -r app/
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: ./deploy.sh production
```

---

## 📈 Performance e Escalabilidade

### **Otimizações Implementadas**
- ✅ **Cache Redis** para sessões e dados frequentes
- ✅ **Connection pooling** para banco de dados
- ✅ **Lazy loading** de componentes Streamlit
- ✅ **Compressão gzip** para responses
- ✅ **CDN** para assets estáticos
- ✅ **Rate limiting** por usuário
- ✅ **Pagination** em listagens

### **Métricas de Performance**
```
🚀 Tempo de resposta API: < 200ms (95th percentile)
📊 Throughput: 1000+ requests/segundo
👥 Usuários simultâneos: 10.000+
💾 Uso de memória: < 512MB por container
🔄 Uptime: 99.9%
```

### **Escalabilidade Horizontal**
```yaml
# docker-compose.yml
services:
  app:
    image: agente-concurseiro:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
  
  nginx:
    image: nginx:alpine
    depends_on:
      - app
    ports:
      - "80:80"
```

---

## 🔧 Configurações Avançadas

### **Variáveis de Ambiente**
```bash
# Aplicação
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info

# Banco de dados
DATABASE_URL=postgresql://user:pass@host:5432/db
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Cache
REDIS_URL=redis://host:6379/0
CACHE_TTL=3600

# IA
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_MAX_TOKENS=2000

# Segurança
JWT_SECRET_KEY=super-secret-key
CORS_ORIGINS=https://app.com,https://api.com

# Monitoramento
PROMETHEUS_ENABLED=true
GRAFANA_ADMIN_PASSWORD=admin123

# Backup
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *
S3_BUCKET=backups-bucket
```

### **Configuração de Produção**
```python
# config/production.py
PRODUCTION_CONFIG = {
    "database": {
        "pool_size": 20,
        "max_overflow": 30,
        "pool_pre_ping": True,
        "pool_recycle": 3600
    },
    "redis": {
        "max_connections": 100,
        "retry_on_timeout": True,
        "socket_keepalive": True
    },
    "security": {
        "jwt_expiration": 7 * 24 * 60 * 60,  # 7 dias
        "rate_limit": "100/hour",
        "cors_max_age": 86400
    },
    "monitoring": {
        "metrics_enabled": True,
        "health_check_interval": 30,
        "log_level": "INFO"
    }
}
```

Este documento técnico complementa o README principal e fornece todas as informações necessárias para desenvolvedores que queiram entender, modificar ou contribuir com o sistema.
