"""
Módulo do Agente de Redação
Responsável por criar o agente que avalia e fornece feedback sobre redações.
"""

from crewai import Agent
from tools.writing_tool import WritingTool

def create_writing_agent():
    """
    Cria e retorna o agente especialista em redação.
    O agente utiliza a WritingTool para avaliar e dar feedback detalhado sobre textos do candidato.
    :return: Instância configurada de Agent para redação.
    """
    return Agent(
        role="Especialista em Redação",
        goal="Avaliar e fornecer feedback detalhado sobre redações para concursos públicos.",
        backstory="Professor experiente de redação com especialização em textos dissertativos-argumentativos e peças processuais para concursos públicos.",
        tools=[WritingTool()],  # Ferramenta de avaliação de redação
        verbose=True
    )