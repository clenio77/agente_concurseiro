from crewai import Agent
from tools.question_api_tool import QuestionAPITool

def create_question_agent():
    return Agent(
        role="Especialista em Questões",
        goal="Fornecer questões relevantes e personalizadas para o candidato, com base em seu plano de estudos e desempenho",
        backstory="Especialista em bancos de questões de concursos, com amplo conhecimento sobre padrões de questões de diferentes bancas e habilidade para selecionar questões adequadas ao nível do candidato.",
        tools=[QuestionAPITool()],
        verbose=True
    )