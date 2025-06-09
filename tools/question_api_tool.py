import json
import random
from typing import Dict, List
import requests
from datetime import datetime

class QuestionAPITool:
    def __init__(self):
        self.name = "QuestionAPITool"
        self.description = "Integra com APIs de questões de concursos"
        self.api_base_url = "https://api.example.com/questions"  # URL fictícia
    
    def fetch_questions(self, subjects: List[str], difficulty: str = "medium", 
                       count: int = 10, banca: str = None) -> List[Dict]:
        """Busca questões de uma API externa (simulada)"""
        # Simulação de resposta da API
        questions = []
        
        for _ in range(count):
            subject = random.choice(subjects)
            
            # Gerar questão simulada
            question = {
                "id": f"q{random.randint(1000, 9999)}",
                "subject": subject,
                "difficulty": difficulty,
                "banca": banca or "CESPE",
                "year": random.randint(2015, 2023),
                "text": f"Questão sobre {subject} com dificuldade {difficulty}.",
                "options": [
                    {"id": "a", "text": f"Opção A para {subject}"},
                    {"id": "b", "text": f"Opção B para {subject}"},
                    {"id": "c", "text": f"Opção C para {subject}"},
                    {"id": "d", "text": f"Opção D para {subject}"},
                    {"id": "e", "text": f"Opção E para {subject}"}
                ],
                "answer": random.choice(["a", "b", "c", "d", "e"]),
                "explanation": f"Explicação detalhada sobre a resposta correta para {subject}."
            }
            
            questions.append(question)
        
        return questions
    
    def generate_daily_quiz(self, study_plan: Dict, performance_history: List[Dict] = None) -> Dict:
        """Gera um quiz diário com base no plano de estudos e histórico de desempenho"""
        quiz = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": "Quiz Diário",
            "questions": [],
            "focus_subjects": [],
            "difficulty": "medium",
            "estimated_time": "15 minutos"
        }
        
        # Determinar matérias de foco
        focus_subjects = []
        
        if study_plan and "subject_distribution" in study_plan:
            # Extrair todas as matérias
            all_subjects = list(study_plan["subject_distribution"].keys())
            
            # Identificar matérias com baixo desempenho
            low_performance_subjects = []
            if performance_history and len(performance_history) > 0:
                latest_performance = performance_history[-1]
                if "subject_scores" in latest_performance:
                    for subject, score in latest_performance["subject_scores"].items():
                        if score < 70 and subject in all_subjects:
                            low_performance_subjects.append(subject)
            
            # Priorizar matérias com baixo desempenho
            if low_performance_subjects:
                focus_subjects = low_performance_subjects[:3]  # Até 3 matérias com baixo desempenho
            
            # Completar com outras matérias se necessário
            remaining_slots = 3 - len(focus_subjects)
            if remaining_slots > 0:
                other_subjects = [s for s in all_subjects if s not in focus_subjects]
                if other_subjects:
                    focus_subjects.extend(random.sample(other_subjects, min(remaining_slots, len(other_subjects))))
        
        # Se não houver matérias de foco, usar padrões
        if not focus_subjects:
            focus_subjects = ["Português", "Matemática", "Conhecimentos Específicos"]
        
        quiz["focus_subjects"] = focus_subjects
        
        # Determinar dificuldade
        difficulty = "medium"
        if performance_history and len(performance_history) > 0:
            latest_performance = performance_history[-1]
            overall_score = latest_performance.get("overall_score", 0)
            
            if overall_score >= 80:
                difficulty = "hard"
            elif overall_score <= 50:
                difficulty = "easy"
        
        quiz["difficulty"] = difficulty
        
        # Buscar questões
        questions = self.fetch_questions(
            subjects=focus_subjects,
            difficulty=difficulty,
            count=10
        )
        
        quiz["questions"] = questions
        quiz["estimated_time"] = f"{len(questions) * 1.5:.0f} minutos"
        
        return quiz
    
    def submit_quiz_answers(self, quiz_id: str, answers: Dict[str, str]) -> Dict:
        """Submete respostas de um quiz e retorna resultados"""
        # Simulação de verificação de respostas
        correct_count = 0
        incorrect_count = 0
        unanswered_count = 0
        
        # Gerar resultados simulados
        results = {
            "quiz_id": quiz_id,
            "submission_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": len(answers),
            "correct_count": 0,
            "incorrect_count": 0,
            "unanswered_count": 0,
            "score": 0,
            "question_results": [],
            "subject_scores": {}
        }
        
        # Simular verificação de cada resposta
        subject_correct = {}
        subject_total = {}
        
        for question_id, answer in answers.items():
            # Simular resposta correta (50% de chance)
            is_correct = random.choice([True, False])
            
            # Simular matéria
            subject = random.choice(["Português", "Matemática", "Conhecimentos Específicos"])
            
            # Atualizar contadores por matéria
            if subject not in subject_total:
                subject_total[subject] = 0
                subject_correct[subject] = 0
            
            subject_total[subject] += 1
            
            if is_correct:
                correct_count += 1
                subject_correct[subject] += 1
                results["question_results"].append({
                    "question_id": question_id,
                    "is_correct": True,
                    "submitted_answer": answer,
                    "correct_answer": answer,
                    "subject": subject
                })
            else:
                incorrect_count += 1
                # Simular resposta correta diferente
                correct_answer = random.choice(["a", "b", "c", "d", "e"])
                while correct_answer == answer:
                    correct_answer = random.choice(["a", "b", "c", "d", "e"])
                
                results["question_results"].append({
                    "question_id": question_id,
                    "is_correct": False,
                    "submitted_answer": answer,
                    "correct_answer": correct_answer,
                    "subject": subject
                })
        
        # Calcular pontuações por matéria
        for subject in subject_total:
            if subject_total[subject] > 0:
                score = (subject_correct[subject] / subject_total[subject]) * 100
                results["subject_scores"][subject] = round(score, 1)
        
        # Atualizar resultados gerais
        results["correct_count"] = correct_count
        results["incorrect_count"] = incorrect_count
        results["unanswered_count"] = unanswered_count
        results["score"] = round((correct_count / len(answers)) * 100, 1) if answers else 0
        
        return results
    
    def _run(self, action: str, params_json: str) -> str:
        """Interface principal da ferramenta"""
        try:
            # Converter parâmetros JSON para dicionário
            params = json.loads(params_json)
            
            # Executar ação solicitada
            if action == "fetch_questions":
                subjects = params.get("subjects", ["Português", "Matemática"])
                difficulty = params.get("difficulty", "medium")
                count = params.get("count", 10)
                banca = params.get("banca")
                
                result = self.fetch_questions(subjects, difficulty, count, banca)
            
            elif action == "daily_quiz":
                study_plan = params.get("study_plan", {})
                performance_history = params.get("performance_history", [])
                
                result = self.generate_daily_quiz(study_plan, performance_history)
            
            elif action == "submit_answers":
                quiz_id = params.get("quiz_id", "")
                answers = params.get("answers", {})
                
                result = self.submit_quiz_answers(quiz_id, answers)
            
            else:
                result = {"error": "Ação inválida"}
            
            return json.dumps(result, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'error': f'Erro na ferramenta de questões: {str(e)}'
            }, indent=2, ensure_ascii=False)