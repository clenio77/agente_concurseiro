import json
from typing import Dict, List
import numpy as np
from datetime import datetime, timedelta

class RecommendationTool:
    def __init__(self):
        self.name = "RecommendationTool"
        self.description = "Gera recomendações personalizadas de estudo e materiais"
    
    def generate_recommendations(self, user_profile: Dict, study_plan: Dict, 
                                performance_data: Dict, available_materials: List[Dict]) -> Dict:
        """Gera recomendações personalizadas com base no perfil e desempenho"""
        recommendations = {
            "priority_subjects": [],
            "recommended_materials": [],
            "daily_focus": {},
            "weak_areas": [],
            "next_steps": [],
            "time_optimization": {}
        }
        
        # Identificar áreas prioritárias com base no desempenho
        if "performance" in performance_data:
            weak_subjects = self._identify_weak_subjects(performance_data["performance"])
            recommendations["weak_areas"] = weak_subjects
            
            # Priorizar áreas fracas, mas manter equilíbrio com o plano original
            recommendations["priority_subjects"] = self._balance_priorities(
                weak_subjects, 
                study_plan.get("subject_distribution", {})
            )
        else:
            # Se não houver dados de desempenho, usar distribuição do plano
            if "subject_distribution" in study_plan:
                recommendations["priority_subjects"] = [
                    {"subject": subject, "priority": data.get("priority", "Média")}
                    for subject, data in study_plan["subject_distribution"].items()
                ]
        
        # Recomendar materiais específicos
        if available_materials:
            recommendations["recommended_materials"] = self._recommend_materials(
                recommendations["priority_subjects"],
                available_materials,
                user_profile.get("learning_style", "Visual")
            )
        
        # Gerar foco diário (rotação de assuntos)
        recommendations["daily_focus"] = self._generate_daily_focus(
            recommendations["priority_subjects"]
        )
        
        # Próximos passos
        recommendations["next_steps"] = self._suggest_next_steps(
            performance_data, 
            study_plan,
            user_profile.get("goal_date")
        )
        
        # Otimização de tempo
        recommendations["time_optimization"] = self._optimize_study_time(
            user_profile.get("available_hours", {}),
            recommendations["priority_subjects"]
        )
        
        return recommendations
    
    def _identify_weak_subjects(self, performance: Dict) -> List[Dict]:
        """Identifica áreas com desempenho mais fraco"""
        weak_areas = []
        
        # Ordenar assuntos por desempenho (do pior para o melhor)
        if "subjects" in performance:
            sorted_subjects = sorted(
                performance["subjects"].items(),
                key=lambda x: x[1].get("score", 100)
            )
            
            # Selecionar os 3 piores ou todos se houver menos de 3
            for subject, data in sorted_subjects[:3]:
                score = data.get("score", 0)
                weak_areas.append({
                    "subject": subject,
                    "score": score,
                    "priority": "Alta" if score < 60 else "Média" if score < 75 else "Baixa"
                })
        
        return weak_areas
    
    def _balance_priorities(self, weak_subjects: List[Dict], original_distribution: Dict) -> List[Dict]:
        """Equilibra prioridades entre áreas fracas e distribuição original"""
        balanced_priorities = []
        
        # Primeiro, incluir áreas fracas
        weak_subject_names = [item["subject"] for item in weak_subjects]
        balanced_priorities.extend(weak_subjects)
        
        # Depois, incluir outras áreas do plano original que não estão nas áreas fracas
        for subject, data in original_distribution.items():
            if subject not in weak_subject_names:
                balanced_priorities.append({
                    "subject": subject,
                    "priority": data.get("priority", "Média"),
                    "weight": data.get("weight", 10)
                })
        
        # Ordenar por prioridade
        priority_order = {"Alta": 3, "Média": 2, "Baixa": 1}
        balanced_priorities.sort(
            key=lambda x: (priority_order.get(x.get("priority", "Média"), 0), 
                          x.get("weight", 0)), 
            reverse=True
        )
        
        return balanced_priorities
    
    def _recommend_materials(self, priority_subjects: List[Dict], 
                           available_materials: List[Dict],
                           learning_style: str) -> List[Dict]:
        """Recomenda materiais específicos para cada assunto prioritário"""
        recommendations = []
        
        # Filtrar por estilo de aprendizagem
        style_preference = {
            "Visual": ["vídeo", "infográfico", "mapa mental"],
            "Auditivo": ["áudio", "podcast", "videoaula"],
            "Leitura/Escrita": ["livro", "apostila", "resumo"],
            "Cinestésico": ["exercício", "simulado", "prática"]
        }
        
        preferred_types = style_preference.get(learning_style, ["vídeo", "livro", "exercício"])
        
        # Recomendar para cada assunto prioritário
        for priority_item in priority_subjects[:5]:  # Limitar a 5 assuntos
            subject = priority_item["subject"]
            
            # Filtrar materiais por assunto
            subject_materials = [
                material for material in available_materials
                if material.get("subject", "").lower() == subject.lower()
            ]
            
            # Ordenar por tipo preferido e depois por avaliação
            sorted_materials = sorted(
                subject_materials,
                key=lambda x: (
                    1 if x.get("type", "") in preferred_types else 0,
                    x.get("rating", 0)
                ),
                reverse=True
            )
            
            # Selecionar os 3 melhores materiais
            best_materials = sorted_materials[:3]
            if best_materials:
                recommendations.append({
                    "subject": subject,
                    "materials": best_materials
                })
        
        return recommendations
    
    def _generate_daily_focus(self, priority_subjects: List[Dict]) -> Dict:
        """Gera foco diário com rotação de assuntos"""
        daily_focus = {}
        days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        
        # Obter lista de assuntos
        subjects = [item["subject"] for item in priority_subjects]
        
        # Garantir que temos assuntos suficientes (repetir se necessário)
        while len(subjects) < len(days):
            subjects.extend(subjects[:len(days)-len(subjects)])
        
        # Distribuir assuntos pelos dias da semana
        for i, day in enumerate(days):
            # Assunto principal do dia
            main_subject = subjects[i % len(subjects)]
            
            # Assunto secundário (próximo na lista)
            secondary_subject = subjects[(i + 1) % len(subjects)]
            
            daily_focus[day] = {
                "main_focus": main_subject,
                "secondary_focus": secondary_subject,
                "review": subjects[(i + 3) % len(subjects)]  # Revisão de um assunto visto há alguns dias
            }
        
        return daily_focus
    
    def _suggest_next_steps(self, performance_data: Dict, study_plan: Dict, goal_date: str = None) -> List[str]:
        """Sugere próximos passos com base no desempenho e plano"""
        next_steps = []
        
        # Verificar progresso geral
        progress = performance_data.get("overall_progress", 0)
        
        # Verificar proximidade da data objetivo
        days_remaining = 180  # Padrão: 6 meses
        if goal_date:
            try:
                goal_datetime = datetime.strptime(goal_date, "%Y-%m-%d")
                days_remaining = (goal_datetime - datetime.now()).days
                if days_remaining < 0:
                    days_remaining = 0
            except:
                pass
        
        # Sugestões baseadas no tempo restante
        if days_remaining < 30:
            next_steps.append("Foco em revisão e simulados completos")
            next_steps.append("Priorize questões de provas anteriores da banca")
        elif days_remaining < 90:
            next_steps.append("Intensifique estudos em áreas de baixo desempenho")
            next_steps.append("Realize simulados semanais")
        else:
            next_steps.append("Siga o plano de estudos com foco em construir base sólida")
            next_steps.append("Faça questões específicas por assunto")
        
        # Sugestões baseadas no progresso
        if progress < 30:
            next_steps.append("Concentre-se em entender os conceitos fundamentais")
        elif progress < 70:
            next_steps.append("Aprofunde o conhecimento com questões de média dificuldade")
        else:
            next_steps.append("Foque em questões avançadas e pontos específicos")
        
        # Sugestões baseadas em áreas fracas
        if "weak_areas" in performance_data and performance_data["weak_areas"]:
            weak_area = performance_data["weak_areas"][0]["subject"]
            next_steps.append(f"Dedique tempo extra para {weak_area}")
        
        return next_steps
    
    def _optimize_study_time(self, available_hours: Dict, priority_subjects: List[Dict]) -> Dict:
        """Otimiza distribuição de tempo de estudo"""
        optimization = {
            "distribution": {},
            "best_times": {},
            "session_duration": {}
        }
        
        # Total de horas disponíveis
        total_hours = sum(available_hours.values()) if available_hours else 10
        
        # Distribuir horas por assunto com base na prioridade
        priority_weights = {"Alta": 3, "Média": 2, "Baixa": 1}
        total_weight = sum(priority_weights.get(item.get("priority", "Média"), 1) for item in priority_subjects)
        
        for item in priority_subjects:
            subject = item["subject"]
            priority = item.get("priority", "Média")
            weight = priority_weights.get(priority, 1)
            
            # Calcular horas proporcionais ao peso
            subject_hours = (weight / total_weight) * total_hours if total_weight > 0 else total_hours / len(priority_subjects)
            optimization["distribution"][subject] = round(subject_hours, 1)
        
        # Determinar melhores horários para estudo
        if available_hours:
            # Ordenar horários por disponibilidade
            sorted_hours = sorted(available_hours.items(), key=lambda x: x[1], reverse=True)
            
            # Atribuir assuntos mais prioritários aos horários mais disponíveis
            for i, item in enumerate(priority_subjects):
                if i < len(sorted_hours):
                    optimization["best_times"][item["subject"]] = sorted_hours[i][0]
        
        # Sugerir duração de sessões
        for item in priority_subjects:
            subject = item["subject"]
            priority = item.get("priority", "Média")
            
            if priority == "Alta":
                optimization["session_duration"][subject] = "45-60 minutos"
            elif priority == "Média":
                optimization["session_duration"][subject] = "30-45 minutos"
            else:
                optimization["session_duration"][subject] = "20-30 minutos"
        
        return optimization
    
    def _run(self, user_profile_json: str, study_plan_json: str, 
            performance_data_json: str, available_materials_json: str = "[]") -> str:
        """Interface principal da ferramenta"""
        try:
            # Converter strings JSON para dicionários
            user_profile = json.loads(user_profile_json)
            study_plan = json.loads(study_plan_json)
            performance_data = json.loads(performance_data_json)
            available_materials = json.loads(available_materials_json)
            
            # Gerar recomendações
            recommendations = self.generate_recommendations(
                user_profile, study_plan, performance_data, available_materials
            )
            
            return json.dumps(recommendations, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'error': f'Erro ao gerar recomendações: {str(e)}'
            }, indent=2, ensure_ascii=False)