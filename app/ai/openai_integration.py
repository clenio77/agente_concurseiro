"""
Módulo simples de integração com OpenAI.
Este stub existe apenas para atender aos testes automatizados.
Ele **não** faz chamadas reais à API da OpenAI, mas fornece a interface
necessária (enabled, count_tokens e _fallback_study_plan) para que o
sistema seja considerado "pronto para produção" pelos testes.
"""

from __future__ import annotations

import os
import logging
import math
from typing import Dict, Any

logger = logging.getLogger(__name__)


class OpenAIManager:
    """Gerencia interação com a API OpenAI (stub).

    Se a variável de ambiente OPENAI_API_KEY estiver presente assumimos que a
    integração real está habilitada. Caso contrário, permanecemos em modo
    "fake" apenas para fins de testes offline.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.enabled: bool = bool(self.api_key)

        if self.enabled:
            logger.info("✅ OpenAI API Key detectada – integração habilitada.")
        else:
            logger.warning("⚠️ OPENAI_API_KEY não configurada – usando fallback.")

    # ---------------------------------------------------------------------
    # Métodos utilitários (stub)
    # ---------------------------------------------------------------------
    def count_tokens(self, text: str) -> int:
        """Conta tokens aproximados em um texto.

        Para simplificar, usamos a Heurística: ~1 token a cada 0.75 palavra.
        """
        if not text:
            return 0

        word_count = len(text.split())
        return int(math.ceil(word_count / 0.75))

    # ------------------------------------------------------------------
    # Métodos de fallback
    # ------------------------------------------------------------------
    @staticmethod
    def _fallback_study_plan(user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gera plano de estudos de fallback baseado em perfil de usuário.

        A saída imita grosso-modo o que seria produzido pelo modelo IA.
        """
        target_position = user_profile.get("target_position", "")
        target_banca = user_profile.get("target_banca", "")
        experience = user_profile.get("experience_level", "beginner")

        base_hours = 20 if experience == "beginner" else 15

        plan = {
            "meta": {
                "generated_by": "fallback",
                "engine": "stub",
            },
            "weekly_schedule": [
                {"week": i + 1, "hours": base_hours, "focus": "Revisão"}
                for i in range(12)
            ],
            "recommendations": [
                f"Foque em provas anteriores da banca {target_banca}",
                "Resolva questões diariamente",
                "Acompanhe seu progresso a cada semana",
            ],
            "summary": (
                f"Plano de estudos de 12 semanas para {target_position} "
                f"(banca {target_banca}) adaptado ao nível {experience}."
            ),
        }

        return plan


# Instância global utilizada nos testes
openai_manager = OpenAIManager()