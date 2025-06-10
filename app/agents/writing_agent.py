from crewai import Agent
from tools.writing_tool import WritingTool

def create_writing_agent():
    return Agent(
        role="Especialista em Redação",
        goal="Avaliar e fornecer feedback detalhado sobre redações para concursos públicos.",
        backstory="Professor experiente de redação com especialização em textos dissertativos-argumentativos e peças processuais para concursos públicos.",
        tools=[WritingTool()],
        verbose=True
    )