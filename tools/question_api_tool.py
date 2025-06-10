import json
import random
from typing import Dict, List
import requests
from datetime import datetime
import os

class QuestionAPITool:
    def __init__(self):
        self.name = "QuestionAPITool"
        self.description = "Integra com banco de questões local e APIs externas"
        self.api_base_url = "https://api.example.com/questions"  # URL fictícia
        self.question_bank = self._load_question_bank()

    def _load_question_bank(self) -> Dict:
        """Carrega banco de questões local"""
        try:
            with open('data/questions/question_bank.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('questions', {})
        except FileNotFoundError:
            print("Arquivo de banco de questões não encontrado. Usando questões simuladas.")
            return self._get_simulated_questions()
        except Exception as e:
            print(f"Erro ao carregar banco de questões: {e}")
            return self._get_simulated_questions()

    def _get_simulated_questions(self) -> Dict:
        """Questões simuladas como fallback"""
        return {
            'Português': [
                {
                    'id': 'sim_port_001',
                    'text': 'Qual alternativa está correta?',
                    'options': [
                        {'id': 'A', 'text': 'Opção A'},
                        {'id': 'B', 'text': 'Opção B'},
                        {'id': 'C', 'text': 'Opção C'},
                        {'id': 'D', 'text': 'Opção D'}
                    ],
                    'correct_answer': 'A',
                    'explanation': 'Explicação simulada.',
                    'difficulty': 'medium',
                    'subject': 'Português',
                    'topic': 'Simulado',
                    'banca': 'CESPE',
                    'year': 2023
                }
            ]
        }

    def fetch_questions(self, subjects: List[str], difficulty: str = "medium",
                       count: int = 10, banca: str = None) -> List[Dict]:
        """Busca questões do banco local filtradas por critérios"""
        selected_questions = []

        # Coletar todas as questões disponíveis das matérias solicitadas
        available_questions = []

        for subject in subjects:
            if subject in self.question_bank:
                subject_questions = self.question_bank[subject]

                # Filtrar por dificuldade se especificada
                if difficulty != "mixed":
                    subject_questions = [q for q in subject_questions if q.get('difficulty') == difficulty]

                # Filtrar por banca se especificada
                if banca:
                    subject_questions = [q for q in subject_questions if q.get('banca', '').upper() == banca.upper()]

                available_questions.extend(subject_questions)

        # Se não há questões suficientes, gerar questões simuladas
        if len(available_questions) < count:
            print(f"Apenas {len(available_questions)} questões disponíveis. Gerando questões simuladas para completar.")

            # Usar questões disponíveis
            selected_questions.extend(available_questions)

            # Gerar questões simuladas para completar
            remaining_count = count - len(available_questions)
            simulated_questions = self._generate_simulated_questions(subjects, difficulty, banca, remaining_count)
            selected_questions.extend(simulated_questions)
        else:
            # Selecionar questões aleatoriamente
            selected_questions = random.sample(available_questions, count)

        # Embaralhar questões
        random.shuffle(selected_questions)

        return selected_questions

    def _generate_simulated_questions(self, subjects: List[str], difficulty: str,
                                    banca: str, count: int) -> List[Dict]:
        """Gera questões simuladas quando não há questões suficientes no banco"""
        simulated_questions = []

        question_templates = {
            'Português': [
                "Assinale a alternativa que apresenta ERRO de concordância:",
                "Qual das frases abaixo está CORRETA quanto à regência verbal?",
                "Identifique a alternativa com uso INCORRETO da crase:",
                "Marque a opção que contém ERRO de colocação pronominal:"
            ],
            'Matemática': [
                "Resolva a equação: {equation}",
                "Calcule o valor da expressão: {expression}",
                "Em uma progressão aritmética com primeiro termo {a1} e razão {r}, qual é o {n}º termo?",
                "Se {percentage}% de {number} é {result}, qual é o valor de {variable}?"
            ],
            'Direito': [
                "Segundo a Constituição Federal, é CORRETO afirmar:",
                "Sobre os princípios da Administração Pública:",
                "De acordo com a legislação vigente:",
                "Quanto aos direitos fundamentais:"
            ],
            'Informática': [
                "No Microsoft Word, qual a função da tecla de atalho {shortcut}?",
                "Qual protocolo é usado para {purpose}?",
                "Em relação à segurança da informação:",
                "Sobre redes de computadores:"
            ]
        }

        for i in range(count):
            subject = random.choice(subjects)

            # Selecionar template de questão
            templates = question_templates.get(subject, ["Questão sobre {subject}:"])
            question_text = random.choice(templates)

            # Personalizar questão baseada na matéria
            if subject == 'Matemática':
                question_text = question_text.format(
                    equation=f"{random.randint(2,5)}x + {random.randint(1,10)} = {random.randint(15,50)}",
                    expression=f"({random.randint(2,5)}² × {random.randint(2,4)}) ÷ {random.randint(2,6)}",
                    a1=random.randint(1,10),
                    r=random.randint(2,5),
                    n=random.randint(5,15),
                    percentage=random.randint(10,50),
                    number=random.randint(100,500),
                    result=random.randint(20,100),
                    variable="x"
                )
            elif subject == 'Informática':
                shortcuts = ['Ctrl+C', 'Ctrl+V', 'Ctrl+Z', 'Ctrl+S', 'Alt+Tab']
                purposes = ['transferência segura de arquivos', 'envio de emails', 'navegação web']
                question_text = question_text.format(
                    shortcut=random.choice(shortcuts),
                    purpose=random.choice(purposes)
                )

            # Gerar opções de resposta
            options = []
            for j, letter in enumerate(['A', 'B', 'C', 'D']):
                options.append({
                    'id': letter,
                    'text': f"Opção {letter} - {subject}"
                })

            question = {
                'id': f'sim_{subject.lower()[:3]}_{i+1000}',
                'text': question_text,
                'options': options,
                'correct_answer': random.choice(['A', 'B', 'C', 'D']),
                'explanation': f'Explicação simulada para questão de {subject}.',
                'difficulty': difficulty,
                'subject': subject,
                'topic': 'Simulado',
                'banca': banca or 'CESPE',
                'year': 2023,
                'source': 'Questão Simulada'
            }

            simulated_questions.append(question)

        return simulated_questions
    
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