import hashlib
import re
import secrets
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import redis
from fastapi import Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AuthenticationError, AuthorizationError, RateLimitError
from app.core.logger import get_logger, log_api_request, log_security_event
from app.db.base import get_db
from app.db.models import User

logger = get_logger(__name__)

# Configuração de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração de segurança
security = HTTPBearer()

# Redis para rate limiting (opcional)
redis_client = None
if settings.REDIS_URL:
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        redis_client.ping()  # Testar conexão
        logger.info("Redis connected for rate limiting")
    except Exception as e:
        logger.warning(f"Redis not available for rate limiting: {e}")

class SecurityManager:
    """Gerenciador de segurança centralizado"""

    def __init__(self):
        self.password_patterns = {
            'min_length': 8,
            'max_length': 128,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_digits': True,
            'require_special': True,
            'forbidden_patterns': [
                r'123456',
                r'password',
                r'qwerty',
                r'admin',
                r'user',
                r'123',
                r'abc'
            ]
        }

        self.rate_limits = {
            'login': {'requests': 5, 'window': 300},  # 5 tentativas em 5 minutos
            'register': {'requests': 3, 'window': 3600},  # 3 registros por hora
            'api': {'requests': 100, 'window': 3600},  # 100 requests por hora
            'crew_execution': {'requests': 10, 'window': 3600},  # 10 execuções por hora
        }

    def hash_password(self, password: str) -> str:
        """Hash de senha com bcrypt"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica senha com bcrypt"""
        return pwd_context.verify(plain_password, hashed_password)

    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Valida força da senha"""
        errors = []
        warnings = []

        # Verificar comprimento
        if len(password) < self.password_patterns['min_length']:
            errors.append(f"Senha deve ter pelo menos {self.password_patterns['min_length']} caracteres")
        elif len(password) > self.password_patterns['max_length']:
            errors.append(f"Senha deve ter no máximo {self.password_patterns['max_length']} caracteres")

        # Verificar requisitos
        if self.password_patterns['require_uppercase'] and not re.search(r'[A-Z]', password):
            errors.append("Senha deve conter pelo menos uma letra maiúscula")

        if self.password_patterns['require_lowercase'] and not re.search(r'[a-z]', password):
            errors.append("Senha deve conter pelo menos uma letra minúscula")

        if self.password_patterns['require_digits'] and not re.search(r'\d', password):
            errors.append("Senha deve conter pelo menos um número")

        if self.password_patterns['require_special'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Senha deve conter pelo menos um caractere especial")

        # Verificar padrões proibidos
        for pattern in self.password_patterns['forbidden_patterns']:
            if re.search(pattern, password, re.IGNORECASE):
                warnings.append(f"Senha contém padrão comum: {pattern}")

        # Verificar sequências
        if re.search(r'(.)\1{2,}', password):
            warnings.append("Senha contém caracteres repetidos")

        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password, re.IGNORECASE):
            warnings.append("Senha contém sequência de letras")

        if re.search(r'(123|234|345|456|567|678|789|012)', password):
            warnings.append("Senha contém sequência de números")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'score': self._calculate_password_score(password)
        }

    def _calculate_password_score(self, password: str) -> int:
        """Calcula score da senha (0-100)"""
        score = 0

        # Comprimento
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10

        # Complexidade
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'\d', password):
            score += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 10

        # Penalidades
        for pattern in self.password_patterns['forbidden_patterns']:
            if re.search(pattern, password, re.IGNORECASE):
                score -= 20

        return max(0, min(100, score))

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Cria token JWT de acesso"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verifica e decodifica token JWT"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")

            if username is None:
                raise AuthenticationError("Token inválido")

            return payload
        except JWTError as e:
            raise AuthenticationError(f"Token inválido: {str(e)}")

    def check_rate_limit(self, key: str, limit_type: str = 'api') -> bool:
        """Verifica rate limit"""
        if not redis_client:
            return True  # Sem Redis, não aplicar rate limiting

        try:
            limit_config = self.rate_limits.get(limit_type, self.rate_limits['api'])
            current_time = int(time.time())
            window_start = current_time - limit_config['window']

            # Usar Redis para tracking
            pipe = redis_client.pipeline()
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zadd(key, {str(current_time): current_time})
            pipe.zcard(key)
            pipe.expire(key, limit_config['window'])
            results = pipe.execute()

            current_requests = results[2]

            if current_requests > limit_config['requests']:
                log_security_event(
                    logger,
                    "rate_limit_exceeded",
                    details=f"Rate limit exceeded for {key} ({limit_type})"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # Em caso de erro, permitir

    def sanitize_input(self, text: str) -> str:
        """Sanitiza entrada de texto"""
        if not text:
            return text

        # Remover caracteres perigosos
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
        for char in dangerous_chars:
            text = text.replace(char, '')

        # Remover scripts
        text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)

        # Limitar comprimento
        if len(text) > 10000:  # 10KB
            text = text[:10000]

        return text.strip()

    def validate_email(self, email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_username(self, username: str) -> bool:
        """Valida formato de username"""
        # 3-20 caracteres, apenas letras, números e underscore
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))

    def generate_secure_token(self, length: int = 32) -> str:
        """Gera token seguro"""
        return secrets.token_urlsafe(length)

    def hash_sensitive_data(self, data: str) -> str:
        """Hash de dados sensíveis"""
        return hashlib.sha256(data.encode()).hexdigest()

# Instância global do gerenciador de segurança
security_manager = SecurityManager()

# Exportar constantes
ALGORITHM = "HS256"

# Exportar funções
create_access_token = security_manager.create_access_token
verify_password = security_manager.verify_password
get_password_hash = security_manager.hash_password

# Middleware de segurança
def add_security_middleware(app):
    """Adiciona middlewares de segurança à aplicação"""

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Rate limiting middleware
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        # Gerar chave única para rate limiting
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        rate_limit_key = f"rate_limit:{client_ip}:{hashlib.md5(user_agent.encode()).hexdigest()}"

        # Verificar rate limit
        if not security_manager.check_rate_limit(rate_limit_key, 'api'):
            raise RateLimitError(
                service="API",
                retry_after=300,
                details={"client_ip": client_ip}
            )

        # Adicionar timestamp de início
        request.state.start_time = datetime.utcnow()

        response = await call_next(request)

        # Log da requisição
        duration = (datetime.utcnow() - request.state.start_time).total_seconds()
        log_api_request(
            logger,
            request.method,
            request.url.path,
            response.status_code,
            duration,
            request_id=getattr(request.state, 'request_id', None)
        )

        return response

# Dependências de segurança
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Obtém usuário atual a partir do token"""

    try:
        # Verificar token
        payload = security_manager.verify_token(credentials.credentials)
        username: str = payload.get("sub")

        if username is None:
            raise AuthenticationError("Token inválido")

        # Buscar usuário no banco
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise AuthenticationError("Usuário não encontrado")

        if not user.is_active:
            raise AuthenticationError("Usuário inativo")

        return user

    except JWTError as e:
        raise AuthenticationError(f"Token inválido: {str(e)}")

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtém usuário ativo atual"""
    if not current_user.is_active:
        raise AuthenticationError("Usuário inativo")
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtém usuário administrador atual"""
    # TODO: Implementar sistema de roles/permissões
    # Por enquanto, todos os usuários ativos são considerados admin
    return current_user

