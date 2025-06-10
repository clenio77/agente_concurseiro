from crewai import Agent
from tools.performance_prediction_tool import PerformancePredictionTool

def create_performance_prediction_agent():
    return Agent(
        role="Analista de Desempenho",
        goal="Prever o desempenho futuro do candidato e identificar áreas para melhoria",
        backstory="Especialista em análise de dados educacionais e previsão de desempenho, com experiência em modelagem preditiva para otimização de estudos.",
        tools=[PerformancePredictionTool()],
        verbose=True
    )