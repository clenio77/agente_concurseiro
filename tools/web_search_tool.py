from crewai_tools import Tool
from duckduckgo_search import DDG
import os
import requests
from bs4 import BeautifulSoup
import PyPDF2

class WebSearchTool(Tool):
    name = "WebSearchTool"
    description = "Pesquisa na web por provas anteriores e extrai dados relevantes."

    def _run(self, query: str) -> str:
        results = DDG().text(query, max_results=10)
        exam_data = []
        for result in results:
            try:
                response = requests.get(result['href'], timeout=5)
                if response.headers.get('content-type') == 'application/pdf':
                    with open(f"data/previous_exams/{result['title']}.pdf", 'wb') as f:
                        f.write(response.content)
                    exam_data.append(f"PDF salvo: {result['title']}")
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text()
                    exam_data.append(f"Texto extraído de {result['href']}: {text[:500]}...")
            except Exception as e:
                exam_data.append(f"Erro ao processar {result['href']}: {str(e)}")
        return "\n".join(exam_data)