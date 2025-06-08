from crewai import Agent
from tools.web_search_tool import WebSearchTool

def create_search_agent():
    return Agent(
        role="Especialista em Busca de Provas",
        goal="Encontrar provas anteriores para o cargo, concurso, banca e cidade especificados.",
        backstory="Especialista em busca na web e recuperação de dados, com conhecimento profundo de repositórios de provas de concursos públicos.",
        tools=[WebSearchTool()],
        verbose=True
    )