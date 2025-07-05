"""
Modelos de banco de dados para o Agente Concurseiro
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    """Modelo de usuário"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    
    # Perfil do candidato
    target_exam = Column(String(255))
    target_position = Column(String(255))
    target_banca = Column(String(50))
    target_city = Column(String(100))
    education_level = Column(String(50))
    experience_level = Column(String(50), default="beginner")
    
    # Configurações de estudo
    weekly_study_hours = Column(Integer, default=20)
    study_months = Column(Integer, default=6)
    exam_date = Column(DateTime)
    
    # Configurações do sistema
    preferences = Column(JSON, default=dict)
    notification_settings = Column(JSON, default=dict)
    
    # Metadados
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime)
    
    # Relacionamentos
    study_plans = relationship("StudyPlan", back_populates="user")
    mock_exams = relationship("MockExam", back_populates="user")
    essays = relationship("Essay", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class StudyPlan(Base):
    """Plano de estudos do usuário"""
    __tablename__ = "study_plans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Configurações do plano
    name = Column(String(255), nullable=False)
    description = Column(Text)
    banca = Column(String(50), nullable=False)
    cargo = Column(String(255), nullable=False)
    total_weeks = Column(Integer, nullable=False)
    weekly_hours = Column(Integer, nullable=False)
    
    # Conteúdo do plano
    subjects = Column(JSON, nullable=False)  # Distribuição por matéria
    schedule = Column(JSON, nullable=False)  # Cronograma detalhado
    milestones = Column(JSON, default=list)  # Marcos importantes
    
    # Status
    is_active = Column(Boolean, default=True)
    progress_percentage = Column(Float, default=0.0)
    current_week = Column(Integer, default=1)
    
    # Metadados
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="study_plans")

class MockExam(Base):
    """Simulados realizados"""
    __tablename__ = "mock_exams"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Configurações do simulado
    banca = Column(String(50), nullable=False)
    subjects = Column(JSON, nullable=False)  # Lista de matérias
    difficulty = Column(String(20), default="medium")
    total_questions = Column(Integer, nullable=False)
    time_limit_minutes = Column(Integer)
    
    # Questões e respostas
    questions = Column(JSON, nullable=False)  # Lista de questões
    user_answers = Column(JSON, default=dict)  # Respostas do usuário
    
    # Resultados
    score = Column(Float)  # Pontuação final (0-100)
    correct_answers = Column(Integer, default=0)
    time_spent_minutes = Column(Integer)
    subject_scores = Column(JSON, default=dict)  # Pontuação por matéria
    
    # Status
    status = Column(String(20), default="created")  # created, in_progress, completed
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Metadados
    created_at = Column(DateTime, default=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="mock_exams")

class Essay(Base):
    """Redações avaliadas"""
    __tablename__ = "essays"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Configurações da redação
    banca = Column(String(50), nullable=False)
    essay_type = Column(String(50), nullable=False)
    theme = Column(String(500))
    
    # Conteúdo
    text = Column(Text, nullable=False)
    word_count = Column(Integer)
    
    # Avaliação
    final_score = Column(Float)  # Nota final (0-10)
    criterion_scores = Column(JSON, default=dict)  # Pontuação por critério
    feedback = Column(JSON, default=dict)  # Feedback detalhado
    strengths = Column(JSON, default=list)  # Pontos fortes
    weaknesses = Column(JSON, default=list)  # Pontos fracos
    suggestions = Column(JSON, default=list)  # Sugestões de melhoria
    
    # Metadados
    created_at = Column(DateTime, default=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="essays")

class Question(Base):
    """Banco de questões"""
    __tablename__ = "questions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Identificação
    external_id = Column(String(100), unique=True)  # ID da fonte externa
    source = Column(String(100))  # Fonte da questão
    
    # Conteúdo
    text = Column(Text, nullable=False)
    options = Column(JSON)  # Lista de opções para múltipla escolha
    correct_answer = Column(String(10), nullable=False)
    explanation = Column(Text)
    
    # Classificação
    subject = Column(String(100), nullable=False, index=True)
    topic = Column(String(200), index=True)
    subtopic = Column(String(200))
    difficulty = Column(String(20), default="medium", index=True)
    banca = Column(String(50), index=True)
    year = Column(Integer, index=True)
    exam_name = Column(String(200))
    position = Column(String(200))
    
    # Estatísticas
    times_used = Column(Integer, default=0)
    correct_rate = Column(Float)  # Taxa de acerto geral
    
    # Metadados
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UserAchievement(Base):
    """Conquistas dos usuários"""
    __tablename__ = "user_achievements"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Conquista
    achievement_id = Column(String(100), nullable=False)
    achievement_name = Column(String(255), nullable=False)
    achievement_description = Column(Text)
    achievement_icon = Column(String(50))
    points_earned = Column(Integer, default=0)
    category = Column(String(50))
    
    # Status
    is_earned = Column(Boolean, default=False)
    progress = Column(Float, default=0.0)
    max_progress = Column(Float, default=100.0)
    
    # Metadados
    earned_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="achievements")

class UserStats(Base):
    """Estatísticas do usuário"""
    __tablename__ = "user_stats"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Gamificação
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    
    # Estudos
    total_study_hours = Column(Float, default=0.0)
    current_streak = Column(Integer, default=0)
    max_streak = Column(Integer, default=0)
    study_days_count = Column(Integer, default=0)
    
    # Simulados
    mock_exams_completed = Column(Integer, default=0)
    best_mock_score = Column(Float, default=0.0)
    average_mock_score = Column(Float, default=0.0)
    
    # Redações
    essays_completed = Column(Integer, default=0)
    best_essay_score = Column(Float, default=0.0)
    average_essay_score = Column(Float, default=0.0)
    
    # Quiz diário
    daily_quizzes_completed = Column(Integer, default=0)
    quiz_streak = Column(Integer, default=0)
    
    # Conquistas
    achievements_earned = Column(Integer, default=0)
    badges_earned = Column(Integer, default=0)
    
    # Atividade
    last_activity = Column(DateTime)
    last_study_session = Column(DateTime)
    
    # Metadados
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Notification(Base):
    """Notificações do usuário"""
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Conteúdo
    type = Column(String(50), nullable=False)
    priority = Column(String(20), default="medium")
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Ação
    action_text = Column(String(100))
    action_url = Column(String(500))
    
    # Status
    is_read = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    
    # Agendamento
    scheduled_for = Column(DateTime)
    
    # Metadados
    extra_metadata = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    read_at = Column(DateTime)
    
    # Relacionamentos
    user = relationship("User", back_populates="notifications")

class SystemConfig(Base):
    """Configurações do sistema"""
    __tablename__ = "system_config"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Configuração
    key = Column(String(100), unique=True, nullable=False)
    value = Column(JSON, nullable=False)
    description = Column(Text)
    category = Column(String(50), default="general")
    
    # Metadados
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AuditLog(Base):
    """Log de auditoria"""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Evento
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String)
    
    # Detalhes
    details = Column(JSON, default=dict)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Metadados
    timestamp = Column(DateTime, default=func.now())
    
    # Configurações da tabela
    __table_args__ = (
        {'mysql_engine': 'InnoDB'} if os.getenv('DATABASE_URL', '').startswith('mysql') else {}
    )
