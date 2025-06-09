import json
from typing import Dict, List
from datetime import datetime, timedelta
import uuid

class CalendarIntegrationTool:
    def __init__(self):
        self.name = "CalendarIntegrationTool"
        self.description = "Integra plano de estudos com calendários"
    
    def generate_calendar_events(self, study_plan: Dict, spaced_repetition_plan: Dict = None) -> Dict:
        """Gera eventos de calendário a partir do plano de estudos e repetição espaçada"""
        events = []
        
        # Data de início (hoje)
        start_date = datetime.now().date()
        
        # Gerar eventos a partir do plano de estudos
        if "weekly_schedule" in study_plan:
            for week_idx, week in enumerate(study_plan["weekly_schedule"]):
                week_start = start_date + timedelta(days=week_idx * 7)
                
                # Criar eventos para cada matéria na semana
                for subject, data in week.get("subjects", {}).items():
                    hours = data.get("hours", 0)
                    activity = data.get("activity", "Estudo")
                    
                    # Dividir horas em sessões de 2 horas
                    session_hours = 2
                    sessions = max(1, int(hours / session_hours))
                    hours_per_session = hours / sessions
                    
                    # Criar eventos para cada sessão
                    for session in range(sessions):
                        # Distribuir ao longo da semana
                        day_offset = session % 7
                        event_date = week_start + timedelta(days=day_offset)
                        
                        # Horário (simplificado - apenas durante o dia)
                        start_hour = 8 + (session % 4) * 3  # 8h, 11h, 14h ou 17h
                        
                        event = {
                            "id": str(uuid.uuid4()),
                            "title": f"{subject} - {activity}",
                            "start": datetime.combine(event_date, datetime.min.time().replace(hour=start_hour)).isoformat(),
                            "end": datetime.combine(event_date, datetime.min.time().replace(hour=start_hour + int(hours_per_session))).isoformat(),
                            "description": f"Sessão de estudo: {activity}\nSemana {week['week']}: {week['phase']}\nFoco: {week['focus']}",
                            "type": "study_session"
                        }
                        events.append(event)
        
        # Gerar eventos a partir do plano de repetição espaçada
        if spaced_repetition_plan:
            # Eventos para hoje
            today = start_date
            if "today" in spaced_repetition_plan and spaced_repetition_plan["today"]:
                event = {
                    "id": str(uuid.uuid4()),
                    "title": "Revisão Espaçada",
                    "start": datetime.combine(today, datetime.min.time().replace(hour=20)).isoformat(),
                    "end": datetime.combine(today, datetime.min.time().replace(hour=21)).isoformat(),
                    "description": f"Revisão de {len(spaced_repetition_plan['today'])} itens",
                    "type": "spaced_repetition"
                }
                events.append(event)
            
            # Eventos para amanhã
            tomorrow = today + timedelta(days=1)
            if "tomorrow" in spaced_repetition_plan and spaced_repetition_plan["tomorrow"]:
                event = {
                    "id": str(uuid.uuid4()),
                    "title": "Revisão Espaçada",
                    "start": datetime.combine(tomorrow, datetime.min.time().replace(hour=20)).isoformat(),
                    "end": datetime.combine(tomorrow, datetime.min.time().replace(hour=21)).isoformat(),
                    "description": f"Revisão de {len(spaced_repetition_plan['tomorrow'])} itens",
                    "type": "spaced_repetition"
                }
                events.append(event)
            
            # Eventos para esta semana
            if "this_week" in spaced_repetition_plan and spaced_repetition_plan["this_week"]:
                # Distribuir ao longo da semana
                items_per_day = max(1, len(spaced_repetition_plan["this_week"]) // 5)
                for day in range(2, 7):  # Próximos 5 dias
                    review_date = today + timedelta(days=day)
                    event = {
                        "id": str(uuid.uuid4()),
                        "title": "Revisão Espaçada",
                        "start": datetime.combine(review_date, datetime.min.time().replace(hour=20)).isoformat(),
                        "end": datetime.combine(review_date, datetime.min.time().replace(hour=21)).isoformat(),
                        "description": f"Revisão de aproximadamente {items_per_day} itens",
                        "type": "spaced_repetition"
                    }
                    events.append(event)
        
        # Gerar URLs para exportação
        calendar_urls = {
            "google": self._generate_google_calendar_url(events),
            "ical": "#",  # Placeholder para URL de download iCal
            "outlook": "#"  # Placeholder para URL Outlook
        }
        
        return {
            "events": events,
            "calendar_urls": calendar_urls,
            "total_events": len(events)
        }
    
    def _generate_google_calendar_url(self, events: List[Dict]) -> str:
        """Gera URL para adicionar eventos ao Google Calendar"""
        # Implementação simplificada - na prática, seria necessário gerar URLs reais
        base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
        
        # Usar apenas o primeiro evento para exemplo
        if events:
            event = events[0]
            title = event["title"].replace(" ", "+")
            start = event["start"].replace(":", "").replace("-", "")
            end = event["end"].replace(":", "").replace("-", "")
            details = event["description"].replace(" ", "+")
            
            return f"{base_url}&text={title}&dates={start}/{end}&details={details}"
        
        return base_url
    
    def _run(self, study_plan_json: str, spaced_repetition_plan_json: str = "{}") -> str:
        """Interface principal da ferramenta"""
        try:
            # Converter strings JSON para dicionários
            study_plan = json.loads(study_plan_json)
            spaced_repetition_plan = json.loads(spaced_repetition_plan_json) if spaced_repetition_plan_json else {}
            
            # Gerar eventos de calendário
            calendar_data = self.generate_calendar_events(study_plan, spaced_repetition_plan)
            
            return json.dumps(calendar_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'error': f'Erro na integração com calendário: {str(e)}'
            }, indent=2, ensure_ascii=False)