# Funções utilitárias de segurança
def validate_and_sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valida e sanitiza dados de entrada"""
    sanitized_data = {}

    for key, value in data.items():
        if isinstance(value, str):
            sanitized_data[key] = security_manager.sanitize_input(value)
        elif isinstance(value, dict):
            sanitized_data[key] = validate_and_sanitize_input(value)
        elif isinstance(value, list):
            sanitized_data[key] = [
                validate_and_sanitize_input(item) if isinstance(item, dict)
                else security_manager.sanitize_input(item) if isinstance(item, str)
                else item
                for item in value
            ]
        else:
            sanitized_data[key] = value

    return sanitized_data

def check_permission(user: User, resource: str, action: str) -> bool:
    """Verifica permissão do usuário"""
    # TODO: Implementar lógica de permissões baseada em roles
    # Por enquanto, todos os usuários ativos têm todas as permissões
    if user.is_active:
        return True

    # Permissões específicas podem ser implementadas aqui
    user_permissions = getattr(user, 'permissions', [])

    required_permission = f"{resource}:{action}"
    return required_permission in user_permissions

def log_security_activity(user_id: int, action: str, details: str = "", ip_address: str = None):
    """Log de atividade de segurança"""
    log_security_event(
        logger,
        action,
        user_id=user_id,
        ip_address=ip_address,
        details=details
    )

# Configurações de segurança
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
}

def add_security_headers(response):
    """Adiciona headers de segurança à resposta"""
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response
