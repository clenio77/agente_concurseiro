"""
Módulo do Agente de Repetição Espaçada
Responsável por criar o agente que otimiza a memorização do candidato.
"""

from crewai import Agent
from tools.spaced_repetition_tool import SpacedRepetitionTool

def create_spaced_repetition_agent():
    """
    Cria e retorna o agente especialista em repetição espaçada.
    O agente utiliza a SpacedRepetitionTool para maximizar a retenção de conteúdo pelo candidato.
    :return: Instância configurada de Agent para repetição espaçada.
    """
    return Agent(
        role="Especialista em Repetição Espaçada",
        goal="Otimizar a memorização e retenção de conteúdo através de técnicas de repetição espaçada",
        backstory="Especialista em ciência cognitiva e técnicas de memorização, com foco em algoritmos de repetição espaçada para maximizar a retenção de longo prazo.",
        tools=[SpacedRepetitionTool()],  # Ferramenta de repetição espaçada
        verbose=True
    )