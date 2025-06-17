"""
Módulo do Agente de Previsão de Desempenho
Responsável por criar o agente que prevê o desempenho do candidato.
"""

from crewai import Agent
from tools.performance_prediction_tool import PerformancePredictionTool

def create_performance_prediction_agent():
    """
    Cria e retorna o agente analista de desempenho.
    O agente utiliza técnicas de modelagem preditiva e a PerformancePredictionTool para prever resultados e sugerir melhorias.
    :return: Instância configurada de Agent para previsão de desempenho.
    """
    return Agent(
        role="Analista de Desempenho",
        goal="Prever o desempenho futuro do candidato e identificar áreas para melhoria",
        backstory="Especialista em análise de dados educacionais e previsão de desempenho, com experiência em modelagem preditiva para otimização de estudos.",
        tools=[PerformancePredictionTool()],  # Ferramenta de previsão de desempenho
        verbose=True
    )