import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.core.config import settings


class CustomFormatter(logging.Formatter):
    """Formatador personalizado para logs com cores e estrutura melhorada"""

    # Cores ANSI para terminal
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record):
        # Adicionar timestamp personalizado
        record.timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')

        # Adicionar informações extras
        record.module_info = f"{record.module}:{record.funcName}:{record.lineno}"

        # Formato base
        log_format = (
            "%(timestamp)s | %(levelname)-8s | %(module_info)-30s | %(message)s"
        )

        # Adicionar cores se estiver no terminal
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            log_format = f"{color}{log_format}{self.COLORS['RESET']}"

        formatter = logging.Formatter(log_format)
        return formatter.format(record)

class StructuredFormatter(logging.Formatter):
    """Formatador estruturado para logs JSON"""

    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
            'logger': record.name
        }

        # Adicionar campos extras se existirem
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'operation'):
            log_entry['operation'] = record.operation
        if hasattr(record, 'duration'):
            log_entry['duration'] = record.duration

        # Adicionar exceção se existir
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        return log_entry

class DatabaseHandler(logging.Handler):
    """Handler para salvar logs no banco de dados"""

    def __init__(self, db_session_factory):
        super().__init__()
        self.db_session_factory = db_session_factory

    def emit(self, record):
        try:
            from app.db.models import AuditLog as LogEntry

            with self.db_session_factory() as session:
                log_entry = LogEntry(
                    timestamp=datetime.fromtimestamp(record.created),
                    level=record.levelname,
                    module=record.module,
                    function=record.funcName,
                    line=record.lineno,
                    message=record.getMessage(),
                    logger=record.name
                )

                # Adicionar campos extras
                if hasattr(record, 'user_id'):
                    log_entry.user_id = record.user_id
                if hasattr(record, 'request_id'):
                    log_entry.request_id = record.request_id
                if hasattr(record, 'operation'):
                    log_entry.operation = record.operation
                if hasattr(record, 'duration'):
                    log_entry.duration = record.duration

                session.add(log_entry)
                session.commit()

        except Exception as e:
            # Fallback para console se falhar
            sys.stderr.write(f"Erro ao salvar log no banco: {e}\n")

def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    enable_database_logging: bool = False,
    db_session_factory = None
) -> logging.Logger:
    """
    Configura o sistema de logging
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Caminho para arquivo de log
        max_bytes: Tamanho máximo do arquivo de log
        backup_count: Número de backups a manter
        enable_database_logging: Se deve salvar logs no banco de dados
        db_session_factory: Factory para sessões do banco de dados
    """

    # Criar diretório de logs se não existir
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configurar logger raiz
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Limpar handlers existentes
    logger.handlers.clear()

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    # Handler para arquivo (se especificado)
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)

    # Handler para banco de dados (se habilitado)
    if enable_database_logging and db_session_factory:
        db_handler = DatabaseHandler(db_session_factory)
        db_handler.setLevel(logging.INFO)  # Apenas INFO e acima para o banco
        db_handler.setFormatter(StructuredFormatter())
        logger.addHandler(db_handler)

    # Configurar loggers específicos
    setup_specific_loggers(log_level)

    return logger

def setup_specific_loggers(log_level: str):
    """Configura loggers específicos para diferentes módulos"""

    # Logger para API
    api_logger = logging.getLogger("app.api")
    api_logger.setLevel(getattr(logging, log_level.upper()))

    # Logger para agentes
    agents_logger = logging.getLogger("app.agents")
    agents_logger.setLevel(getattr(logging, log_level.upper()))

    # Logger para banco de dados
    db_logger = logging.getLogger("app.db")
    db_logger.setLevel(getattr(logging, log_level.upper()))

    # Logger para ferramentas
    tools_logger = logging.getLogger("tools")
    tools_logger.setLevel(getattr(logging, log_level.upper()))

    # Logger para CrewAI
    crewai_logger = logging.getLogger("crewai")
    crewai_logger.setLevel(logging.WARNING)  # Reduzir verbosidade do CrewAI

    # Logger para SQLAlchemy
    sqlalchemy_logger = logging.getLogger("sqlalchemy")
    sqlalchemy_logger.setLevel(logging.WARNING)  # Reduzir logs SQL

    # Logger para FastAPI
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(getattr(logging, log_level.upper()))

    # Logger para Uvicorn
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(getattr(logging, log_level.upper()))

