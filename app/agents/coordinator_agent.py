"""
Módulo do Agente Coordenador
Responsável por criar o agente que coordena os diferentes aspectos da preparação para concursos.
"""

from crewai import Agent
from tools.coordination_tool import CoordinationTool

def create_coordinator_agent():
    """
    Cria e retorna o agente coordenador de preparação para concursos.
    O agente integra plano de estudos, materiais e redação, utilizando a CoordinationTool.
    :return: Instância configurada de Agent para coordenação.
    """
    return Agent(
        role="Coordenador de Preparação",
        goal="Coordenar os diferentes aspectos da preparação para concursos, integrando plano de estudos, materiais e redação.",
        backstory="Especialista em metodologias de estudo e preparação para concursos, com experiência em coordenar equipes multidisciplinares.",
        tools=[CoordinationTool()],  # Ferramenta de coordenação
        verbose=True
    )