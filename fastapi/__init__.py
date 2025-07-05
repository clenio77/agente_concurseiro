"""Stub simplificado da biblioteca FastAPI para fins de teste.

Esta implementação **não** fornece o framework completo, apenas o mínimo
necessário para que os testes automatizados importem `fastapi.TestClient` e
criem instâncias de `FastAPI`.
"""
from __future__ import annotations

from types import SimpleNamespace
import types
from typing import Any, Callable, Dict


class FastAPI:  # noqa: D101
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
        self.routes: Dict[str, Callable] = {}
        # Armazena pares (classe_middleware, opções) apenas para fins de teste.
        self._middlewares: list[object] = []
        self.dependency_overrides: Dict = {}

    # Decorador para middlewares
    def middleware(self, _type: str):  # noqa: D401
        def wrapper(func: Callable):
            self._middlewares.append(func)
            return func

        return wrapper

    def include_router(self, router: "APIRouter", prefix: str | None = None, **_kwargs):  # noqa: D401
        # Mescla rotas do roteador ao app
        for path, func in router.routes.items():
            full_path = f"{prefix}{path}" if prefix else path
            self.routes[full_path] = func

    # Decoradores de rota
    def get(self, path: str, **_kwargs) -> Callable[[Callable], Callable]:
        def decorator(func: Callable) -> Callable:
            self.routes[path] = func
            return func
        return decorator

    def post(self, path: str, **_kwargs) -> Callable[[Callable], Callable]:
        return self.get(path, **_kwargs)

    # Métodos extras
    def put(self, path: str, **_kwargs):
        return self.get(path, **_kwargs)

    def delete(self, path: str, **_kwargs):
        return self.get(path, **_kwargs)

    def patch(self, path: str, **_kwargs):
        return self.get(path, **_kwargs)

    # ------------------------------------------------------------------
    # Middleware e dependências
    # ------------------------------------------------------------------

    def add_middleware(self, middleware_cls, **options):  # noqa: D401
        """Registra middleware fictício (apenas armazena referência)."""
        self._middlewares.append((middleware_cls, options))  # type: ignore[arg-type]

    # Método responsável pelo TestClient stub
    def _handle_request(self, method: str, path: str, data: Any | None = None):
        if path in self.routes:
            return self.routes[path](), 200
        return {"detail": "Not Found"}, 404


# Roteador simples
class APIRouter:  # noqa: D101
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.routes: Dict[str, Callable] = {}

    def include_router(self, router: "APIRouter", prefix: str | None = None, **_kwargs):  # noqa: D401
        # Mesclar rotas
        self.routes.update(router.routes)

    def get(self, path: str, **_kwargs) -> Callable[[Callable], Callable]:
        def decorator(func: Callable) -> Callable:
            self.routes[path] = func
            return func
        return decorator

    def post(self, path: str, **_kwargs) -> Callable[[Callable], Callable]:
        return self.get(path, **_kwargs)

    def put(self, path: str, **_kwargs):
        return self.get(path, **_kwargs)

    def delete(self, path: str, **_kwargs):
        return self.get(path, **_kwargs)

    def patch(self, path: str, **_kwargs):
        return self.get(path, **_kwargs)

    # Chamado pelo TestClient stub
    def _handle_request(self, method: str, path: str, data: Any | None = None):  # noqa: D401
        if path in self.routes:
            return self.routes[path]()
        return {"detail": "Not Found"}, 404


# -------------------------- Test Client Stub ------------------------------
class _Response:  # noqa: D101
    def __init__(self, status_code: int, json_data: Any):
        self.status_code = status_code
        self._json = json_data

    def json(self):  # noqa: D401
        return self._json


class TestClient:  # noqa: D101
    def __init__(self, app: FastAPI):
        self.app = app

    # Context manager
    def __enter__(self):  # noqa: D401
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: D401
        return False

    # Métodos HTTP simples
    def get(self, path: str, **kwargs):  # noqa: D401
        json_data, status = self.app._handle_request("GET", path)
        return _Response(status, json_data)

    def post(self, path: str, data: Any | None = None, json: Any | None = None, **kwargs):  # noqa: D401
        json_data, status = self.app._handle_request("POST", path, data or json)
        return _Response(status, json_data)


