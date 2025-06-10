import json
import random
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class MockExamTool:
    def __init__(self):
        self.name = "MockExamTool"
        self.description = "Gera simulados inteligentes baseados em padrões de bancas e dados de provas anteriores"

        # Base de questões por matéria e banca
        self.question_bank = self._initialize_question_bank()

        # Padrões de bancas
        self.banca_patterns = {
            'CESPE': {
                'question_types': ['Certo/Errado', 'Múltipla Escolha'],
                'time_per_question': 3,
                'difficulty_distribution': {'easy': 0.2, 'medium': 0.6, 'hard': 0.2},
                'subjects_weight': {
                    'Português': 0.25, 'Direito': 0.30, 'Conhecimentos Específicos': 0.25,
                    'Matemática': 0.10, 'Informática': 0.10
                }
            },
            'FCC': {
                'question_types': ['Múltipla Escolha'],
                'time_per_question': 2.5,
                'difficulty_distribution': {'easy': 0.15, 'medium': 0.70, 'hard': 0.15},
                'subjects_weight': {
                    'Português': 0.30, 'Matemática': 0.20, 'Conhecimentos Específicos': 0.30,
                    'Direito': 0.15, 'Informática': 0.05
                }
            },
            'VUNESP': {
                'question_types': ['Múltipla Escolha'],
                'time_per_question': 2.8,
                'difficulty_distribution': {'easy': 0.25, 'medium': 0.60, 'hard': 0.15},
                'subjects_weight': {
                    'Português': 0.25, 'Matemática': 0.15, 'Conhecimentos Específicos': 0.35,
                    'Atualidades': 0.15, 'Informática': 0.10
                }
            }
        }

    def _initialize_question_bank(self) -> Dict:
        """Carrega banco de questões do arquivo JSON"""
        try:
            with open('data/questions/question_bank.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('questions', {})
        except FileNotFoundError:
            # Fallback para questões básicas se arquivo não existir
            return self._get_fallback_questions()
        except Exception as e:
            print(f"Erro ao carregar banco de questões: {e}")
            return self._get_fallback_questions()

    def _get_fallback_questions(self) -> Dict:
        """Questões básicas como fallback"""
        return {
            'Português': [
                {
                    'id': 'port_001',
                    'text': 'Assinale a alternativa em que a concordância verbal está CORRETA:',
                    'options': [
                        {'id': 'A', 'text': 'Fazem dois anos que ele partiu.'},
                        {'id': 'B', 'text': 'Faz dois anos que ele partiu.'},
                        {'id': 'C', 'text': 'Fazem dois anos desde que ele partiu.'},
                        {'id': 'D', 'text': 'Fazia dois anos desde que ele partiu.'}
                    ],
                    'correct_answer': 'B',
                    'explanation': 'O verbo "fazer" no sentido de tempo decorrido é impessoal, permanecendo sempre na 3ª pessoa do singular.',
                    'difficulty': 'medium',
                    'subject': 'Português',
                    'topic': 'Concordância Verbal'
                }
            ],
            'Matemática': [
                {
                    'id': 'mat_001',
                    'text': 'Se 3x + 5 = 20, qual o valor de x?',
                    'options': [
                        {'id': 'A', 'text': '3'},
                        {'id': 'B', 'text': '5'},
                        {'id': 'C', 'text': '15'},
                        {'id': 'D', 'text': '25'}
                    ],
                    'correct_answer': 'B',
                    'explanation': '3x + 5 = 20 → 3x = 15 → x = 5',
                    'difficulty': 'easy',
                    'subject': 'Matemática',
                    'topic': 'Equações do 1º grau'
                }
            ]
        }

    def generate_mock_exam(self, banca: str, subjects: List[str], num_questions: int = 20,
                          difficulty: str = 'mixed', cargo: str = None) -> Dict:
        """Gera um simulado baseado nos parâmetros especificados"""

        # Obter padrão da banca
        banca_pattern = self.banca_patterns.get(banca, self.banca_patterns['CESPE'])

        # Distribuir questões por matéria
        questions_per_subject = self._distribute_questions_by_subject(
            subjects, num_questions, banca_pattern['subjects_weight']
        )

        # Gerar questões
        selected_questions = []

        for subject, count in questions_per_subject.items():
            if subject in self.question_bank:
                subject_questions = self._select_questions_by_difficulty(
                    self.question_bank[subject], count, difficulty, banca_pattern
                )
                selected_questions.extend(subject_questions)

        # Embaralhar questões
        random.shuffle(selected_questions)

        # Criar estrutura do simulado
        mock_exam = {
            'id': str(uuid.uuid4()),
            'title': f'Simulado {banca} - {cargo or "Geral"}',
            'banca': banca,
            'cargo': cargo,
            'created_at': datetime.now().isoformat(),
            'total_questions': len(selected_questions),
            'estimated_time': len(selected_questions) * banca_pattern['time_per_question'],
            'subjects': subjects,
            'difficulty': difficulty,
            'questions': selected_questions,
            'instructions': self._generate_instructions(banca, len(selected_questions)),
            'scoring': {
                'total_points': len(selected_questions) * 10,
                'passing_score': len(selected_questions) * 6,  # 60% para aprovação
                'weight_per_question': 10
            }
        }

        return mock_exam

    def _distribute_questions_by_subject(self, subjects: List[str], total_questions: int,
                                       subject_weights: Dict[str, float]) -> Dict[str, int]:
        """Distribui questões por matéria baseado nos pesos da banca"""
        distribution = {}

        # Calcular peso total das matérias selecionadas
        total_weight = sum(subject_weights.get(subject, 0.1) for subject in subjects)

        # Distribuir questões proporcionalmente
        remaining_questions = total_questions

        for i, subject in enumerate(subjects):
            weight = subject_weights.get(subject, 0.1)

            if i == len(subjects) - 1:  # Última matéria recebe o restante
                distribution[subject] = remaining_questions
            else:
                count = int((weight / total_weight) * total_questions)
                distribution[subject] = max(1, count)  # Mínimo 1 questão por matéria
                remaining_questions -= distribution[subject]

        return distribution

    def _select_questions_by_difficulty(self, questions: List[Dict], count: int,
                                      difficulty: str, banca_pattern: Dict) -> List[Dict]:
        """Seleciona questões baseado na dificuldade especificada"""
        if difficulty == 'mixed':
            # Usar distribuição da banca
            diff_dist = banca_pattern['difficulty_distribution']
            easy_count = int(count * diff_dist['easy'])
            medium_count = int(count * diff_dist['medium'])
            hard_count = count - easy_count - medium_count

            selected = []

            # Selecionar questões por dificuldade
            easy_questions = [q for q in questions if q.get('difficulty') == 'easy']
            medium_questions = [q for q in questions if q.get('difficulty') == 'medium']
            hard_questions = [q for q in questions if q.get('difficulty') == 'hard']

            selected.extend(random.sample(easy_questions, min(easy_count, len(easy_questions))))
            selected.extend(random.sample(medium_questions, min(medium_count, len(medium_questions))))
            selected.extend(random.sample(hard_questions, min(hard_count, len(hard_questions))))

            # Completar com questões aleatórias se necessário
            while len(selected) < count and len(selected) < len(questions):
                remaining = [q for q in questions if q not in selected]
                if remaining:
                    selected.append(random.choice(remaining))
                else:
                    break

        else:
            # Filtrar por dificuldade específica
            filtered_questions = [q for q in questions if q.get('difficulty') == difficulty]
            if not filtered_questions:
                filtered_questions = questions  # Fallback para todas as questões

            selected = random.sample(filtered_questions, min(count, len(filtered_questions)))

        return selected

    def _generate_instructions(self, banca: str, num_questions: int) -> List[str]:
        """Gera instruções específicas para o simulado baseado na banca"""
        base_instructions = [
            f"Este simulado contém {num_questions} questões.",
            "Leia atentamente cada questão antes de responder.",
            "Marque apenas uma alternativa por questão.",
            "Não é permitido o uso de calculadora ou material de consulta.",
        ]

        banca_specific = {
            'CESPE': [
                "Atenção: Esta banca é conhecida por questões com pegadinhas.",
                "Leia os enunciados com muito cuidado, prestando atenção aos detalhes.",
                "Para questões Certo/Errado, marque C para Certo e E para Errado."
            ],
            'FCC': [
                "Esta banca valoriza conhecimento técnico e precisão conceitual.",
                "Foque na aplicação prática dos conceitos.",
                "Elimine as alternativas claramente incorretas."
            ],
            'VUNESP': [
                "Esta banca costuma contextualizar as questões com situações práticas.",
                "Mantenha-se atualizado com notícias e acontecimentos recentes.",
                "Preste atenção às questões de interpretação de texto."
            ]
        }

        instructions = base_instructions + banca_specific.get(banca, [])
        return instructions

    def evaluate_exam(self, exam_id: str, answers: Dict[str, str]) -> Dict:
        """Avalia as respostas do simulado"""
        # Em uma implementação real, buscaria o exame do banco de dados
        # Por ora, vamos simular a avaliação

        total_questions = len(answers)
        correct_count = 0
        question_results = []
        subject_scores = {}

        # Simular avaliação (em produção, compararia com respostas corretas)
        for question_id, submitted_answer in answers.items():
            # Simular se a resposta está correta (70% de chance de acerto)
            is_correct = random.random() < 0.7

            if is_correct:
                correct_count += 1

            # Simular dados da questão
            question_result = {
                'question_id': question_id,
                'submitted_answer': submitted_answer,
                'correct_answer': random.choice(['A', 'B', 'C', 'D']),
                'is_correct': is_correct,
                'points': 10 if is_correct else 0
            }

            question_results.append(question_result)

        # Calcular pontuação geral
        score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        # Simular pontuação por matéria
        subjects = ['Português', 'Matemática', 'Direito', 'Informática']
        for subject in subjects:
            subject_scores[subject] = random.randint(50, 95)

        evaluation = {
            'exam_id': exam_id,
            'total_questions': total_questions,
            'correct_count': correct_count,
            'score': round(score_percentage, 1),
            'grade': self._calculate_grade(score_percentage),
            'subject_scores': subject_scores,
            'question_results': question_results,
            'performance_analysis': self._analyze_performance(score_percentage, subject_scores),
            'recommendations': self._generate_recommendations(score_percentage, subject_scores),
            'evaluated_at': datetime.now().isoformat()
        }

        return evaluation

    def _calculate_grade(self, score: float) -> str:
        """Calcula conceito baseado na pontuação"""
        if score >= 90:
            return 'Excelente'
        elif score >= 80:
            return 'Muito Bom'
        elif score >= 70:
            return 'Bom'
        elif score >= 60:
            return 'Regular'
        else:
            return 'Insuficiente'

    def _analyze_performance(self, overall_score: float, subject_scores: Dict[str, float]) -> Dict:
        """Analisa o desempenho do candidato"""
        analysis = {
            'overall_performance': 'good' if overall_score >= 70 else 'needs_improvement',
            'strongest_subjects': [],
            'weakest_subjects': [],
            'consistency': 'high'  # Seria calculado baseado na variação entre matérias
        }

        # Identificar matérias mais fortes e mais fracas
        sorted_subjects = sorted(subject_scores.items(), key=lambda x: x[1], reverse=True)

        analysis['strongest_subjects'] = [subj for subj, score in sorted_subjects[:2]]
        analysis['weakest_subjects'] = [subj for subj, score in sorted_subjects[-2:]]

        return analysis

    def _generate_recommendations(self, overall_score: float, subject_scores: Dict[str, float]) -> List[str]:
        """Gera recomendações baseadas no desempenho"""
        recommendations = []

        if overall_score < 60:
            recommendations.append("Foque em revisar os conceitos básicos de todas as matérias.")
            recommendations.append("Aumente o tempo de estudo diário.")
        elif overall_score < 80:
            recommendations.append("Concentre-se nas matérias com menor pontuação.")
            recommendations.append("Pratique mais exercícios das áreas fracas.")
        else:
            recommendations.append("Mantenha o ritmo de estudos.")
            recommendations.append("Foque em questões de maior dificuldade.")

        # Recomendações específicas por matéria
        for subject, score in subject_scores.items():
            if score < 60:
                recommendations.append(f"Revisar urgentemente os conceitos de {subject}.")

        return recommendations

    def _run(self, action: str, params_json: str) -> str:
        """Interface principal da ferramenta"""
        try:
            params = json.loads(params_json)

            if action == "generate_exam":
                banca = params.get('banca', 'CESPE')
                subjects = params.get('subjects', ['Português', 'Matemática'])
                num_questions = params.get('num_questions', 20)
                difficulty = params.get('difficulty', 'mixed')
                cargo = params.get('cargo')

                result = self.generate_mock_exam(banca, subjects, num_questions, difficulty, cargo)

            elif action == "evaluate_exam":
                exam_id = params.get('exam_id')
                answers = params.get('answers', {})

                result = self.evaluate_exam(exam_id, answers)

            else:
                result = {"error": "Ação não reconhecida. Use 'generate_exam' ou 'evaluate_exam'."}

            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            return json.dumps({
                'error': f'Erro na ferramenta de simulados: {str(e)}'
            }, indent=2, ensure_ascii=False)