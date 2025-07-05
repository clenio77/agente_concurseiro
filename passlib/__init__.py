"""Stub mínimo da biblioteca passlib utilizado nos testes."""
from __future__ import annotations

class CryptContext:  # noqa: D101
    def __init__(self, schemes=None, deprecated="auto"):
        self._schemes = schemes or []

    def hash(self, password: str) -> str:  # noqa: D401
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def verify(self, password: str, hashed: str) -> bool:  # noqa: D401
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest() == hashed


# Expor submódulo context
import types  # noqa: E402
import sys  # noqa: E402

context_module = types.ModuleType("passlib.context")
setattr(context_module, "CryptContext", CryptContext)
sys.modules["passlib.context"] = context_module