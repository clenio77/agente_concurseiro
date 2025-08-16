import logging
import traceback
from typing import Any, Dict

from fastapi import HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.core.logger import get_logger

logger = get_logger(__name__)

class AgenteConcurseiroException(Exception):
    """Exceção base para todas as exceções do Agente Concurseiro"""

    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code or "GENERAL_ERROR"
        self.details = details or {}
        super().__init__(self.message)

class AuthenticationError(AgenteConcurseiroException):
    """Exceção para erros de autenticação"""

    def __init__(self, message: str = "Erro de autenticação", details: Dict[str, Any] = None):
        super().__init__(message, "AUTH_ERROR", details)

class AuthorizationError(AgenteConcurseiroException):
    """Exceção para erros de autorização"""

    def __init__(self, message: str = "Acesso negado", details: Dict[str, Any] = None):
        super().__init__(message, "AUTHORIZATION_ERROR", details)

class ValidationError(AgenteConcurseiroException):
    """Exceção para erros de validação"""

    def __init__(self, message: str = "Dados inválidos", field: str = None, details: Dict[str, Any] = None):
        if field:
            message = f"Campo '{field}': {message}"
        super().__init__(message, "VALIDATION_ERROR", details)

class DatabaseError(AgenteConcurseiroException):
    """Exceção para erros de banco de dados"""

    def __init__(self, message: str = "Erro no banco de dados", operation: str = None, details: Dict[str, Any] = None):
        if operation:
            message = f"Erro na operação '{operation}': {message}"
        super().__init__(message, "DATABASE_ERROR", details)

class ExternalServiceError(AgenteConcurseiroException):
    """Exceção para erros de serviços externos"""

    def __init__(self, service: str, message: str = "Erro no serviço externo", details: Dict[str, Any] = None):
        message = f"Erro no serviço '{service}': {message}"
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", details)

class AIAgentError(AgenteConcurseiroException):
    """Exceção para erros dos agentes de IA"""

    def __init__(self, agent: str, task: str, message: str = "Erro no agente de IA", details: Dict[str, Any] = None):
        message = f"Erro no agente '{agent}' na tarefa '{task}': {message}"
        super().__init__(message, "AI_AGENT_ERROR", details)

class ResourceNotFoundError(AgenteConcurseiroException):
    """Exceção para recursos não encontrados"""

    def __init__(self, resource_type: str, resource_id: Any, details: Dict[str, Any] = None):
        message = f"{resource_type} com ID '{resource_id}' não encontrado"
        super().__init__(message, "RESOURCE_NOT_FOUND", details)

class RateLimitError(AgenteConcurseiroException):
    """Exceção para limites de taxa excedidos"""

    def __init__(self, service: str = None, retry_after: int = None, details: Dict[str, Any] = None):
        message = "Limite de taxa excedido"
        if service:
            message += f" para o serviço '{service}'"
        super().__init__(message, "RATE_LIMIT_ERROR", details)

class ConfigurationError(AgenteConcurseiroException):
    """Exceção para erros de configuração"""

    def __init__(self, config_key: str = None, message: str = "Erro de configuração", details: Dict[str, Any] = None):
        if config_key:
            message = f"Erro na configuração '{config_key}': {message}"
        super().__init__(message, "CONFIGURATION_ERROR", details)

class BusinessLogicError(AgenteConcurseiroException):
    """Exceção para erros de lógica de negócio"""

    def __init__(self, operation: str, message: str = "Erro na lógica de negócio", details: Dict[str, Any] = None):
        message = f"Erro na operação '{operation}': {message}"
        super().__init__(message, "BUSINESS_LOGIC_ERROR", details)

def handle_agente_concurseiro_exception(request: Request, exc: AgenteConcurseiroException) -> JSONResponse:
    """Handler para exceções personalizadas do Agente Concurseiro"""

    # Determinar status HTTP baseado no tipo de exceção
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    if isinstance(exc, AuthenticationError):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, AuthorizationError):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(exc, ValidationError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif isinstance(exc, ResourceNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, RateLimitError):
        status_code = status.HTTP_429_TOO_MANY_REQUESTS
    elif isinstance(exc, ConfigurationError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif isinstance(exc, BusinessLogicError):
        status_code = status.HTTP_400_BAD_REQUEST

    # Log do erro
    logger.error(
        f"AgenteConcurseiroException: {exc.error_code} - {exc.message}",
        extra={
            'error_code': exc.error_code,
            'details': exc.details,
            'path': request.url.path,
            'method': request.method
        }
    )

    # Construir resposta de erro
    error_response = {
        "error": {
            "code": exc.error_code,
            "message": exc.message,
            "details": exc.details
        },
        "timestamp": request.state.start_time.isoformat() if hasattr(request.state, 'start_time') else None,
        "path": request.url.path,
        "method": request.method
    }

    return JSONResponse(
        status_code=status_code,
        content=error_response
    )

def handle_general_exception(request: Request, exc: Exception) -> JSONResponse:
    """Handler para exceções gerais não tratadas"""

    # Log do erro com stack trace
    logger.error(
        f"Unhandled exception: {type(exc).__name__} - {str(exc)}",
        extra={
            'exception_type': type(exc).__name__,
            'stack_trace': traceback.format_exc(),
            'path': request.url.path,
            'method': request.method
        }
    )

    # Em produção, não expor detalhes internos
    if hasattr(request.app.state, 'environment') and request.app.state.environment == "production":
        message = "Erro interno do servidor"
        details = None
    else:
        message = str(exc)
        details = {
            "exception_type": type(exc).__name__,
            "stack_trace": traceback.format_exc()
        }

    error_response = {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": message,
            "details": details
        },
        "timestamp": request.state.start_time.isoformat() if hasattr(request.state, 'start_time') else None,
        "path": request.url.path,
        "method": request.method
    }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )

