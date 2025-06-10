import json
from typing import Dict, List
import numpy as np
from datetime import datetime, timedelta

class PerformancePredictionTool:
    def __init__(self):
        self.name = "PerformancePredictionTool"
        self.description = "Prevê desempenho futuro com base em dados históricos"
    
    def predict_performance(self, study_plan: Dict, performance_history: List[Dict], 
                          goal_date: str = None) -> Dict:
        """Prevê desempenho futuro com base no histórico e plano de estudos"""
        predictions = {
            "overall_score": 0,
            "subject_scores": {},
            "success_probability": 0,
            "critical_subjects": [],
            "expected_timeline": {},
            "improvement_rate": 0
        }
        
        # Definir data objetivo
        target_date = None
        if goal_date:
            try:
                target_date = datetime.strptime(goal_date, "%Y-%m-%d").date()
            except:
                # Data padrão: 6 meses a partir de hoje
                target_date = datetime.now().date() + timedelta(days=180)
        else:
            # Data padrão: 6 meses a partir de hoje
            target_date = datetime.now().date() + timedelta(days=180)
        
        # Calcular dias restantes
        days_remaining = (target_date - datetime.now().date()).days
        if days_remaining < 0:
            days_remaining = 0
        
        # Analisar histórico de desempenho
        if performance_history:
            # Ordenar histórico por data
            sorted_history = sorted(performance_history, key=lambda x: x.get("date", ""))
            
            # Extrair pontuações gerais
            overall_scores = [entry.get("overall_score", 0) for entry in sorted_history]
            
            # Calcular taxa de melhoria
            if len(overall_scores) >= 2:
                first_score = overall_scores[0]
                last_score = overall_scores[-1]
                time_span = len(overall_scores)
                
                if time_span > 0:
                    improvement_rate = (last_score - first_score) / time_span
                    predictions["improvement_rate"] = round(improvement_rate, 2)
            
            # Prever pontuação futura
            if predictions["improvement_rate"] > 0 and days_remaining > 0:
                # Estimar quantas avaliações serão feitas até a data objetivo
                assessments_until_goal = days_remaining / 14  # Assumindo uma avaliação a cada 2 semanas
                
                # Prever pontuação final
                predicted_improvement = predictions["improvement_rate"] * assessments_until_goal
                predicted_score = min(100, last_score + predicted_improvement)
                predictions["overall_score"] = round(predicted_score, 1)
            else:
                # Se não houver taxa de melhoria positiva, usar última pontuação
                predictions["overall_score"] = overall_scores[-1] if overall_scores else 0
            
            # Analisar desempenho por matéria
            subject_scores = {}
            for entry in sorted_history:
                if "subject_scores" in entry:
                    for subject, score in entry["subject_scores"].items():
                        if subject not in subject_scores:
                            subject_scores[subject] = []
                        subject_scores[subject].append(score)
            
            # Prever pontuações por matéria
            for subject, scores in subject_scores.items():
                if len(scores) >= 2:
                    # Calcular taxa de melhoria para esta matéria
                    subject_improvement_rate = (scores[-1] - scores[0]) / len(scores)
                    
                    # Prever pontuação final
                    if subject_improvement_rate > 0 and days_remaining > 0:
                        assessments_until_goal = days_remaining / 14
                        predicted_improvement = subject_improvement_rate * assessments_until_goal
                        predicted_score = min(100, scores[-1] + predicted_improvement)
                        predictions["subject_scores"][subject] = round(predicted_score, 1)
                    else:
                        predictions["subject_scores"][subject] = scores[-1]
                else:
                    # Se houver apenas uma pontuação, usá-la como previsão
                    predictions["subject_scores"][subject] = scores[-1]
            
            # Identificar matérias críticas (pontuação < 60)
            predictions["critical_subjects"] = [
                subject for subject, score in predictions["subject_scores"].items() 
                if score < 60
            ]
            
            # Calcular probabilidade de sucesso
            if predictions["overall_score"] >= 80:
                predictions["success_probability"] = 0.9
            elif predictions["overall_score"] >= 70:
                predictions["success_probability"] = 0.7
            elif predictions["overall_score"] >= 60:
                predictions["success_probability"] = 0.5
            else:
                predictions["success_probability"] = 0.3
            
            # Ajustar com base em matérias críticas
            predictions["success_probability"] -= len(predictions["critical_subjects"]) * 0.05
            predictions["success_probability"] = max(0.1, min(0.95, predictions["success_probability"]))
            predictions["success_probability"] = round(predictions["success_probability"], 2)
        
        # Gerar linha do tempo esperada
        if days_remaining > 0:
            # Dividir em marcos de tempo
            milestones = [
                {"days": int(days_remaining * 0.25), "label": "25% do tempo"},
                {"days": int(days_remaining * 0.5), "label": "50% do tempo"},
                {"days": int(days_remaining * 0.75), "label": "75% do tempo"},
                {"days": days_remaining, "label": "Data objetivo"}
            ]
            
            # Calcular pontuações esperadas para cada marco
            for milestone in milestones:
                days = milestone["days"]
                if predictions["improvement_rate"] > 0:
                    assessments = days / 14
                    improvement = predictions["improvement_rate"] * assessments
                    
                    # Última pontuação conhecida
                    last_known_score = overall_scores[-1] if overall_scores else 50
                    
                    # Pontuação esperada neste marco
                    expected_score = min(100, last_known_score + improvement)
                    
                    # Adicionar à linha do tempo
                    milestone_date = (datetime.now().date() + timedelta(days=days)).strftime("%Y-%m-%d")
                    predictions["expected_timeline"][milestone_date] = {
                        "label": milestone["label"],
                        "expected_score": round(expected_score, 1)
                    }
        
        return predictions
    
    def analyze_study_efficiency(self, study_plan: Dict, performance_history: List[Dict]) -> Dict:
        """Analisa a eficiência do plano de estudos com base no desempenho"""
        efficiency = {
            "overall_efficiency": 0,
            "subject_efficiency": {},
            "time_allocation_recommendations": {},
            "study_method_effectiveness": {},
            "optimal_study_pattern": {}
        }
        
        # Verificar se há dados suficientes
        if not performance_history or len(performance_history) < 2:
            efficiency["overall_efficiency"] = 0.5  # Valor padrão
            return efficiency
        
        # Extrair dados de estudo do plano
        study_hours_per_subject = {}
        if study_plan and "subject_distribution" in study_plan:
            for subject, data in study_plan["subject_distribution"].items():
                if "hours_per_week" in data:
                    study_hours_per_subject[subject] = data["hours_per_week"]
        
        # Ordenar histórico por data
        sorted_history = sorted(performance_history, key=lambda x: x.get("date", ""))
        
        # Calcular melhoria por hora de estudo
        if study_hours_per_subject:
            # Extrair pontuações por matéria
            subject_scores = {}
            for entry in sorted_history:
                if "subject_scores" in entry:
                    for subject, score in entry["subject_scores"].items():
                        if subject not in subject_scores:
                            subject_scores[subject] = []
                        subject_scores[subject].append(score)
            
            # Calcular eficiência por matéria
            total_efficiency = 0
            count = 0
            
            for subject, scores in subject_scores.items():
                if len(scores) >= 2 and subject in study_hours_per_subject:
                    # Melhoria total
                    improvement = scores[-1] - scores[0]
                    
                    # Horas totais de estudo
                    weeks = len(scores) - 1  # Assumindo uma avaliação por semana
                    total_hours = study_hours_per_subject[subject] * weeks
                    
                    if total_hours > 0:
                        # Eficiência = melhoria por hora
                        subject_efficiency = improvement / total_hours
                        efficiency["subject_efficiency"][subject] = round(subject_efficiency, 3)
                        
                        total_efficiency += subject_efficiency
                        count += 1
            
            # Calcular eficiência geral
            if count > 0:
                efficiency["overall_efficiency"] = round(total_efficiency / count, 3)
        
        # Gerar recomendações de alocação de tempo
        if efficiency["subject_efficiency"]:
            # Identificar matérias mais e menos eficientes
            sorted_efficiency = sorted(
                efficiency["subject_efficiency"].items(), 
                key=lambda x: x[1]
            )
            
            # Recomendar ajustes
            for subject, eff in sorted_efficiency:
                if eff < 0.05:  # Eficiência muito baixa
                    efficiency["time_allocation_recommendations"][subject] = "Aumentar tempo de estudo e revisar método"
                elif eff < 0.1:  # Eficiência baixa
                    efficiency["time_allocation_recommendations"][subject] = "Aumentar tempo de estudo"
                elif eff > 0.3:  # Eficiência muito alta
                    efficiency["time_allocation_recommendations"][subject] = "Manter ou reduzir tempo, focar em outras matérias"
        
        # Analisar efetividade de métodos de estudo
        study_methods = ["Leitura", "Resumos", "Exercícios", "Flashcards", "Vídeo-aulas"]
        for method in study_methods:
            # Simulação de efetividade
            effectiveness = random.uniform(0.5, 0.9)
            efficiency["study_method_effectiveness"][method] = round(effectiveness, 2)
        
        # Determinar padrão ótimo de estudo
        efficiency["optimal_study_pattern"] = {
            "session_duration": "45 minutos com intervalos de 15 minutos",
            "best_time_of_day": "Manhã (6-10h)",
            "frequency": "Diário, com revisões semanais",
            "recommended_methods": sorted(
                efficiency["study_method_effectiveness"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
        }
        
        return efficiency
    
    def generate_improvement_plan(self, predictions: Dict, efficiency: Dict) -> Dict:
        """Gera plano de melhoria com base nas previsões e análise de eficiência"""
        improvement_plan = {
            "focus_areas": [],
            "time_adjustments": {},
            "method_recommendations": {},
            "milestone_targets": {},
            "critical_interventions": []
        }
        
        # Definir áreas de foco (matérias críticas)
        improvement_plan["focus_areas"] = predictions.get("critical_subjects", [])
        
        # Ajustes de tempo com base na eficiência
        if "subject_efficiency" in efficiency and "time_allocation_recommendations" in efficiency:
            improvement_plan["time_adjustments"] = efficiency["time_allocation_recommendations"]
        
        # Recomendações de métodos
        if "study_method_effectiveness" in efficiency:
            methods = efficiency["study_method_effectiveness"]
            sorted_methods = sorted(methods.items(), key=lambda x: x[1], reverse=True)
            
            # Recomendar métodos mais eficazes para matérias críticas
            for subject in improvement_plan["focus_areas"]:
                improvement_plan["method_recommendations"][subject] = [
                    method for method, _ in sorted_methods[:2]
                ]
        
        # Definir metas para marcos de tempo
        if "expected_timeline" in predictions:
            for date, data in predictions["expected_timeline"].items():
                improvement_plan["milestone_targets"][date] = {
                    "label": data["label"],
                    "target_score": min(data["expected_score"] + 5, 100)  # Meta 5 pontos acima da previsão
                }
        
        # Intervenções críticas para matérias problemáticas
        for subject in improvement_plan["focus_areas"]:
            intervention = {
                "subject": subject,
                "action": "Intensificar estudos com foco em exercícios práticos",
                "duration": "2 semanas",
                "expected_improvement": "10-15 pontos"
            }
            improvement_plan["critical_interventions"].append(intervention)
        
        return improvement_plan
    
    def _run(self, study_plan_json: str, performance_history_json: str, goal_date: str = None) -> str:
        """Interface principal da ferramenta"""
        try:
            # Converter strings JSON para dicionários
            study_plan = json.loads(study_plan_json)
            performance_history = json.loads(performance_history_json)
            
            # Prever desempenho
            predictions = self.predict_performance(study_plan, performance_history, goal_date)
            
            # Analisar eficiência do estudo
            efficiency = self.analyze_study_efficiency(study_plan, performance_history)
            
            # Gerar plano de melhoria
            improvement_plan = self.generate_improvement_plan(predictions, efficiency)
            
            # Combinar resultados
            result = {
                "predictions": predictions,
                "study_efficiency": efficiency,
                "improvement_plan": improvement_plan,
                "summary": f"Previsão de pontuação final: {predictions['overall_score']}, Probabilidade de sucesso: {predictions['success_probability'] * 100}%"
            }
            
            return json.dumps(result, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'error': f'Erro na previsão de desempenho: {str(e)}'
            }, indent=2, ensure_ascii=False)