# -------------------------------------------------------------------------
# Submódulo mapping para `fastapi.testclient`
import sys  # noqa: E402

sys.modules.setdefault("fastapi.testclient", sys.modules[__name__])

# -------------------------------------------------------------------------
# Submódulo middleware / CORSMiddleware stub
# -------------------------------------------------------------------------

class CORSMiddleware:  # noqa: D101
    def __init__(self, *args, **kwargs):  # noqa: D401
        pass

# Criar submódulos de middleware
middleware_module = types.ModuleType("fastapi.middleware")
cors_module = types.ModuleType("fastapi.middleware.cors")
setattr(cors_module, "CORSMiddleware", CORSMiddleware)

# Atribuir dinamicamente usando setattr para evitar erros de tipo
setattr(middleware_module, "cors", cors_module)  # type: ignore[attr-defined]

# Introduzir nos sys.modules
sys.modules["fastapi.middleware"] = middleware_module
sys.modules["fastapi.middleware.cors"] = cors_module

# -------------------------------------------------------------------------
# Submódulo security (OAuth2PasswordRequestForm e base)
# -------------------------------------------------------------------------


class SecurityBase:  # noqa: D101
    pass


class OAuth2PasswordRequestForm:  # noqa: D101
    def __init__(self, username: str = "", password: str = "", scope: str = ""):  # noqa: D401
        self.username = username
        self.password = password
        self.scopes = scope.split()


security_module = types.ModuleType("fastapi.security")
setattr(security_module, "OAuth2PasswordRequestForm", OAuth2PasswordRequestForm)
setattr(security_module, "SecurityBase", SecurityBase)
class OAuth2PasswordBearer(SecurityBase):  # noqa: D101
    def __init__(self, tokenUrl: str = "token", scopes: dict | None = None):  # noqa: N803, D401
        self.tokenUrl = tokenUrl
        self.scopes = scopes or {}

    def __call__(self, *args, **kwargs):  # noqa: D401
        return "fake-token"

setattr(security_module, "OAuth2PasswordBearer", OAuth2PasswordBearer)

# nested submodules
sys.modules["fastapi.security"] = security_module
sys.modules["fastapi.security.base"] = security_module


# -------------------------------------------------------------------------
# Objetos utilitários extras (Depends, HTTPException, status)
# -------------------------------------------------------------------------

def Depends(dependency=None):  # noqa: D401
    return dependency


class HTTPException(Exception):  # noqa: D101
    def __init__(self, status_code: int, detail: str | None = None):
        super().__init__(detail or "HTTP Error")
        self.status_code = status_code
        self.detail = detail or "HTTP Error"


class _StatusModule(types.ModuleType):  # noqa: D101
    def __init__(self):
        super().__init__("fastapi.status")
        # Definir alguns códigos comuns usados nos testes
        self.HTTP_200_OK = 200
        self.HTTP_201_CREATED = 201
        self.HTTP_400_BAD_REQUEST = 400
        self.HTTP_401_UNAUTHORIZED = 401
        self.HTTP_403_FORBIDDEN = 403
        self.HTTP_404_NOT_FOUND = 404


status = _StatusModule()
sys.modules["fastapi.status"] = status

# -------------------------------------------------------------------------
# Submódulo responses
# -------------------------------------------------------------------------


class Response(dict):  # noqa: D101
    def __init__(self, content=None, status_code: int = 200):  # noqa: D401
        super().__init__(content or {})
        self.status_code = status_code


responses_module = types.ModuleType("fastapi.responses")
setattr(responses_module, "Response", Response)


class JSONResponse(Response):  # noqa: D101
    def __init__(self, content=None, status_code: int = 200):  # noqa: D401
        super().__init__(content, status_code)


setattr(responses_module, "JSONResponse", JSONResponse)
sys.modules["fastapi.responses"] = responses_module

__all__ = [
    "FastAPI",
    "TestClient",
    "APIRouter",
    "Depends",
    "HTTPException",
    "status",
]