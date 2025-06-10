import json
from typing import Dict, List
from datetime import datetime, timedelta
import math

class SpacedRepetitionTool:
    def __init__(self):
        self.name = "SpacedRepetitionTool"
        self.description = "Gerencia sistema de repetição espaçada para otimizar memorização"
    
    def schedule_review(self, items: List[Dict], performance_history: Dict = None) -> Dict:
        """Agenda revisões usando algoritmo de repetição espaçada"""
        schedule = {
            "today": [],
            "tomorrow": [],
            "this_week": [],
            "next_week": [],
            "later": [],
            "metadata": {
                "total_items": len(items),
                "priority_distribution": {}
            }
        }
        
        today = datetime.now().date()
        
        # Processar cada item
        for item in items:
            # Obter dados do item
            item_id = item.get("id", "unknown")
            difficulty = item.get("difficulty", 5)  # Escala 1-10
            priority = item.get("priority", "Média")
            last_review = item.get("last_review")
            
            # Converter last_review para data
            if last_review:
                try:
                    last_review_date = datetime.strptime(last_review, "%Y-%m-%d").date()
                except:
                    last_review_date = today - timedelta(days=30)  # Fallback
            else:
                last_review_date = today - timedelta(days=30)  # Nunca revisado
            
            # Obter histórico de desempenho para este item
            item_history = performance_history.get(item_id, []) if performance_history else []
            
            # Calcular intervalo de repetição
            interval = self._calculate_interval(difficulty, item_history, priority)
            
            # Calcular próxima data de revisão
            next_review = last_review_date + timedelta(days=interval)
            
            # Adicionar à categoria apropriada
            review_item = {
                "id": item_id,
                "content": item.get("content", ""),
                "subject": item.get("subject", ""),
                "difficulty": difficulty,
                "priority": priority,
                "next_review": next_review.strftime("%Y-%m-%d")
            }
            
            days_until_review = (next_review - today).days
            
            if days_until_review <= 0:
                schedule["today"].append(review_item)
            elif days_until_review == 1:
                schedule["tomorrow"].append(review_item)
            elif days_until_review <= 7:
                schedule["this_week"].append(review_item)
            elif days_until_review <= 14:
                schedule["next_week"].append(review_item)
            else:
                schedule["later"].append(review_item)
            
            # Atualizar distribuição de prioridade
            schedule["metadata"]["priority_distribution"][priority] = schedule["metadata"]["priority_distribution"].get(priority, 0) + 1
        
        # Ordenar itens por prioridade e dificuldade
        priority_order = {"Alta": 3, "Média": 2, "Baixa": 1}
        for key in ["today", "tomorrow", "this_week", "next_week", "later"]:
            schedule[key].sort(key=lambda x: (priority_order.get(x["priority"], 0), x["difficulty"]), reverse=True)
        
        return schedule
    
    def _calculate_interval(self, difficulty: int, history: List[Dict], priority: str) -> int:
        """Calcula intervalo de repetição baseado no algoritmo SM-2 modificado"""
        # Fatores de base para o algoritmo
        base_interval = 1
        ease_factor = 2.5
        
        # Ajustar com base na dificuldade (1-10)
        difficulty_factor = 1 - (difficulty / 10)  # Mais difícil = intervalo menor
        
        # Ajustar com base na prioridade
        priority_factor = {
            "Alta": 0.7,    # Intervalos menores para alta prioridade
            "Média": 1.0,   # Intervalo padrão
            "Baixa": 1.3    # Intervalos maiores para baixa prioridade
        }.get(priority, 1.0)
        
        # Processar histórico de revisões
        if history:
            # Ordenar histórico por data
            sorted_history = sorted(history, key=lambda x: x.get("date", ""))
            
            # Obter último desempenho
            last_performance = sorted_history[-1]
            quality = last_performance.get("quality", 3)  # Escala 0-5
            
            # Calcular novo ease factor
            ease_factor = max(1.3, ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
            
            # Calcular novo intervalo
            if quality < 3:
                # Resposta incorreta, voltar ao início
                base_interval = 1
            else:
                # Resposta correta, aumentar intervalo
                if len(sorted_history) == 1:
                    base_interval = 1
                elif len(sorted_history) == 2:
                    base_interval = 6
                else:
                    # Intervalo anterior * ease factor
                    prev_interval = (datetime.strptime(sorted_history[-1]["date"], "%Y-%m-%d") - 
                                    datetime.strptime(sorted_history[-2]["date"], "%Y-%m-%d")).days
                    base_interval = int(prev_interval * ease_factor)
        
        # Aplicar fatores de ajuste
        adjusted_interval = max(1, int(base_interval * difficulty_factor * priority_factor))
        
        # Limitar intervalo máximo a 60 dias
        return min(adjusted_interval, 60)
    
    def update_item_performance(self, item_id: str, quality: int, items: List[Dict], 
                               performance_history: Dict) -> Dict:
        """Atualiza histórico de desempenho de um item"""
        # Inicializar histórico se não existir
        if item_id not in performance_history:
            performance_history[item_id] = []
        
        # Adicionar nova entrada de desempenho
        performance_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "quality": quality,
            "timestamp": datetime.now().isoformat()
        }
        
        performance_history[item_id].append(performance_entry)
        
        # Atualizar last_review no item
        for item in items:
            if item.get("id") == item_id:
                item["last_review"] = datetime.now().strftime("%Y-%m-%d")
                break
        
        # Calcular estatísticas
        stats = self._calculate_performance_stats(item_id, performance_history)
        
        return {
            "updated_history": performance_history,
            "updated_items": items,
            "stats": stats
        }
    
    def _calculate_performance_stats(self, item_id: str, performance_history: Dict) -> Dict:
        """Calcula estatísticas de desempenho para um item"""
        if item_id not in performance_history:
            return {"average_quality": 0, "review_count": 0, "mastery_level": "Não iniciado"}
        
        history = performance_history[item_id]
        
        # Calcular média de qualidade
        qualities = [entry.get("quality", 0) for entry in history]
        avg_quality = sum(qualities) / len(qualities) if qualities else 0
        
        # Determinar nível de domínio
        mastery_level = "Não iniciado"
        if len(history) >= 5 and avg_quality >= 4.5:
            mastery_level = "Dominado"
        elif len(history) >= 3 and avg_quality >= 4.0:
            mastery_level = "Proficiente"
        elif len(history) >= 2 and avg_quality >= 3.0:
            mastery_level = "Familiar"
        elif len(history) >= 1:
            mastery_level = "Iniciante"
        
        return {
            "average_quality": round(avg_quality, 2),
            "review_count": len(history),
            "mastery_level": mastery_level,
            "last_review": history[-1]["date"] if history else None
        }
    
    def generate_daily_review_plan(self, items: List[Dict], performance_history: Dict = None, 
                                 max_items: int = 20) -> Dict:
        """Gera plano diário de revisão"""
        # Agendar revisões
        schedule = self.schedule_review(items, performance_history)
        
        # Selecionar itens para hoje
        today_items = schedule["today"]
        
        # Se não houver itens suficientes para hoje, adicionar de amanhã
        if len(today_items) < max_items and schedule["tomorrow"]:
            remaining = max_items - len(today_items)
            today_items.extend(schedule["tomorrow"][:remaining])
        
        # Se ainda não houver itens suficientes, adicionar desta semana
        if len(today_items) < max_items and schedule["this_week"]:
            remaining = max_items - len(today_items)
            today_items.extend(schedule["this_week"][:remaining])
        
        # Limitar ao máximo de itens
        today_items = today_items[:max_items]
        
        # Organizar por assunto
        by_subject = {}
        for item in today_items:
            subject = item.get("subject", "Outros")
            if subject not in by_subject:
                by_subject[subject] = []
            by_subject[subject].append(item)
        
        # Calcular estatísticas
        stats = {
            "total_items": len(today_items),
            "subjects_count": len(by_subject),
            "priority_distribution": {
                "Alta": len([i for i in today_items if i.get("priority") == "Alta"]),
                "Média": len([i for i in today_items if i.get("priority") == "Média"]),
                "Baixa": len([i for i in today_items if i.get("priority") == "Baixa"])
            },
            "estimated_time": len(today_items) * 3  # Estimativa: 3 minutos por item
        }
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "items": today_items,
            "by_subject": by_subject,
            "stats": stats
        }
    
    def calculate_user_stats(self, performance_history: Dict) -> Dict:
        """Calcula estatísticas gerais do usuário e elementos de gamificação"""
        stats = {
            "total_reviews": 0,
            "mastery_levels": {
                "Dominado": 0,
                "Proficiente": 0,
                "Familiar": 0,
                "Iniciante": 0,
                "Não iniciado": 0
            },
            "streak": 0,
            "longest_streak": 0,
            "points": 0,
            "level": 1,
            "achievements": []
        }
        
        if not performance_history:
            return stats
        
        # Calcular total de revisões
        total_reviews = sum(len(history) for history in performance_history.values())
        stats["total_reviews"] = total_reviews
        
        # Calcular pontos (5 por revisão)
        stats["points"] = total_reviews * 5
        
        # Calcular nível (1 nível a cada 100 pontos)
        stats["level"] = max(1, stats["points"] // 100 + 1)
        
        # Calcular distribuição de níveis de domínio
        for item_id, history in performance_history.items():
            item_stats = self._calculate_performance_stats(item_id, performance_history)
            mastery = item_stats["mastery_level"]
            stats["mastery_levels"][mastery] = stats["mastery_levels"].get(mastery, 0) + 1
        
        # Calcular sequência atual e mais longa
        dates = []
        for item_id, history in performance_history.items():
            for entry in history:
                if "date" in entry:
                    dates.append(entry["date"])
        
        if dates:
            # Ordenar datas
            dates = sorted(set(dates))
            
            # Verificar sequência atual
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)
            if yesterday.strftime("%Y-%m-%d") in dates or today.strftime("%Y-%m-%d") in dates:
                # Contar dias consecutivos
                streak = 1
                check_date = yesterday
                while check_date.strftime("%Y-%m-%d") in dates:
                    streak += 1
                    check_date = check_date - timedelta(days=1)
                stats["streak"] = streak
        
            # Calcular sequência mais longa
            longest = 1
            current = 1
            for i in range(1, len(dates)):
                date1 = datetime.strptime(dates[i-1], "%Y-%m-%d").date()
                date2 = datetime.strptime(dates[i], "%Y-%m-%d").date()
                if (date2 - date1).days == 1:
                    current += 1
                    longest = max(longest, current)
                else:
                    current = 1
            stats["longest_streak"] = longest
        
        # Definir conquistas
        achievements = []
        if stats["total_reviews"] >= 100:
            achievements.append({"name": "Centenário", "description": "Completou 100 revisões"})
        if stats["streak"] >= 7:
            achievements.append({"name": "Consistente", "description": "Manteve uma sequência de 7 dias"})
        if stats["mastery_levels"]["Dominado"] >= 10:
            achievements.append({"name": "Mestre", "description": "Dominou 10 itens"})
        if stats["level"] >= 5:
            achievements.append({"name": "Veterano", "description": "Alcançou o nível 5"})
        
        stats["achievements"] = achievements
        
        return stats
    
    def _run(self, items_json: str, performance_history_json: str = "{}", action: str = "schedule", 
           item_id: str = None, quality: int = None, max_items: int = 20) -> str:
        """Interface principal da ferramenta"""
        try:
            # Converter strings JSON para dicionários
            items = json.loads(items_json)
            performance_history = json.loads(performance_history_json)
            
            # Executar ação solicitada
            if action == "schedule":
                result = self.schedule_review(items, performance_history)
            elif action == "update" and item_id and quality is not None:
                result = self.update_item_performance(item_id, quality, items, performance_history)
            elif action == "daily_plan":
                result = self.generate_daily_review_plan(items, performance_history, max_items)
            else:
                result = {"error": "Ação inválida ou parâmetros incompletos"}
            
            return json.dumps(result, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'error': f'Erro na ferramenta de repetição espaçada: {str(e)}'
            }, indent=2, ensure_ascii=False)
