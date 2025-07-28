# 🚀 Sprint de Implementação - Agente Concurseiro v2.0

**Duração:** 2 semanas (10 dias úteis)  
**Objetivo:** Estabilizar sistema para produção  
**Status atual:** 85% implementado  

---

## 📋 Sprint Backlog

### 🎯 **Objetivo Principal**
Transformar o sistema de 85% para 95% de implementação, focando em **estabilidade, testes e segurança** para lançamento em produção.

### 📊 **Métricas de Sucesso**
- [ ] Cobertura de testes: 80%+
- [ ] Zero vulnerabilidades críticas
- [ ] Tempo de resposta API < 200ms
- [ ] Sistema de logging estruturado
- [ ] Error handling robusto

---

## 📅 Cronograma Detalhado

### **SEMANA 1: Fundação e Estabilidade**

#### **Dia 1-2: Sistema de Testes (CRÍTICO)**
**Story Points:** 8  
**Responsável:** Desenvolvedor Backend  

**Tarefas:**
- [ ] **Setup de ambiente de testes**
  ```bash
  # Criar estrutura de testes
  mkdir -p tests/{unit,integration,e2e}
  touch tests/__init__.py
  ```

- [ ] **Testes unitários para Tools principais**
  ```python
  # tests/tools/test_writing_tool.py
  def test_writing_tool_evaluation():
      tool = WritingTool()
      result = tool.evaluate_essay_by_banca(essay_text, "CESPE")
      assert result["score_final"] > 0
      assert "error" not in result
  ```

- [ ] **Testes para agentes CrewAI**
  ```python
  # tests/agents/test_crew_integration.py
  def test_crew_complete_workflow():
      result = run_crew("Analista", "TRF", "CESPE", "Brasília", 20, 6)
      assert all(key in result for key in ["exam_data", "study_plan"])
  ```

- [ ] **Testes de API endpoints**
  ```python
  # tests/api/test_endpoints.py
  def test_create_study_plan_endpoint():
      response = client.post("/study-plans", json=plan_data)
      assert response.status_code == 201
  ```

**Entregáveis:**
- ✅ 80% cobertura de testes
- ✅ Pipeline de CI configurado
- ✅ Relatório de cobertura

#### **Dia 3-4: Logging e Error Handling**
**Story Points:** 6  
**Responsável:** Desenvolvedor Backend  

**Tarefas:**
- [ ] **Sistema de logging estruturado**
  ```python
  # app/core/logger.py
  import structlog
  import logging
  from datetime import datetime
  
  def setup_logging():
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
  ```

- [ ] **Error handlers personalizados**
  ```python
  # app/core/exceptions.py
  class AgenteConcurseiroException(Exception):
      """Exceção base do sistema"""
      def __init__(self, message, error_code=None, details=None):
          super().__init__(message)
          self.error_code = error_code
          self.details = details or {}
  
  class ValidationError(AgenteConcurseiroException):
      """Erro de validação de dados"""
      pass
  
  class AuthenticationError(AgenteConcurseiroException):
      """Erro de autenticação"""
      pass
  ```

- [ ] **Middleware de tratamento de erros**
  ```python
  # app/core/error_handlers.py
  from fastapi import Request, status
  from fastapi.responses import JSONResponse
  
  async def agente_exception_handler(request: Request, exc: AgenteConcurseiroException):
      return JSONResponse(
          status_code=status.HTTP_400_BAD_REQUEST,
          content={
              "error": str(exc),
              "error_code": exc.error_code,
              "details": exc.details,
              "timestamp": datetime.utcnow().isoformat()
          }
      )
  ```

**Entregáveis:**
- ✅ Logs estruturados em JSON
- ✅ Error handling consistente
- ✅ Monitoramento de erros

#### **Dia 5: Segurança Avançada**
**Story Points:** 5  
**Responsável:** Desenvolvedor Backend  

**Tarefas:**
- [ ] **Rate limiting por usuário**
  ```python
  # app/core/rate_limit.py
  from slowapi import Limiter, _rate_limit_exceeded_handler
  from slowapi.util import get_remote_address
  from slowapi.errors import RateLimitExceeded
  
  limiter = Limiter(key_func=get_remote_address)
  
  @app.middleware("http")
  async def rate_limit_middleware(request: Request, call_next):
      # Rate limit por endpoint
      if request.url.path.startswith("/api/"):
          await limiter.check_request_limit(request)
      return await call_next(request)
  ```

- [ ] **Sanitização de inputs**
  ```python
  # app/core/sanitizer.py
  import bleach
  from html import escape
  
  def sanitize_text(text: str) -> str:
      """Remove HTML e scripts maliciosos"""
      return bleach.clean(text, strip=True)
  
  def sanitize_json(data: dict) -> dict:
      """Sanitiza dados JSON"""
      return {k: sanitize_text(str(v)) if isinstance(v, str) else v 
              for k, v in data.items()}
  ```

