import json
from typing import Dict, List
from datetime import datetime, timedelta
import math

class ProgressTrackingTool:
    def __init__(self):
        self.name = "ProgressTrackingTool"
        self.description = "Acompanha e analisa o progresso do estudante"
    
    def analyze_progress(self, study_plan: Dict, performance_history: List[Dict], 
                        spaced_repetition_data: Dict = None) -> Dict:
        """Analisa o progresso do estudante em relação ao plano de estudos"""
        progress = {
            "overall_completion": 0,
            "subject_completion": {},
            "time_tracking": {
                "planned_hours": 0,
                "completed_hours": 0,
                "efficiency": 0
            },
            "learning_curve": [],
            "milestones": {
                "completed": [],
                "upcoming": []
            },
            "recommendations": []
        }
        
        # Calcular horas planejadas
        if "subject_distribution" in study_plan:
            for subject, data in study_plan["subject_distribution"].items():
                if "hours_per_week" in data:
                    progress["time_tracking"]["planned_hours"] += data["hours_per_week"]
        
        # Multiplicar por número de semanas
        weeks = study_plan.get("duration_weeks", 24)  # Padrão: 6 meses
        progress["time_tracking"]["planned_hours"] *= weeks
        
        # Calcular horas completadas (simulado)
        if performance_history:
            # Assumir que cada entrada de desempenho representa uma semana de estudo
            weeks_completed = len(performance_history)
            
            # Estimar horas completadas
            if "subject_distribution" in study_plan:
                weekly_hours = sum(data.get("hours_per_week", 0) for data in study_plan["subject_distribution"].values())
                progress["time_tracking"]["completed_hours"] = weekly_hours * weeks_completed
        
        # Calcular eficiência (pontuação média / horas de estudo)
        if progress["time_tracking"]["completed_hours"] > 0 and performance_history:
            total_score = sum(entry.get("overall_score", 0) for entry in performance_history)
            avg_score = total_score / len(performance_history) if performance_history else 0
            
            # Eficiência = pontos por hora de estudo
            if progress["time_tracking"]["completed_hours"] > 0:
                progress["time_tracking"]["efficiency"] = round(avg_score / progress["time_tracking"]["completed_hours"] * 10, 2)
        
        # Calcular conclusão geral
        if progress["time_tracking"]["planned_hours"] > 0:
            progress["overall_completion"] = round(
                (progress["time_tracking"]["completed_hours"] / progress["time_tracking"]["planned_hours"]) * 100, 1
            )
        
        # Calcular conclusão por matéria
        if "subject_distribution" in study_plan and performance_history:
            for subject, data in study_plan["subject_distribution"].items():
                # Horas planejadas para esta matéria
                planned_hours = data.get("hours_per_week", 0) * weeks
                
                # Estimar horas completadas
                completed_hours = data.get("hours_per_week", 0) * weeks_completed
                
                # Calcular porcentagem de conclusão
                if planned_hours > 0:
                    completion = (completed_hours / planned_hours) * 100
                else:
                    completion = 0
                
                # Obter pontuação mais recente para esta matéria
                latest_score = 0
                if performance_history:
                    latest_entry = performance_history[-1]
                    if "subject_scores" in latest_entry and subject in latest_entry["subject_scores"]:
                        latest_score = latest_entry["subject_scores"][subject]
                
                progress["subject_completion"][subject] = {
                    "completion_percentage": round(completion, 1),
                    "planned_hours": planned_hours,
                    "completed_hours": completed_hours,
                    "latest_score": latest_score
                }
        
        # Gerar curva de aprendizado
        if performance_history:
            for i, entry in enumerate(performance_history):
                week = i + 1
                progress["learning_curve"].append({
                    "week": week,
                    "overall_score": entry.get("overall_score", 0),
                    "subject_scores": entry.get("subject_scores", {})
                })
        
        # Identificar marcos concluídos e próximos
        if "weekly_schedule" in study_plan:
            for i, week in enumerate(study_plan["weekly_schedule"]):
                milestone = {
                    "week": week["week"],
                    "phase": week["phase"],
                    "focus": week["focus"]
                }
                
                # Determinar se o marco foi concluído
                if i < weeks_completed:
                    progress["milestones"]["completed"].append(milestone)
                else:
                    progress["milestones"]["upcoming"].append(milestone)
                    # Limitar a 3 próximos marcos
                    if len(progress["milestones"]["upcoming"]) >= 3:
                        break
        
        # Gerar recomendações com base no progresso
        self._generate_progress_recommendations(progress, study_plan, performance_history, spaced_repetition_data)
        
        return progress
    
    def _generate_progress_recommendations(self, progress: Dict, study_plan: Dict, 
                                         performance_history: List[Dict], 
                                         spaced_repetition_data: Dict = None) -> None:
        """Gera recomendações com base na análise de progresso"""
        recommendations = []
        
        # Verificar se está atrasado no cronograma
        if progress["overall_completion"] < 90 and len(progress["milestones"]["completed"]) > 0:
            expected_completion = (len(progress["milestones"]["completed"]) / 
                                 (len(progress["milestones"]["completed"]) + len(progress["milestones"]["upcoming"]))) * 100
            
            if progress["overall_completion"] < expected_completion - 10:
                recommendations.append({
                    "type": "warning",
                    "title": "Atraso no cronograma",
                    "description": f"Você está {expected_completion - progress['overall_completion']:.1f}% atrasado em relação ao cronograma previsto.",
                    "action": "Considere aumentar suas horas de estudo semanais ou revisar a distribuição de tempo."
                })
        
        # Identificar matérias com baixo desempenho
        low_performance_subjects = []
        for subject, data in progress["subject_completion"].items():
            if data["latest_score"] < 60:
                low_performance_subjects.append(subject)
        
        if low_performance_subjects:
            recommendations.append({
                "type": "alert",
                "title": "Matérias com baixo desempenho",
                "description": f"As seguintes matérias estão com desempenho abaixo do esperado: {', '.join(low_performance_subjects)}",
                "action": "Dedique mais tempo a estas matérias e considere mudar seu método de estudo."
            })
        
        # Verificar eficiência de estudo
        if progress["time_tracking"]["efficiency"] < 0.5:
            recommendations.append({
                "type": "suggestion",
                "title": "Baixa eficiência de estudo",
                "description": "Sua eficiência de estudo está abaixo do ideal.",
                "action": "Experimente técnicas como Pomodoro, estudo ativo ou mudança de ambiente."
            })
        
        # Verificar uso da repetição espaçada
        if spaced_repetition_data and "today" in spaced_repetition_data:
            pending_reviews = len(spaced_repetition_data["today"])
            if pending_reviews > 10:
                recommendations.append({
                    "type": "reminder",
                    "title": "Revisões pendentes",
                    "description": f"Você tem {pending_reviews} itens aguardando revisão hoje.",
                    "action": "Complete suas revisões diárias para maximizar