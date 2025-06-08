from crewai import Agent
from tools.mock_exam_tool import MockExamTool

def create_mock_exam_agent():
    return Agent(
        role="Gerador de Simulados",
        goal="Gerar simulados com base no estilo de questões e padrões de provas anteriores da banca.",
        backstory="Especialista em design de provas, familiarizado com os formatos e níveis de dificuldade das bancas.",
        tools=[MockExamTool()],
        verbose=True
    )