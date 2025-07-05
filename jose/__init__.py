"""Stub simplificado da biblioteca `python-jose`.

Fornece apenas as funções `encode` e `decode` dentro do submódulo `jose.jwt`.
Não utiliza criptografia real – apenas codifica/decodifica JSON em base64 para
atender aos testes.
"""
from __future__ import annotations

import base64
import json
import sys
from typing import Any, Dict


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


class _JWTStub:  # noqa: D101
    @staticmethod
    def encode(payload: Dict[str, Any], key: str | None = None, algorithm: str | None = None):  # noqa: D401
        header = {"alg": algorithm or "none", "typ": "JWT"}
        segments = [
            _b64encode(json.dumps(header).encode()),
            _b64encode(json.dumps(payload).encode()),
            ""  # assinatura vazia
        ]
        return ".".join(segments)

    @staticmethod
    def decode(token: str, key: str | None = None, algorithms: list[str] | None = None):  # noqa: D401
        try:
            header_b64, payload_b64, _signature = token.split(".")
            payload_json = _b64decode(payload_b64).decode()
            return json.loads(payload_json)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("Invalid token") from exc


jwt = _JWTStub()

import types  # noqa: E402

jwt_module = types.ModuleType("jose.jwt")
setattr(jwt_module, "encode", _JWTStub.encode)
setattr(jwt_module, "decode", _JWTStub.decode)

# Expor submódulo
sys.modules["jose.jwt"] = jwt_module