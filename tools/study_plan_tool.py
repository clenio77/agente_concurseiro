from crewai_tools import Tool
import datetime
import json

class StudyPlanTool(Tool):
    name = "StudyPlanTool"
    description = "Gera um plano de estudos personalizado com base em dados de provas."

    def _run(self, exam_data: str, study_hours: int, months: int) -> str:
        topics = ["Matemática", "Português", "Direito", "Informática", "Conhecimentos Específicos"]
        daily_hours = study_hours / 5  # Assume 5 dias/semana
        plan = {}
        start_date = datetime.datetime.now()
        for i, topic in enumerate(topics):
            plan[f"Semana {i+1}"] = {
                "Tópico": topic,
                "Horas": daily_hours,
                "DataInício": (start_date + datetime.timedelta(days=i*7)).strftime("%Y-%m-%d")
            }
        with open(f"data/study_plans/plano_{start_date.strftime('%Y%m%d')}.json", 'w') as f:
            json.dump(plan, f, indent=2)
        return json.dumps(plan)