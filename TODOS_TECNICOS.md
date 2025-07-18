# 🔧 TODOs Técnicos - Agente Concurseiro

**Para:** Equipe de Desenvolvimento  
**Prioridade:** Ordem de implementação sugerida  
**Status:** Ready to implement  

---

## 🔥 SPRINT 1: Testes e Estabilidade (Semana 1-2)

### 1.1 Sistema de Testes Críticos

#### 📁 `tests/tools/`
```python
# tests/tools/test_writing_tool.py
import pytest
from tools.writing_tool import WritingTool

class TestWritingTool:
    def setup_method(self):
        self.tool = WritingTool()
    
    def test_evaluate_essay_cespe(self):
        essay = "Texto de teste para CESPE..."
        result = self.tool.evaluate_essay_by_banca(essay, "CESPE")
        assert "score_final" in result
        assert 0 <= result["score_final"] <= 10
    
    def test_get_tema_by_banca(self):
        result = self.tool.get_tema_by_banca("CESPE", "Analista")
        assert "tema" in result
        assert "contexto" in result

# tests/tools/test_mock_exam_tool.py
from tools.mock_exam_tool import MockExamTool

class TestMockExamTool:
    def test_generate_exam(self):
        tool = MockExamTool()
        exam = tool.generate_mock_exam("CESPE", ["Português"], 5)
        assert "questions" in exam
        assert len(exam["questions"]) == 5

# tests/tools/test_question_api_tool.py
from tools.question_api_tool import QuestionAPITool

class TestQuestionAPITool:
    def test_fetch_questions(self):
        tool = QuestionAPITool()
        questions = tool.fetch_questions(["Português"], "medium", 3)
        assert len(questions) == 3
        assert all("subject" in q for q in questions)
```

#### 📁 `tests/agents/`
```python
# tests/agents/test_crew_integration.py
import pytest
from app.crew import run_crew

class TestCrewIntegration:
    def test_complete_workflow(self):
        result = run_crew("Analista", "TRF", "CESPE", "Brasília", 20, 6)
        required_keys = ["exam_data", "study_plan", "mock_exam", 
                        "spaced_repetition_plan", "performance_prediction"]
        assert all(key in result for key in required_keys)
    
    def test_agents_initialization(self):
        from agents.search_agent import create_search_agent
        agent = create_search_agent()
        assert agent.role == "Especialista em Busca de Provas"
```

#### 📁 `tests/api/`
```python
# tests/api/test_study_plans.py
import pytest
from fastapi.testclient import TestClient

class TestStudyPlansAPI:
    def test_create_study_plan(self, client, auth_headers):
        plan_data = {
            "title": "Teste TRF",
            "cargo": "Analista",
            "banca": "CESPE",
            "study_hours_per_week": 20,
            "duration_months": 6
        }
        response = client.post("/study-plans/", json=plan_data, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["title"] == "Teste TRF"

# tests/api/test_quizzes.py
class TestQuizzesAPI:
    def test_create_quiz(self, client, auth_headers):
        quiz_data = {
            "title": "Quiz Teste",
            "difficulty": "medium",
            "subjects": ["Português"]
        }
        response = client.post("/quizzes/", json=quiz_data, headers=auth_headers)
        assert response.status_code == 201
```

### 1.2 Configuração CI/CD

#### 📁 `.github/workflows/ci.yml`
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-prod.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=app --cov-report=html
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 app/ --count --max-line-length=88 --statistics
```

### 1.3 Sistema de Logging

#### 📁 `app/core/logger.py`
```python
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
import structlog

def setup_logging():
    """Configure structured logging"""
    
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    
    # Add file handler
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    logging.getLogger().addHandler(file_handler)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

# Usage:
logger = structlog.get_logger()
```

### 1.4 Error Handling

#### 📁 `app/core/exceptions.py`
```python
from fastapi import HTTPException
from typing import Any, Dict, Optional

