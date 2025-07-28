from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class LogEntry(Base):
    """Modelo para armazenar logs no banco de dados"""

    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    level = Column(String(10), nullable=False, index=True)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    module = Column(String(100), nullable=False)
    function = Column(String(100), nullable=False)
    line = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    logger = Column(String(100), nullable=False)

    # Campos opcionais para contexto adicional
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    request_id = Column(String(100), nullable=True, index=True)
    operation = Column(String(200), nullable=True, index=True)
    duration = Column(Float, nullable=True)  # Duração em segundos

    # Relacionamento com usuário
    user = relationship("User", back_populates="logs")

    def __repr__(self):
        return f"<LogEntry(id={self.id}, level='{self.level}', module='{self.module}', timestamp='{self.timestamp}')>"

    @classmethod
    def create_from_record(cls, record, db_session):
        """Cria uma entrada de log a partir de um record de logging"""
        log_entry = cls(
            timestamp=datetime.fromtimestamp(record.created),
            level=record.levelname,
            module=record.module,
            function=record.funcName,
            line=record.lineno,
            message=record.getMessage(),
            logger=record.name
        )

        # Adicionar campos extras se existirem
        if hasattr(record, 'user_id'):
            log_entry.user_id = record.user_id
        if hasattr(record, 'request_id'):
            log_entry.request_id = record.request_id
        if hasattr(record, 'operation'):
            log_entry.operation = record.operation
        if hasattr(record, 'duration'):
            log_entry.duration = record.duration

        db_session.add(log_entry)
        db_session.commit()

        return log_entry
