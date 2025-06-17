"""
Módulo do Agente de Plano de Estudos
Responsável por criar o agente que gera planos de estudo personalizados.
"""

from crewai import Agent
from tools.study_plan_tool import StudyPlanTool

def create_study_plan_agent():
    """
    Cria e retorna o agente criador de plano de estudos.
    O agente utiliza a StudyPlanTool para montar cronogramas personalizados para o candidato.
    :return: Instância configurada de Agent para plano de estudos.
    """
    return Agent(
        role="Criador de Plano de Estudos",
        goal="Criar um plano de estudos personalizado com base em provas anteriores e padrões da banca.",
        backstory="Educador experiente especializado em criar cronogramas de estudo estruturados para candidatos a concursos.",
        tools=[StudyPlanTool()],  # Ferramenta de criação de plano de estudos
        verbose=True
    )