def get_logger(name: str) -> logging.Logger:
    """Obtém um logger configurado"""
    return logging.getLogger(name)

def log_user_activity(logger: logging.Logger, user_id: int, operation: str,
                     details: str = "", duration: float = None):
    """Log específico para atividades do usuário"""
    extra = {
        'user_id': user_id,
        'operation': operation,
        'duration': duration
    }
    logger.info(f"User activity: {operation} - {details}", extra=extra)

def log_api_request(logger: logging.Logger, method: str, path: str,
                   status_code: int, duration: float, user_id: int = None,
                   request_id: str = None):
    """Log específico para requisições da API"""
    extra = {
        'user_id': user_id,
        'request_id': request_id,
        'operation': f"{method} {path}",
        'duration': duration
    }

    level = logging.INFO if status_code < 400 else logging.WARNING
    logger.log(level, f"API Request: {method} {path} - {status_code} ({duration:.3f}s)", extra=extra)

def log_agent_execution(logger: logging.Logger, agent_name: str, task: str,
                       duration: float, success: bool, error: str = None):
    """Log específico para execução de agentes"""
    extra = {
        'operation': f"{agent_name}:{task}",
        'duration': duration
    }

    if success:
        logger.info(f"Agent execution: {agent_name} - {task} completed ({duration:.3f}s)", extra=extra)
    else:
        logger.error(f"Agent execution: {agent_name} - {task} failed: {error} ({duration:.3f}s)", extra=extra)

def log_database_operation(logger: logging.Logger, operation: str, table: str,
                          duration: float, success: bool, error: str = None):
    """Log específico para operações de banco de dados"""
    extra = {
        'operation': f"DB:{operation}:{table}",
        'duration': duration
    }

    if success:
        logger.debug(f"Database operation: {operation} on {table} ({duration:.3f}s)", extra=extra)
    else:
        logger.error(f"Database operation: {operation} on {table} failed: {error} ({duration:.3f}s)", extra=extra)

def log_security_event(logger: logging.Logger, event_type: str, user_id: int = None,
                      ip_address: str = None, details: str = ""):
    """Log específico para eventos de segurança"""
    extra = {
        'user_id': user_id,
        'operation': f"SECURITY:{event_type}"
    }

    message = f"Security event: {event_type}"
    if ip_address:
        message += f" from {ip_address}"
    if details:
        message += f" - {details}"

    logger.warning(message, extra=extra)

def log_performance_metric(logger: logging.Logger, metric_name: str, value: float,
                          unit: str = "", context: str = ""):
    """Log específico para métricas de performance"""
    extra = {
        'operation': f"PERFORMANCE:{metric_name}",
        'duration': value
    }

    message = f"Performance metric: {metric_name} = {value}"
    if unit:
        message += f" {unit}"
    if context:
        message += f" ({context})"

    logger.info(message, extra=extra)

# Configuração inicial do logging
def initialize_logging():
    """Inicializa o sistema de logging com configurações padrão"""

    # Determinar nível de log baseado no ambiente
    log_level = os.getenv("LOG_LEVEL", "INFO")

    # Determinar arquivo de log
    log_file = None
    if settings.ENVIRONMENT == "production":
        log_file = "logs/app.log"
    elif settings.ENVIRONMENT == "development":
        log_file = "logs/dev.log"

    # Configurar logging
    setup_logging(
        log_level=log_level,
        log_file=log_file,
        enable_database_logging=settings.ENVIRONMENT == "production"
    )

    logger = get_logger(__name__)
    logger.info("Logging system initialized - Level: %s, Environment: %s", log_level, settings.ENVIRONMENT)

    return logger

# Logger global
logger = initialize_logging()
