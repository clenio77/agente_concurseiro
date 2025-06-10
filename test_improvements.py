#!/usr/bin/env python3
"""
Script de teste para verificar as melhorias implementadas
"""

import json
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mock_exam_tool():
    """Testa o MockExamTool melhorado"""
    print("🎯 Testando MockExamTool...")
    
    try:
        from tools.mock_exam_tool import MockExamTool
        
        tool = MockExamTool()
        
        # Teste 1: Gerar simulado
        params = {
            "banca": "CESPE",
            "subjects": ["Português", "Matemática", "Direito"],
            "num_questions": 10,
            "difficulty": "medium",
            "cargo": "Analista Judiciário"
        }
        
        result = tool._run("generate_exam", json.dumps(params))
        exam_data = json.loads(result)
        
        print(f"✅ Simulado gerado com {exam_data['total_questions']} questões")
        print(f"   Banca: {exam_data['banca']}")
        print(f"   Tempo estimado: {exam_data['estimated_time']} minutos")
        
        # Teste 2: Avaliar simulado
        answers = {}
        for i, question in enumerate(exam_data['questions'][:3]):
            answers[question['id']] = 'A'  # Simular respostas
        
        eval_params = {
            "exam_id": exam_data['id'],
            "answers": answers
        }
        
        eval_result = tool._run("evaluate_exam", json.dumps(eval_params))
        eval_data = json.loads(eval_result)
        
        print(f"✅ Avaliação concluída - Pontuação: {eval_data['score']}%")
        print(f"   Acertos: {eval_data['correct_count']}/{eval_data['total_questions']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no MockExamTool: {e}")
        return False

def test_web_search_tool():
    """Testa o WebSearchTool melhorado"""
    print("\n🔍 Testando WebSearchTool...")
    
    try:
        from tools.web_search_tool import WebSearchTool
        
        tool = WebSearchTool()
        
        # Teste de busca
        params = {
            "cargo": "Analista Judiciário",
            "concurso": "TRF",
            "banca": "CESPE",
            "cidade": "Brasília",
            "max_results": 5
        }
        
        result = tool._run("search_exams", json.dumps(params))
        search_data = json.loads(result)
        
        print(f"✅ Busca realizada - {search_data['total_results']} resultados")
        print(f"   Extrações bem-sucedidas: {search_data['successful_extractions']}")
        print(f"   Recomendações: {len(search_data['recommendations'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no WebSearchTool: {e}")
        return False

def test_question_api_tool():
    """Testa o QuestionAPITool melhorado"""
    print("\n❓ Testando QuestionAPITool...")
    
    try:
        from tools.question_api_tool import QuestionAPITool
        
        tool = QuestionAPITool()
        
        # Teste 1: Buscar questões
        params = {
            "subjects": ["Português", "Matemática"],
            "difficulty": "medium",
            "count": 5,
            "banca": "CESPE"
        }
        
        result = tool._run("fetch_questions", json.dumps(params))
        questions = json.loads(result)
        
        print(f"✅ {len(questions)} questões obtidas")
        
        if questions:
            first_question = questions[0]
            print(f"   Primeira questão: {first_question['subject']} - {first_question['difficulty']}")
        
        # Teste 2: Quiz diário
        study_plan = {
            "subject_distribution": {
                "Português": {"hours_per_week": 8},
                "Matemática": {"hours_per_week": 6}
            }
        }
        
        quiz_params = {
            "study_plan": study_plan,
            "performance_history": []
        }
        
        quiz_result = tool._run("daily_quiz", json.dumps(quiz_params))
        quiz_data = json.loads(quiz_result)
        
        print(f"✅ Quiz diário gerado com {len(quiz_data['questions'])} questões")
        print(f"   Matérias de foco: {', '.join(quiz_data['focus_subjects'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no QuestionAPITool: {e}")
        return False

def test_question_bank():
    """Testa o banco de questões"""
    print("\n📚 Testando banco de questões...")
    
    try:
        with open('data/questions/question_bank.json', 'r', encoding='utf-8') as f:
            bank = json.load(f)
        
        total_questions = 0
        for subject, questions in bank['questions'].items():
            total_questions += len(questions)
            print(f"   {subject}: {len(questions)} questões")
        
        print(f"✅ Banco carregado com {total_questions} questões totais")
        print(f"   Matérias: {len(bank['questions'])}")
        print(f"   Bancas suportadas: {', '.join(bank['metadata']['bancas'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de questões: {e}")
        return False

def test_dashboard_data():
    """Testa os dados do dashboard"""
    print("\n📊 Testando dados do dashboard...")
    
    try:
        with open('data/dashboard/dashboard_data.json', 'r', encoding='utf-8') as f:
            dashboard = json.load(f)
        
        print(f"✅ Dashboard carregado")
        print(f"   Progresso geral: {dashboard['progress_summary']['completion_percentage']}%")
        print(f"   Matérias: {len(dashboard['subject_progress'])}")
        print(f"   Atividades próximas: {len(dashboard['upcoming_activities'])}")
        print(f"   Conquistas: {len(dashboard.get('achievements', []))}")
        print(f"   Recomendações: {len(dashboard.get('recommendations', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos dados do dashboard: {e}")
        return False