- [ ] **Logs de auditoria**
  ```python
  # app/core/audit.py
  class AuditLogger:
      def log_user_action(self, user_id: str, action: str, resource: str, details: dict):
          logger.info("User action", 
                     user_id=user_id, 
                     action=action, 
                     resource=resource, 
                     details=details)
  ```

**Entregáveis:**
- ✅ Rate limiting configurado
- ✅ Sanitização de inputs
- ✅ Logs de auditoria

### **SEMANA 2: Integrações e Polimento**

#### **Dia 6-7: API Real de Questões**
**Story Points:** 7  
**Responsável:** Desenvolvedor Backend  

**Tarefas:**
- [ ] **Integração com QConcursos API**
  ```python
  # app/integrations/qconcursos.py
  import httpx
  from typing import List, Dict
  
  class QConcursosAPI:
      def __init__(self, api_key: str):
          self.api_key = api_key
          self.base_url = "https://api.qconcursos.com"
          self.client = httpx.AsyncClient()
      
      async def fetch_questions(self, filters: Dict) -> List[Dict]:
          """Busca questões reais da API"""
          params = {
              "api_key": self.api_key,
              **filters
          }
          response = await self.client.get(f"{self.base_url}/questions", params=params)
          return response.json()
      
      async def get_question_details(self, question_id: str) -> Dict:
          """Obtém detalhes de uma questão específica"""
          response = await self.client.get(f"{self.base_url}/questions/{question_id}")
          return response.json()
  ```

- [ ] **Cache inteligente de questões**
  ```python
  # app/core/cache.py
  import redis
  import json
  from datetime import timedelta
  
  class QuestionCache:
      def __init__(self):
          self.redis = redis.Redis(host='localhost', port=6379, db=0)
      
      def get_cached_questions(self, cache_key: str) -> List[Dict]:
          """Busca questões no cache"""
          cached = self.redis.get(cache_key)
          return json.loads(cached) if cached else None
      
      def cache_questions(self, cache_key: str, questions: List[Dict], ttl: int = 3600):
          """Armazena questões no cache"""
          self.redis.setex(cache_key, ttl, json.dumps(questions))
  ```

- [ ] **Sincronização automática**
  ```python
  # app/tasks/sync_questions.py
  from celery import Celery
  
  celery_app = Celery('agente_concurseiro')
  
  @celery_app.task
  def sync_questions_from_api():
      """Sincroniza questões da API externa"""
      api = QConcursosAPI(settings.QCONCURSOS_API_KEY)
      cache = QuestionCache()
      
      # Buscar questões por matéria
      for subject in ["portugues", "matematica", "direito"]:
          questions = api.fetch_questions({"subject": subject, "limit": 100})
          cache.cache_questions(f"questions_{subject}", questions)
  ```

**Entregáveis:**
- ✅ Integração com API real
- ✅ Sistema de cache
- ✅ Sincronização automática

#### **Dia 8-9: Sistema de Notificações**
**Story Points:** 6  
**Responsável:** Desenvolvedor Full-Stack  

**Tarefas:**
- [ ] **E-mail com templates HTML**
  ```python
  # app/notifications/email.py
  from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
  from jinja2 import Environment, FileSystemLoader
  
  class EmailService:
      def __init__(self):
          self.conf = ConnectionConfig(
              MAIL_USERNAME=settings.SMTP_USER,
              MAIL_PASSWORD=settings.SMTP_PASSWORD,
              MAIL_FROM=settings.SMTP_FROM,
              MAIL_PORT=settings.SMTP_PORT,
              MAIL_SERVER=settings.SMTP_SERVER,
              MAIL_TLS=True,
              MAIL_SSL=False,
              USE_CREDENTIALS=True
          )
          self.fastmail = FastMail(self.conf)
          self.template_env = Environment(loader=FileSystemLoader('templates/email'))
      
      async def send_study_reminder(self, user_email: str, user_name: str, study_data: dict):
          """Envia lembrete de estudo personalizado"""
          template = self.template_env.get_template('study_reminder.html')
          html_content = template.render(
              user_name=user_name,
              study_hours=study_data.get('hours', 0),
              next_session=study_data.get('next_session'),
              streak=study_data.get('streak', 0)
          )
          
          message = MessageSchema(
              subject="📚 Lembrete de Estudo - Agente Concurseiro",
              recipients=[user_email],
              body=html_content,
              subtype="html"
          )
          
          await self.fastmail.send_message(message)
  ```

- [ ] **Templates HTML responsivos**
  ```html
  <!-- templates/email/study_reminder.html -->
  <!DOCTYPE html>
  <html>
  <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Lembrete de Estudo</title>
  </head>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
          <h1 style="color: #2c3e50;">📚 Olá, {{ user_name }}!</h1>
          <p>É hora de continuar sua jornada de estudos!</p>
          
          <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3>📊 Seu Progresso</h3>
              <p><strong>Sequência atual:</strong> {{ streak }} dias</p>
              <p><strong>Horas estudadas hoje:</strong> {{ study_hours }}h</p>
              <p><strong>Próxima sessão:</strong> {{ next_session }}</p>
          </div>
          
          <a href="{{ study_url }}" style="background: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
              🚀 Continuar Estudando
          </a>
      </div>
  </body>
  </html>
  ```

