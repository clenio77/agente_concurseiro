import json
from typing import Dict, List

class CoordinationTool:
    def __init__(self):
        self.name = "CoordinationTool"
        self.description = "Coordena diferentes aspectos da preparação para concursos"
    
    def integrate_study_plan(self, study_plan: Dict, materials: List[Dict], writing_feedback: Dict) -> Dict:
        """Integra plano de estudos, materiais e feedback de redação"""
        integrated_plan = {
            "study_plan": study_plan,
            "recommended_materials": self._filter_relevant_materials(study_plan, materials),
            "writing_focus": self._extract_writing_focus(writing_feedback),
            "weekly_schedule": self._generate_weekly_schedule(study_plan, writing_feedback),
            "progress_metrics": self._define_progress_metrics(study_plan)
        }
        
        return integrated_plan
    
    def _filter_relevant_materials(self, study_plan: Dict, materials: List[Dict]) -> Dict:
        """Filtra materiais relevantes para cada tópico do plano de estudos"""
        if not materials:
            return {}
            
        relevant_materials = {}
        
        # Extrair tópicos do plano de estudos
        topics = []
        if "subject_distribution" in study_plan:
            topics = list(study_plan["subject_distribution"].keys())
        elif "weekly_schedule" in study_plan:
            for week in study_plan["weekly_schedule"]:
                if "subjects" in week:
                    topics.extend(list(week["subjects"].keys()))
        
        topics = list(set(topics))  # Remover duplicatas
        
        # Filtrar materiais por tópico
        for topic in topics:
            topic_materials = []
            for material in materials:
                if "subject" in material and topic.lower() in material["subject"].lower():
                    topic_materials.append(material)
            
            if topic_materials:
                relevant_materials[topic] = topic_materials
        
        return relevant_materials
    
    def _extract_writing_focus(self, writing_feedback: Dict) -> Dict:
        """Extrai áreas de foco para melhorar a redação"""
        if not writing_feedback or "feedback" not in writing_feedback:
            return {
                "focus_areas": ["Estrutura", "Argumentação", "Coesão"],
                "recommended_exercises": ["Elaboração de parágrafos", "Conectivos", "Análise de modelos"]
            }
        
        focus_areas = []
        
        # Identificar áreas com pontuação mais baixa
        for criterion, data in writing_feedback["feedback"].items():
            if "score" in data and data["score"] < 7.5:
                focus_areas.append(criterion)
        
        # Se não houver áreas abaixo de 7.5, pegar as duas mais baixas
        if not focus_areas and "feedback" in writing_feedback:
            sorted_criteria = sorted(
                writing_feedback["feedback"].items(),
                key=lambda x: x[1]["score"] if "score" in x[1] else 10
            )
            focus_areas = [criterion for criterion, _ in sorted_criteria[:2]]
        
        # Recomendar exercícios com base nas áreas de foco
        exercises = []
        for area in focus_areas:
            if area == "Estrutura":
                exercises.append("Análise de redações nota 1000")
                exercises.append("Exercícios de organização de parágrafos")
            elif area == "Argumentação":
                exercises.append("Construção de argumentos com base em fatos")
                exercises.append("Exercícios de contra-argumentação")
            elif area == "Gramática":
                exercises.append("Revisão de regras gramaticais")
                exercises.append("Exercícios de concordância e regência")
            elif area == "Coesão":
                exercises.append("Uso de conectivos")
                exercises.append("Exercícios de referenciação")
            elif area == "Adequação ao tema":
                exercises.append("Análise de propostas de redação")
                exercises.append("Delimitação de abordagens temáticas")
        
        return {
            "focus_areas": focus_areas,
            "recommended_exercises": exercises
        }
    
    def _generate_weekly_schedule(self, study_plan: Dict, writing_feedback: Dict) -> List[Dict]:
        """Gera cronograma semanal integrando estudos e prática de redação"""
        weekly_schedule = []
        
        # Extrair cronograma do plano de estudos, se existir
        if "weekly_schedule" in study_plan:
            weekly_schedule = study_plan["weekly_schedule"]
        else:
            # Criar cronograma básico se não existir
            for week in range(1, 5):
                weekly_schedule.append({
                    "week": week,
                    "subjects": {},
                    "activities": []
                })
        
        # Adicionar prática de redação ao cronograma
        writing_focus = self._extract_writing_focus(writing_feedback)
        
        for week in weekly_schedule:
            # Adicionar atividade de redação uma vez por semana
            if week["week"] % 2 == 0:  # A cada duas semanas
                week["activities"].append({
                    "type": "Redação",
                    "description": f"Prática de redação com foco em {', '.join(writing_focus['focus_areas'][:2])}",
                    "duration": "2 horas",
                    "materials": writing_focus["recommended_exercises"][:2]
                })
        
        return weekly_schedule
    
    def _define_progress_metrics(self, study_plan: Dict) -> Dict:
        """Define métricas de progresso para acompanhamento"""
        metrics = {
            "weekly_goals": [],
            "monthly_assessments": [],
            "progress_indicators": {
                "content_coverage": 0,
                "practice_questions": 0,
                "mock_exams": 0,
                "writing_improvement": 0
            }
        }
        
        # Definir metas semanais
        if "weekly_schedule" in study_plan:
            for week in study_plan["weekly_schedule"]:
                if "goals" in week:
                    metrics["weekly_goals"].append({
                        "week": week["week"],
                        "goals": week["goals"]
                    })
        
        # Definir avaliações mensais
        months = 6  # Padrão
        if "metadata" in study_plan and "study_months" in study_plan["metadata"]:
            months = study_plan["metadata"]["study_months"]
        
        for month in range(1, months + 1):
            metrics["monthly_assessments"].append({
                "month": month,
                "assessment_type": "Simulado completo",
                "target_score": 70 + (month * 5)  # Aumenta gradualmente
            })
        
        return metrics
    
    def generate_dashboard_data(self, study_plan: Dict, materials: List[Dict], writing_feedback: Dict) -> Dict:
        """Gera dados para o dashboard"""
        dashboard_data = {
            "progress_summary": {
                "completed_weeks": 0,
                "total_weeks": 24,  # Padrão: 6 meses
                "completion_percentage": 0,
                "current_phase": "Inicial"
            },
            "subject_progress": {},
            "upcoming_activities": [],
            "performance_metrics": {
                "mock_exam_scores": [],
                "writing_scores": [],
                "questions_accuracy": 0
            }
        }
        
        # Extrair informações do plano de estudos
        if "metadata" in study_plan and "total_weeks" in study_plan["metadata"]:
            dashboard_data["progress_summary"]["total_weeks"] = study_plan["metadata"]["total_weeks"]
        
        # Progresso por matéria
        if "subject_distribution" in study_plan:
            for subject, data in study_plan["subject_distribution"].items():
                dashboard_data["subject_progress"][subject] = {
                    "completion": 0,  # Inicialmente 0%
                    "priority": data.get("priority", "Média"),
                    "hours_planned": data.get("hours_per_week", 0) * dashboard_data["progress_summary"]["total_weeks"],
                    "hours_completed": 0
                }
        
        # Atividades próximas
        if "weekly_schedule" in study_plan:
            current_week = dashboard_data["progress_summary"]["completed_weeks"] + 1
            for week in study_plan["weekly_schedule"]:
                if week["week"] >= current_week and week["week"] < current_week + 3:
                    if "activities" in week:
                        for activity in week["activities"]:
                            dashboard_data["upcoming_activities"].append({
                                "week": week["week"],
                                "activity": activity
                            })
        
        # Métricas de desempenho
        if writing_feedback and "score" in writing_feedback:
            dashboard_data["performance_metrics"]["writing_scores"].append({
                "date": writing_feedback.get("created_at", "N/A"),
                "score": writing_feedback["score"]
            })
        
        return dashboard_data
    
    def _run(self, study_plan_json: str, materials_json: str = "[]", writing_feedback_json: str = "{}") -> str:
        """Interface principal da ferramenta"""
        try:
            # Converter strings JSON para dicionários
            study_plan = json.loads(study_plan_json)
            materials = json.loads(materials_json)
            writing_feedback = json.loads(writing_feedback_json)
            
            # Integrar plano de estudos
            integrated_plan = self.integrate_study_plan(study_plan, materials, writing_feedback)
            
            # Gerar dados para dashboard
            dashboard_data = self.generate_dashboard_data(study_plan, materials, writing_feedback)
            
            # Combinar resultados
            result = {
                "integrated_plan": integrated_plan,
                "dashboard_data": dashboard_data
            }
            
            return json.dumps(result, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'error': f'Erro ao coordenar plano: {str(e)}'
            }, indent=2, ensure_ascii=False)