class AgenteConcurseiroException(Exception):
    """Base exception for the application"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class AIToolException(AgenteConcurseiroException):
    """Exception for AI tool errors"""
    pass

class DatabaseException(AgenteConcurseiroException):
    """Exception for database errors"""
    pass

class AuthenticationException(AgenteConcurseiroException):
    """Exception for authentication errors"""
    pass

# Error handlers
async def general_exception_handler(request, exc):
    logger.error("Unhandled exception", exc_info=exc, request=request.url)
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )
```

---

## ⚡ SPRINT 2: Segurança e Performance (Semana 3-4)

### 2.1 Rate Limiting

#### 📁 `app/core/rate_limit.py`
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)

# Rate limiting decorators
def rate_limit_user(max_calls: str):
    """Rate limit per user"""
    return limiter.limit(max_calls)

def rate_limit_ip(max_calls: str):
    """Rate limit per IP"""
    return limiter.limit(max_calls)

# Usage in routes:
@app.post("/auth/login")
@rate_limit_ip("5/minute")
async def login(request: Request, ...):
    pass

@app.post("/quizzes/")
@rate_limit_user("10/minute")
async def create_quiz(request: Request, ...):
    pass
```

### 2.2 Input Sanitization

#### 📁 `app/core/sanitizer.py`
```python
import re
import bleach
from typing import Any, Dict

def sanitize_text(text: str) -> str:
    """Sanitize text input"""
    if not text:
        return ""
    
    # Remove HTML tags
    clean_text = bleach.clean(text, tags=[], strip=True)
    
    # Limit length
    return clean_text[:5000]

def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize dictionary inputs"""
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_text(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        else:
            sanitized[key] = value
    return sanitized
```

### 2.3 Database Optimization

#### 📁 `app/db/optimizations.py`
```python
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import text

class OptimizedQueries:
    @staticmethod
    def get_user_with_plans(db, user_id):
        """Optimized query for user with study plans"""
        return db.query(User).options(
            selectinload(User.study_plans),
            selectinload(User.quizzes),
        ).filter(User.id == user_id).first()
    
    @staticmethod
    def get_quiz_with_questions(db, quiz_id):
        """Optimized query for quiz with questions"""
        return db.query(Quiz).options(
            selectinload(Quiz.questions)
        ).filter(Quiz.id == quiz_id).first()

# Database indexes (migration)
def add_performance_indexes():
    """Add indexes for better performance"""
    return [
        text("CREATE INDEX IF NOT EXISTS idx_quiz_user_id ON quizzes(user_id)"),
        text("CREATE INDEX IF NOT EXISTS idx_flashcard_user_id ON flashcards(user_id)"),
        text("CREATE INDEX IF NOT EXISTS idx_performance_user_date ON performance_records(user_id, date)"),
    ]
```

---

## 🔗 SPRINT 3: Integrações (Semana 5-6)

### 3.1 API Real de Questões

#### 📁 `app/integrations/qconcursos.py`
```python
import httpx
from typing import List, Dict
import asyncio

class QConcursosAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.qconcursos.com/v1"
        self.client = httpx.AsyncClient()
    
    async def fetch_questions(self, filters: Dict) -> List[Dict]:
        """Fetch real questions from QConcursos API"""
        try:
            response = await self.client.get(
                f"{self.base_url}/questions",
                params=filters,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json()["data"]
        except httpx.HTTPError as e:
            logger.error("QConcursos API error", error=str(e))
            return []
    
    async def get_question_by_id(self, question_id: str) -> Dict:
        """Get specific question"""
        response = await self.client.get(
            f"{self.base_url}/questions/{question_id}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()
```

### 3.2 Sistema de E-mail

#### 📁 `app/notifications/email.py`
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import asyncio
from typing import Dict, List

class EmailService:
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.template_env = Environment(loader=FileSystemLoader("templates/email"))
    
    async def send_study_reminder(self, user_email: str, user_name: str, study_data: Dict):
        """Send study reminder email"""
        template = self.template_env.get_template("study_reminder.html")
        html_content = template.render(
            user_name=user_name,
            study_data=study_data
        )
        
        await self._send_email(
            to_email=user_email,
            subject="📚 Lembrete de Estudo - Agente Concurseiro",
            html_content=html_content
        )
    
    async def _send_email(self, to_email: str, subject: str, html_content: str):
        """Send email via SMTP"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = to_email
        
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)
        
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
```

#### 📁 `templates/email/study_reminder.html`
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Lembrete de Estudo</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2c5282;">📚 Hora de Estudar, {{ user_name }}!</h2>
        
        <p>Você tem {{ study_data.pending_hours }}h de estudo pendentes hoje.</p>
        
        <div style="background: #f7fafc; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3>📋 Suas Atividades:</h3>
            <ul>
                {% for activity in study_data.activities %}
                <li>{{ activity.subject }} - {{ activity.duration }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <a href="{{ study_data.dashboard_url }}" 
           style="background: #2c5282; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
            Acessar Dashboard
        </a>
    </div>
</body>
</html>
```

### 3.3 Backup Automático

#### 📁 `app/backup/cloud_backup.py`
```python
import boto3
import schedule
import time
from datetime import datetime
import os
import subprocess

class CloudBackup:
    def __init__(self, aws_access_key: str, aws_secret_key: str, bucket_name: str):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        self.bucket_name = bucket_name
    
    def backup_database(self):
        """Create and upload database backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.sql"
        
        # Create database dump
        subprocess.run([
            "pg_dump",
            os.getenv("DATABASE_URL"),
            "-f", backup_filename
        ])
        
        # Upload to S3
        self.s3_client.upload_file(
            backup_filename,
            self.bucket_name,
            f"database_backups/{backup_filename}"
        )
        
        # Clean local file
        os.remove(backup_filename)
        
        logger.info("Database backup completed", filename=backup_filename)
    
    def schedule_backups(self):
        """Schedule automatic backups"""
        schedule.every().day.at("02:00").do(self.backup_database)
        schedule.every().week.do(self.backup_user_data)
        
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Check every hour
```

---

## 📊 SPRINT 4: Analytics Avançado (Semana 7-8)

### 4.1 Machine Learning Predictor

#### 📁 `app/ml/predictor.py`
```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from typing import Dict, List

class MLPerformancePredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def prepare_features(self, user_data: Dict) -> np.array:
        """Prepare features from user data"""
        features = [
            user_data.get('total_study_hours', 0),
            user_data.get('consistency_score', 0),
            user_data.get('current_streak', 0),
            user_data.get('quiz_average', 0),
            user_data.get('improvement_rate', 0),
            len(user_data.get('subjects_studied', [])),
            user_data.get('days_until_exam', 90) / 90,  # Normalize
        ]
        return np.array(features).reshape(1, -1)
    
    def train_model(self, training_data: List[Dict]):
        """Train the ML model"""
        if len(training_data) < 50:  # Need minimum data
            return False
        
        X = []
        y = []
        
        for data in training_data:
            features = self.prepare_features(data)
            X.append(features[0])
            y.append(data['final_score'])
        
        X = np.array(X)
        y = np.array(y)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        
        self.is_trained = True
        joblib.dump(self.model, 'ml_model.pkl')
        
        logger.info("ML model trained", accuracy=score)
        return True
    
    def predict_performance(self, user_data: Dict) -> Dict:
        """Predict user performance"""
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        features = self.prepare_features(user_data)
        prediction = self.model.predict(features)[0]
        confidence = self.model.predict_proba(features)[0].max() if hasattr(self.model, 'predict_proba') else 0.8
        
        return {
            "predicted_score": float(prediction),
            "confidence": float(confidence),
            "factors": self._get_important_factors(features)
        }
```

---

## 🔍 Checklist de Qualidade

### ✅ Antes de cada merge:
- [ ] Testes passando (coverage > 80%)
- [ ] Linting sem erros
- [ ] Documentação atualizada
- [ ] Logs estruturados adicionados
- [ ] Error handling implementado
- [ ] Performance testada

### ✅ Antes do deploy:
- [ ] Backup do banco realizado
- [ ] Health checks funcionando
- [ ] Monitoring configurado
- [ ] Rate limiting testado
- [ ] Rollback plan definido

---

**📝 Nota:** Estes TODOs são incrementais. Cada sprint constrói sobre o anterior. Priorize qualidade sobre velocidade.