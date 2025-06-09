from crewai import Crew, Process
from agents.search_agent import create_search_agent
from agents.study_plan_agent import create_study_plan_agent
from agents.mock_exam_agent import create_mock_exam_agent
from agents.writing_agent import create_writing_agent
from agents.coordinator_agent import create_coordinator_agent
from agents.spaced_repetition_agent import create_spaced_repetition_agent
from agents.performance_prediction_agent import create_performance_prediction_agent
from crewai import Task
import json
import os

def run_crew(cargo, concurso, banca, cidade, study_hours, study_months):
    # Inicializa agentes
    search_agent = create_search_agent()
    study_plan_agent = create_study_plan_agent()
    mock_exam_agent = create_mock_exam_agent()
    writing_agent = create_writing_agent()
    coordinator_agent = create_coordinator_agent()
    spaced_repetition_agent = create_spaced_repetition_agent()
    performance_prediction_agent = create_performance_prediction_agent()

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
    
    spaced_repetition_task = Task(
        description=f"Criar um plano de revisão espaçada para os tópicos do plano de estudos, otimizando a memorização.",
        agent=spaced_repetition_agent,
        expected_output="Plano de revisão espaçada no formato JSON."
    )
    
    performance_prediction_task = Task(
        description=f"Prever o desempenho futuro com base no plano de estudos e dados históricos simulados.",
        agent=performance_prediction_agent,
        expected_output="Previsão de desempenho e recomendações no formato JSON."
    )

    # Cria crew
    crew = Crew(
        agents=[search_agent, study_plan_agent, mock_exam_agent, spaced_repetition_agent, performance_prediction_agent],
        tasks=[search_task, study_plan_task, mock_exam_task, spaced_repetition_task, performance_prediction_task],
        process=Process.sequential
    )

    # Executa crew
    result = crew.kickoff()
    
    return {
        "exam_data": result.tasks_output[0].raw,
        "study_plan": result.tasks_output[1].raw,
        "mock_exam": result.tasks_output[2].raw,
        "spaced_repetition_plan": result.tasks_output[3].raw,
        "performance_prediction": result.tasks_output[4].raw
    }
