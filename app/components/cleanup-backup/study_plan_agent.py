"""
Módulo do Agente de Plano de Estudos
Responsável por criar o agente que gera planos de estudo personalizados.
"""

from __future__ import annotations

from crewai import Agent

from tools.study_plan_tool import StudyPlanTool


def create_study_plan_agent():
    """
    Cria o agente responsável por gerar o plano de estudos.
    """
    return Agent(
        role='Planejador de Estudos',
        goal='Criar um plano de estudos personalizado e eficaz',
        backstory='Você é um especialista em planejamento de estudos para concursos, capaz de criar cronogramas realistas e otimizados.',
        tools=[StudyPlanTool()],
        allow_delegation=False,
        verbose=True
    )
