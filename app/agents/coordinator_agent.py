from crewai import Agent
from tools.coordination_tool import CoordinationTool

def create_coordinator_agent():
    return Agent(
        role="Coordenador de Preparação",
        goal="Coordenar os diferentes aspectos da preparação para concursos, integrando plano de estudos, materiais e redação.",
        backstory="Especialista em metodologias de estudo e preparação para concursos, com experiência em coordenar equipes multidisciplinares.",
        tools=[CoordinationTool()],
        verbose=True
    )