from crewai import Agent
from tools.spaced_repetition_tool import SpacedRepetitionTool

def create_spaced_repetition_agent():
    return Agent(
        role="Especialista em Repetição Espaçada",
        goal="Otimizar a memorização e retenção de conteúdo através de técnicas de repetição espaçada",
        backstory="Especialista em ciência cognitiva e técnicas de memorização, com foco em algoritmos de repetição espaçada para maximizar a retenção de longo prazo.",
        tools=[SpacedRepetitionTool()],
        verbose=True
    )