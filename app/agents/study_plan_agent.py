from crewai import Agent
from tools.study_plan_tool import StudyPlanTool

def create_study_plan_agent():
    return Agent(
        role="Criador de Plano de Estudos",
        goal="Criar um plano de estudos personalizado com base em provas anteriores e padrões da banca.",
        backstory="Educador experiente especializado em criar cronogramas de estudo estruturados para candidatos a concursos.",
        tools=[StudyPlanTool()],
        verbose=True
    )