def test_config():
    """Testa o sistema de configuração"""
    print("\n⚙️ Testando configuração...")
    
    try:
        from app.utils.config import load_config, save_config
        
        config = load_config()
        
        print(f"✅ Configuração carregada")
        print(f"   App: {config['app']['name']} v{config['app']['version']}")
        print(f"   Features ativas: {sum(1 for f in config['features'].values() if f)}")
        print(f"   Bancas suportadas: {len(config['study']['supported_bancas'])}")
        print(f"   Matérias suportadas: {len(config['study']['supported_subjects'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def test_gamification_system():
    """Testa o sistema de gamificação"""
    print("\n🎮 Testando sistema de gamificação...")

    try:
        from app.utils.gamification import GamificationSystem

        # Criar sistema de gamificação
        gamification = GamificationSystem("test_user")

        # Testar adição de experiência
        result = gamification.add_experience(100, "daily_quiz")
        print(f"✅ Experiência adicionada: {result}")

        # Testar verificação de conquistas
        activity_data = {
            "current_streak": 7,
            "study_hours": 25,
            "best_score": 85
        }

        new_achievements = gamification.check_achievements(activity_data)
        print(f"✅ Conquistas verificadas: {len(new_achievements)} novas")

        # Testar resumo do usuário
        summary = gamification.get_user_summary()
        print(f"✅ Resumo gerado - Nível: {summary['level']}, Pontos: {summary['total_points']}")

        return True

    except Exception as e:
        print(f"❌ Erro no sistema de gamificação: {e}")
        return False

def test_performance_predictor():
    """Testa o sistema de predição de desempenho"""
    print("\n🔮 Testando preditor de desempenho...")

    try:
        from app.utils.performance_predictor import PerformancePredictor

        predictor = PerformancePredictor()

        # Dados de teste
        user_data = {
            'mock_exam_scores': [
                {'score': 65, 'date': '2024-01-01'},
                {'score': 70, 'date': '2024-01-08'},
                {'score': 75, 'date': '2024-01-15'}
            ],
            'subject_progress': {
                'Português': {'last_score': 78},
                'Matemática': {'last_score': 65},
                'Direito': {'last_score': 82}
            },
            'total_study_hours': 80,
            'simulados_completed': 3
        }

        # Testar análise de desempenho
        metrics = predictor.analyze_performance(user_data)
        print(f"✅ Métricas analisadas - Score geral: {metrics.overall_score:.1f}%")

        # Testar predição
        prediction = predictor.predict_exam_performance(user_data, "CESPE", 90)
        print(f"✅ Predição gerada - Score previsto: {prediction.predicted_score:.1f}%")
        print(f"   Confiança: {prediction.confidence:.1f}%")

        return True

    except Exception as e:
        print(f"❌ Erro no preditor de desempenho: {e}")
        return False

def test_notifications_system():
    """Testa o sistema de notificações"""
    print("\n🔔 Testando sistema de notificações...")

    try:
        from app.utils.notifications import NotificationManager, NotificationType, NotificationPriority

        # Criar gerenciador de notificações
        manager = NotificationManager("test_user")

        # Criar notificação de teste
        notification = manager.create_notification(
            NotificationType.STUDY_REMINDER,
            "Teste de Notificação",
            "Esta é uma notificação de teste",
            NotificationPriority.MEDIUM
        )

        print(f"✅ Notificação criada: {notification.title}")

        # Testar busca de notificações não lidas
        unread = manager.get_unread_notifications()
        print(f"✅ Notificações não lidas: {len(unread)}")

        # Testar resumo
        summary = manager.get_notification_summary()
        print(f"✅ Resumo gerado - Total não lidas: {summary['total_unread']}")

        return True

    except Exception as e:
        print(f"❌ Erro no sistema de notificações: {e}")
        return False

def test_writing_system():
    """Testa o sistema avançado de redação"""
    print("\n✍️ Testando sistema de redação...")

    try:
        from tools.writing_tool import WritingTool

        # Criar ferramenta de redação
        writing_tool = WritingTool()

        # Texto de teste
        texto_teste = """
        A sustentabilidade ambiental representa um dos maiores desafios contemporâneos.

        Em primeiro lugar, é fundamental reconhecer que o desenvolvimento econômico não pode ocorrer em detrimento do meio ambiente. Portanto, torna-se necessário implementar políticas públicas que promovam o equilíbrio entre crescimento e preservação.

        Ademais, a educação ambiental constitui ferramenta essencial para conscientização da população. Assim, investimentos em programas educacionais podem gerar mudanças significativas no comportamento social.

        Conclui-se, portanto, que a sustentabilidade ambiental exige ações coordenadas entre governo, empresas e sociedade civil para garantir um futuro sustentável para as próximas gerações.
        """

        # Testar avaliação por banca
        resultado = writing_tool.evaluate_essay_by_banca(
            texto_teste,
            "CESPE",
            "dissertativo-argumentativo",
            "Sustentabilidade ambiental"
        )

        print(f"✅ Redação avaliada - Nota: {resultado['score_final']}/10")
        print(f"   Banca: {resultado['banca']}")
        print(f"   Critérios avaliados: {len(resultado['scores_por_criterio'])}")

        # Testar busca de tema
        tema = writing_tool.get_tema_by_banca("CESPE")
        print(f"✅ Tema obtido: {tema.get('tema', 'Erro')}")

        # Testar informações da banca
        info_banca = writing_tool.banca_patterns["FCC"]
        print(f"✅ Padrões FCC carregados - Características: {len(info_banca['caracteristicas'])}")

        return True

    except Exception as e:
        print(f"❌ Erro no sistema de redação: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes das melhorias implementadas...\n")

    tests = [
        test_config,
        test_question_bank,
        test_dashboard_data,
        test_mock_exam_tool,
        test_web_search_tool,
        test_question_api_tool,
        test_gamification_system,
        test_performance_predictor,
        test_notifications_system,
        test_writing_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📋 Resumo dos testes:")
    print(f"   ✅ Passou: {passed}/{total}")
    print(f"   ❌ Falhou: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! Sistema funcionando corretamente.")
        return 0
    else:
        print(f"\n⚠️ {total - passed} teste(s) falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
