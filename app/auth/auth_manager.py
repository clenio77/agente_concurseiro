"""
Gerenciador de autenticação simplificado utilizado apenas para fins de teste.
Não deve ser utilizado em produção sem reforço de segurança.
Fornece as interfaces esperadas pelos testes automatizados.
"""

from __future__ import annotations

import os
import time
import hashlib
import logging
from typing import Dict, Any

import jwt  # Dependência em requirements-prod.txt (pyjwt)

try:
    import bcrypt  # type: ignore

    def _bcrypt_hash(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def _bcrypt_verify(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())

    _HASH_FUNC = "bcrypt"
except Exception:  # pragma: no cover
    # Fallback: SHA256 (NÃO recomendado para produção)
    def _bcrypt_hash(password: str) -> str:  # type: ignore
        return hashlib.sha256(password.encode()).hexdigest()

    def _bcrypt_verify(password: str, hashed: str) -> bool:  # type: ignore
        return hashlib.sha256(password.encode()).hexdigest() == hashed

    _HASH_FUNC = "sha256"


logger = logging.getLogger(__name__)

_SECRET_KEY = os.getenv("JWT_SECRET", "secret-key-for-tests")
_ALGORITHM = "HS256"
_ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))


class _UserStore:
    """Armazena usuários em memória (ou opcionalmente em arquivo JSON)."""

    def __init__(self) -> None:
        self._users: Dict[str, Dict[str, Any]] = {}
        self._file_path = "data/test_users.json"
        # Carregar usuários já existentes (se houver)
        if os.path.exists(self._file_path):
            try:
                import json

                with open(self._file_path, "r", encoding="utf-8") as f:
                    self._users = json.load(f)
            except Exception as e:  # noqa: BLE001
                logger.warning("Não foi possível carregar usuários de %s: %s", self._file_path, e)

    def _persist(self) -> None:
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        try:
            import json

            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(self._users, f, indent=2, ensure_ascii=False)
        except Exception as e:  # noqa: BLE001
            logger.warning("Não foi possível persistir usuários: %s", e)

    # ------------------------------------------------------------------
    def add_user(self, email: str, username: str, password: str, **extra: Any) -> Dict[str, Any]:
        if email in self._users or any(u["username"] == username for u in self._users.values()):
            return {"success": False, "error": "User already exists"}

        user_id = hashlib.md5(f"{email}{time.time()}".encode()).hexdigest()
        hashed_pw = _bcrypt_hash(password)
        self._users[email] = {
            "id": user_id,
            "email": email,
            "username": username,
            "password_hash": hashed_pw,
            **extra,
        }
        self._persist()
        return {"success": True, "user_id": user_id}

    def verify_credentials(self, email_or_username: str, password: str) -> Dict[str, Any] | None:
        # Buscar por email
        user = self._users.get(email_or_username)
        if not user:
            # Buscar por username
            user = next((u for u in self._users.values() if u["username"] == email_or_username), None)
            if not user:
                return None

        if _bcrypt_verify(password, user["password_hash"]):
            return user
        return None

    def get_by_id(self, user_id: str) -> Dict[str, Any] | None:  # noqa: D401
        return next((u for u in self._users.values() if u["id"] == user_id), None)


_user_store = _UserStore()


class AuthManager:
    """Gerenciador de autenticação simplificado."""

    @staticmethod
    def create_user(email: str, username: str, password: str, full_name: str | None = None) -> Dict[str, Any]:
        """Cria novo usuário no sistema (apenas memória)."""
        return _user_store.add_user(email, username, password, full_name=full_name)

    # ------------------------------------------------------------------
    @staticmethod
    def _create_access_token(data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        to_encode["exp"] = int(time.time()) + (_ACCESS_TOKEN_EXPIRE_HOURS * 3600)
        token = jwt.encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)
        return token

    # ------------------------------------------------------------------
    @staticmethod
    def authenticate_user(email_or_username: str, password: str, ip_address: str | None = None) -> Dict[str, Any]:
        user = _user_store.verify_credentials(email_or_username, password)
        if not user:
            return {"success": False, "error": "Invalid credentials"}

        token = AuthManager._create_access_token({"sub": user["id"], "username": user["username"], "ip": ip_address})
        return {"success": True, "access_token": token}

    # ------------------------------------------------------------------
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any] | None:
        try:
            payload = jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise jwt.InvalidTokenError("Invalid payload")
            user = _user_store.get_by_id(user_id)
            if not user:
                raise jwt.InvalidTokenError("User not found")
            return payload
        except jwt.PyJWTError as e:  # noqa: BLE001
            logger.warning("Falha ao verificar token: %s", e)
            return None


# Instância global
auth_manager = AuthManager()