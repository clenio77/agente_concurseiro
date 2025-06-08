from crewai_tools import Tool
import random

class MockExamTool(Tool):
    name = "MockExamTool"
    description = "Gera um simulado com base nos padrões da banca."

    def _run(self, exam_data: str) -> str:
        questions = [
            {
                "question": "Qual é a capital do Brasil?",
                "options": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"],
                "answer": "Brasília"
            },
            {
                "question": "Resolva: 2x + 3 = 7",
                "options": ["x=1", "x=2", "x=3", "x=4"],
                "answer": "x=2"
            }
        ]
        random.shuffle(questions)
        exam_content = ["Simulado\n"]
        for i, q in enumerate(questions, 1):
            exam_content.append(f"{i}. {q['question']}")
            for j, opt in enumerate(q['options'], 1):
                exam_content.append(f"   {j}) {opt}")
            exam_content.append(f"Resposta: {q['answer']}\n")
        return "\n".join(exam_content)