def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """Handler para exceções HTTP do FastAPI"""

    # Log do erro
    logger.warning(
        f"HTTPException: {exc.status_code} - {exc.detail}",
        extra={
            'status_code': exc.status_code,
            'path': request.url.path,
            'method': request.method
        }
    )

    error_response = {
        "error": {
            "code": f"HTTP_{exc.status_code}",
            "message": exc.detail,
            "details": None
        },
        "timestamp": request.state.start_time.isoformat() if hasattr(request.state, 'start_time') else None,
        "path": request.url.path,
        "method": request.method
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )

def handle_validation_exception(request: Request, exc: Exception) -> JSONResponse:
    """Handler para exceções de validação do Pydantic"""

    # Log do erro
    logger.warning(
        f"ValidationError: {str(exc)}",
        extra={
            'path': request.url.path,
            'method': request.method
        }
    )

    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Dados de entrada inválidos",
            "details": {
                "validation_errors": str(exc)
            }
        },
        "timestamp": request.state.start_time.isoformat() if hasattr(request.state, 'start_time') else None,
        "path": request.url.path,
        "method": request.method
    }

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response
    )

# Decorator para capturar exceções em funções
def handle_exceptions(func):
    """Decorator para capturar e tratar exceções automaticamente"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AgenteConcurseiroException as e:
            # Re-raise exceções personalizadas
            raise e
        except Exception as e:
            # Log e converter para exceção personalizada
            logger.error(f"Exception in {func.__name__}: {str(e)}", exc_info=True)
            raise AgenteConcurseiroException(
                message=f"Erro interno na função {func.__name__}",
                error_code="INTERNAL_ERROR",
                details={"original_error": str(e)}
            )

    return wrapper

# Context manager para capturar exceções
class ExceptionContext:
    """Context manager para capturar e tratar exceções"""

    def __init__(self, operation: str, logger: logging.Logger = None):
        self.operation = operation
        self.logger = logger or get_logger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.logger.error(
                f"Exception in operation '{self.operation}': {str(exc_val)}",
                exc_info=(exc_type, exc_val, exc_tb)
            )

            # Converter para exceção personalizada se não for uma
            if not isinstance(exc_val, AgenteConcurseiroException):
                raise AgenteConcurseiroException(
                    message=f"Erro na operação '{self.operation}'",
                    error_code="OPERATION_ERROR",
                    details={"original_error": str(exc_val)}
                )

        return False  # Não suprimir a exceção

# Função utilitária para validar dados
def validate_required_fields(data: Dict[str, Any], required_fields: list, context: str = "") -> None:
    """Valida se campos obrigatórios estão presentes"""

    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)

    if missing_fields:
        raise ValidationError(
            message=f"Campos obrigatórios ausentes: {', '.join(missing_fields)}",
            details={"missing_fields": missing_fields, "context": context}
        )

def validate_field_type(value: Any, expected_type: type, field_name: str) -> None:
    """Valida o tipo de um campo"""

    if not isinstance(value, expected_type):
        raise ValidationError(
            message=f"Campo '{field_name}' deve ser do tipo {expected_type.__name__}",
            field=field_name,
            details={"expected_type": expected_type.__name__, "actual_type": type(value).__name__}
        )

def validate_string_length(value: str, field_name: str, min_length: int = 0, max_length: int = None) -> None:
    """Valida o comprimento de uma string"""

    if not isinstance(value, str):
        raise ValidationError(
            message=f"Campo '{field_name}' deve ser uma string",
            field=field_name
        )

    if len(value) < min_length:
        raise ValidationError(
            message=f"Campo '{field_name}' deve ter pelo menos {min_length} caracteres",
            field=field_name
        )

    if max_length and len(value) > max_length:
        raise ValidationError(
            message=f"Campo '{field_name}' deve ter no máximo {max_length} caracteres",
            field=field_name
        )
