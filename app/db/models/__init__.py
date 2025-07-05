"""Pacote de modelos SQLAlchemy.
Este arquivo garante que `import app.db.models.*` funcione corretamente,
mesmo coexistindo com o arquivo `app/db/models.py` (que contém outros modelos).
"""
from importlib import import_module
from types import ModuleType
import sys

# Importar todos os submódulos explicitamente utilizados nos testes
for _name in [
    "user",
    "study_plan",
    "flashcard",
    "quiz",
    "performance",
]:
    module = import_module(f"app.db.models.{_name}")
    sys.modules[f"app.db.models.{_name}"] = module  # Garantir registro

# Tornar classes acessíveis diretamente via app.db.models.X se desejado
from app.db.models.user import User  # noqa: F401,E402

__all__ = ["User"]