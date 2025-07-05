"""Stub extremamente simplificado do pacote *pydantic*.

Inclui apenas objetos utilizados nos testes do projeto: `BaseModel`,
`BaseSettings`, `EmailStr`, `AnyHttpUrl` e `validator`.

Este *stub* **não** executa validações reais – ele existe apenas para impedir
erros de importação durante a execução dos testes automatizados.
"""
from __future__ import annotations

import types
from typing import Any, Callable, Dict

__all__ = [
    "BaseModel",
    "BaseSettings",
    "EmailStr",
    "AnyHttpUrl",
    "PostgresDsn",
    "validator",
    "UUID4",
    "Field",
    "ValidationError",
]


class BaseModel:  # noqa: D101
    def __init__(self, **data: Any):  # noqa: D401
        for k, v in data.items():
            setattr(self, k, v)

    def dict(self, **kwargs):  # noqa: D401
        return self.__dict__


class BaseSettings(BaseModel):  # noqa: D101
    class Config:  # noqa: D101
        env_file: str = ""

    def __init__(self, _env_file: str | None = None, **data: Any):
        super().__init__(**data)


# Tipos simulados
EmailStr = str  # type alias
AnyHttpUrl = str
PostgresDsn = str
UUID4 = str


# Decorator de validação (faz *passthrough*)

def validator(*args, **kwargs):  # noqa: D401
    def decorator(func: Callable):
        return func

    return decorator

# Field helper

def Field(default=None, **kwargs):  # noqa: D401
    return default


# Exceção de validação simulada
class ValidationError(ValueError):
    pass


# Cria submódulo `errors` vazio para compatibilidade
import sys  # noqa: E402

errors_module = types.ModuleType("pydantic.errors")
setattr(errors_module, "PydanticImportError", ImportError)

sys.modules["pydantic.errors"] = errors_module