from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Notification(Base):
    """Modelo para notificações in-app"""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # study_reminder, achievement, etc.
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)  # Dados adicionais da notificação
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    read = Column(Boolean, default=False, index=True)
    sent_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamento com usuário
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, type='{self.type}', user_id={self.user_id}, read={self.read})>"

    def mark_as_read(self):
        """Marca notificação como lida"""
        self.read = True
        self.read_at = datetime.utcnow()

    def to_dict(self):
        """Converte para dicionário"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "title": self.title,
            "message": self.message,
            "data": self.data,
            "priority": self.priority,
            "read": self.read,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class NotificationPreference(Base):
    """Modelo para preferências de notificação do usuário"""

    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Canais habilitados
    email_enabled = Column(Boolean, default=True)
    push_enabled = Column(Boolean, default=False)
    in_app_enabled = Column(Boolean, default=True)

    # Frequência de emails
    email_frequency = Column(String(20), default="daily")  # immediate, daily, weekly

    # Horário silencioso
    quiet_hours_enabled = Column(Boolean, default=True)
    quiet_hours_start = Column(String(5), default="22:00")  # HH:MM
    quiet_hours_end = Column(String(5), default="08:00")    # HH:MM

    # Tipos de notificação habilitados
    study_reminders_enabled = Column(Boolean, default=True)
    exam_reminders_enabled = Column(Boolean, default=True)
    achievements_enabled = Column(Boolean, default=True)
    performance_updates_enabled = Column(Boolean, default=True)
    system_alerts_enabled = Column(Boolean, default=True)

    # Configurações específicas
    study_reminder_time = Column(String(5), default="09:00")  # Horário do lembrete de estudo
    max_daily_notifications = Column(Integer, default=5)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com usuário
    user = relationship("User", back_populates="notification_preferences")

    def __repr__(self):
        return f"<NotificationPreference(user_id={self.user_id}, email_enabled={self.email_enabled})>"

    def get_enabled_channels(self) -> list:
        """Retorna lista de canais habilitados"""
        channels = []
        if self.email_enabled:
            channels.append("email")
        if self.push_enabled:
            channels.append("push")
        if self.in_app_enabled:
            channels.append("in_app")
        return channels

    def is_quiet_hours(self, current_time: datetime = None) -> bool:
        """Verifica se está no horário silencioso"""
        if not self.quiet_hours_enabled:
            return False

        if current_time is None:
            current_time = datetime.now()

        current_time_str = current_time.strftime("%H:%M")

        # Converter horários para minutos para facilitar comparação
        def time_to_minutes(time_str):
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes

        current_minutes = time_to_minutes(current_time_str)
        start_minutes = time_to_minutes(self.quiet_hours_start)
        end_minutes = time_to_minutes(self.quiet_hours_end)

        # Se o horário silencioso cruza a meia-noite
        if start_minutes > end_minutes:
            return current_minutes >= start_minutes or current_minutes <= end_minutes
        else:
            return start_minutes <= current_minutes <= end_minutes

    def to_dict(self):
        """Converte para dicionário"""
        return {
            "user_id": self.user_id,
            "email_enabled": self.email_enabled,
            "push_enabled": self.push_enabled,
            "in_app_enabled": self.in_app_enabled,
            "email_frequency": self.email_frequency,
            "quiet_hours_enabled": self.quiet_hours_enabled,
            "quiet_hours_start": self.quiet_hours_start,
            "quiet_hours_end": self.quiet_hours_end,
            "study_reminders_enabled": self.study_reminders_enabled,
            "exam_reminders_enabled": self.exam_reminders_enabled,
            "achievements_enabled": self.achievements_enabled,
            "performance_updates_enabled": self.performance_updates_enabled,
            "system_alerts_enabled": self.system_alerts_enabled,
            "study_reminder_time": self.study_reminder_time,
            "max_daily_notifications": self.max_daily_notifications,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class ScheduledNotification(Base):
    """Modelo para notificações agendadas"""

    __tablename__ = "scheduled_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    notification_type = Column(String(50), nullable=False)
    data = Column(JSON, nullable=True)
    channels = Column(JSON, nullable=True)  # Lista de canais
    scheduled_time = Column(DateTime, nullable=False, index=True)
    sent = Column(Boolean, default=False, index=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamento com usuário
    user = relationship("User", back_populates="scheduled_notifications")

    def __repr__(self):
        return f"<ScheduledNotification(id={self.id}, user_id={self.user_id}, scheduled_time='{self.scheduled_time}')>"

    def mark_as_sent(self):
        """Marca notificação como enviada"""
        self.sent = True
        self.sent_at = datetime.utcnow()

    def to_dict(self):
        """Converte para dicionário"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "notification_type": self.notification_type,
            "data": self.data,
            "channels": self.channels,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "sent": self.sent,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
