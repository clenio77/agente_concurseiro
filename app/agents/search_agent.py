"""
Módulo do Agente de Busca de Provas
Responsável por criar o agente que busca provas anteriores na web.
"""

from crewai import Agent
from tools.web_search_tool import WebSearchTool

def create_search_agent():
    """
    Cria e retorna o agente especialista em busca de provas.
    O agente utiliza a WebSearchTool para encontrar provas anteriores conforme critérios do usuário.
    :return: Instância configurada de Agent para busca de provas.
    """
    return Agent(
        role="Especialista em Busca de Provas",
        goal="Encontrar provas anteriores para o cargo, concurso, banca e cidade especificados.",
        backstory="Especialista em busca na web e recuperação de dados, com conhecimento profundo de repositórios de provas de concursos públicos.",
        tools=[WebSearchTool()],  # Ferramenta de busca na web
        verbose=True
    )