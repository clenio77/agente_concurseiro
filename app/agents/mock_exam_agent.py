"""
Módulo do Agente de Simulados
Responsável por criar o agente que gera simulados baseados em provas anteriores.
"""

from crewai import Agent
from tools.mock_exam_tool import MockExamTool

def create_mock_exam_agent():
    """
    Cria e retorna o agente gerador de simulados.
    O agente utiliza padrões de provas anteriores e a MockExamTool para criar simulados realistas.
    :return: Instância configurada de Agent para simulados.
    """
    return Agent(
        role="Gerador de Simulados",
        goal="Gerar simulados com base no estilo de questões e padrões de provas anteriores da banca.",
        backstory="Especialista em design de provas, familiarizado com os formatos e níveis de dificuldade das bancas.",
        tools=[MockExamTool()],  # Ferramenta de geração de simulados
        verbose=True
    )