- [ ] **Scheduler para lembretes automáticos**
  ```python
  # app/tasks/notifications.py
  from celery import Celery
  from app.notifications.email import EmailService
  
  @celery_app.task
  def send_daily_reminders():
      """Envia lembretes diários para todos os usuários ativos"""
      email_service = EmailService()
      
      # Buscar usuários ativos
      active_users = get_active_users()
      
      for user in active_users:
          study_data = get_user_study_data(user.id)
          if should_send_reminder(user, study_data):
              email_service.send_study_reminder(
                  user.email, 
                  user.full_name, 
                  study_data
              )
  ```

**Entregáveis:**
- ✅ Sistema de e-mail funcional
- ✅ Templates HTML responsivos
- ✅ Scheduler automático

#### **Dia 10: Backup e Monitoramento**
**Story Points:** 4  
**Responsável:** DevOps  

**Tarefas:**
- [ ] **Backup automático para cloud**
  ```python
  # app/backup/cloud_backup.py
  import boto3
  from datetime import datetime
  import os
  
  class CloudBackup:
      def __init__(self):
          self.s3 = boto3.client('s3')
          self.bucket_name = settings.BACKUP_BUCKET
      
      def backup_database(self):
          """Faz backup do banco para S3"""
          timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
          backup_file = f"backup_{timestamp}.sql"
          
          # Criar dump do banco
          os.system(f"pg_dump {settings.DATABASE_URL} > {backup_file}")
          
          # Upload para S3
          self.s3.upload_file(
              backup_file, 
              self.bucket_name, 
              f"database/{backup_file}"
          )
          
          # Limpar arquivo local
          os.remove(backup_file)
  ```

- [ ] **Monitoramento de saúde**
  ```python
  # app/monitoring/health.py
  from fastapi import APIRouter
  import psutil
  import redis
  
  router = APIRouter()
  
  @router.get("/health")
  async def health_check():
      """Verifica saúde de todos os componentes"""
      checks = {
          "database": check_database_health(),
          "redis": check_redis_health(),
          "disk_space": check_disk_space(),
          "memory_usage": check_memory_usage(),
          "agents": check_agents_health()
      }
      
      all_healthy = all(checks.values())
      return {
          "status": "healthy" if all_healthy else "unhealthy",
          "checks": checks,
          "timestamp": datetime.utcnow().isoformat()
      }
  ```

**Entregáveis:**
- ✅ Backup automático na nuvem
- ✅ Sistema de monitoramento
- ✅ Health checks completos

---

## 🛠️ Configuração de CI/CD

### **GitHub Actions Workflow**
```yaml
# .github/workflows/ci.yml
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
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-prod.txt
        pip install pytest pytest-cov pytest-asyncio
    
    - name: Run tests
      run: |
        pytest tests/ --cov=app --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
    
    - name: Security scan
      run: |
        pip install bandit safety
        bandit -r app/ -f json -o bandit-report.json
        safety check

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Adicionar comandos de deploy
```

---

## 📊 Métricas de Acompanhamento

### **Daily Standup Checklist**
- [ ] Testes passando (100%)
- [ ] Cobertura de código > 80%
- [ ] Zero vulnerabilidades críticas
- [ ] Logs estruturados funcionando
- [ ] Rate limiting ativo
- [ ] Backup automático executado

### **Sprint Review Checklist**
- [ ] Todas as tarefas completadas
- [ ] Documentação atualizada
- [ ] Testes de integração passando
- [ ] Performance dentro do esperado
- [ ] Segurança validada
- [ ] Deploy em staging funcionando

---

## 🚨 Riscos e Mitigações

### **Riscos Identificados**
1. **API externa indisponível** → Cache local + fallback
2. **Problemas de performance** → Monitoramento + otimizações
3. **Falhas de segurança** → Auditoria + testes de penetração

### **Plano de Contingência**
- Backup de dados críticos
- Rollback automático em caso de falha
- Monitoramento 24/7
- Equipe de suporte escalável

---

## 🎯 Definição de Pronto (DoD)

### **Para cada tarefa:**
- [ ] Código implementado e testado
- [ ] Testes unitários escritos
- [ ] Documentação atualizada
- [ ] Code review aprovado
- [ ] Integração com CI/CD

### **Para o Sprint:**
- [ ] 80%+ cobertura de testes
- [ ] Zero bugs críticos
- [ ] Performance validada
- [ ] Segurança auditada
- [ ] Deploy em produção funcionando

---

## 📈 Próximos Passos Pós-Sprint

### **Sprint 2 (Semana 3-4):**
- Analytics avançado com ML
- A/B testing framework
- Otimizações de performance
- UX/UI melhorias

### **Sprint 3 (Semana 5-6):**
- Integrações externas (calendários)
- PWA (Progressive Web App)
- Funcionalidades avançadas
- Lançamento beta

---

**🎯 Objetivo Final:** Sistema 95% implementado, estável e pronto para produção com qualidade enterprise. 