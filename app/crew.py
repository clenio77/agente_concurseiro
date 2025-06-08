from crewai import Crew, Process
from agents.search_agent import create_search_agent
from agents.study_plan_agent import create_study_plan_agent
from agents.mock_exam_agent import create_mock_exam_agent
from crewai import Task

def run_crew(cargo, concurso, banca, cidade, study_hours, study_months):
    # Inicializa agentes
    search_agent = create_search_agent()
    study_plan_agent = create_study_plan_agent()
    mock_exam_agent = create_mock_exam_agent()

    # Define tarefas
    search_task = Task(
        description=f"Buscar provas anteriores para o cargo '{cargo}' no concurso '{concurso}', organizado pela banca '{banca}' na cidade '{cidade}'.",
        agent=search_agent,
        expected_output="Lista de provas encontradas e dados extraídos."
    )

    study_plan_task = Task(
        description=f"Criar um plano de estudos para {study_hours} horas/semana durante {study_months} meses com base nas provas encontradas.",
        agent=study_plan_agent,
        expected_output="Plano de estudos no formato JSON."
    )

    mock_exam_task = Task(
        description=f"Gerar um simulado com base nos padrões da banca '{banca}' e nas provas encontradas.",
        agent=mock_exam_agent,
        expected_output="Simulado no formato de texto com questões e respostas."
    )

    # Cria crew
    crew = Crew(
        agents=[search_agent, study_plan_agent, mock_exam_agent],
        tasks=[search_task, study_plan_task, mock_exam_task],
        process=Process.sequential
    )

    # Executa crew
    result = crew.kickoff()
    
    return {
        "exam_data": result.tasks_output[0].raw,
        "study_plan": result.tasks_output[1].raw,
        "mock_exam": result.tasks_output[2].raw
    }