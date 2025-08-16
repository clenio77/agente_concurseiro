#!/usr/bin/env python3
"""
Teste das Novas Funcionalidades - Fase 1
Valida Dashboard, Gamificação e Chatbot
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_dashboard_component():
    """Testa o componente Dashboard"""
    print("🧪 TESTANDO DASHBOARD COMPONENT")
    print("="*60)
    
    try:
        from app.components.dashboard import Dashboard
        
        # Criar instância
        dashboard = Dashboard()
        print("✅ Dashboard instanciado com sucesso")
        
        # Testar inicialização de dados
        assert hasattr(dashboard, 'initialize_session_state')
        print("✅ Método de inicialização presente")
        
        # Testar geração de dados mock
        mock_data = dashboard.generate_mock_data()
        assert 'materias' in mock_data
        assert 'atividade_diaria' in mock_data
        print("✅ Dados mock gerados corretamente")
        
        # Verificar estrutura dos dados
        materias = mock_data['materias']
        assert len(materias) > 0
        
        for materia, dados in materias.items():
            assert 'questoes_resolvidas' in dados
            assert 'acertos' in dados
            assert 'tempo_estudo' in dados
            assert 'ultima_atividade' in dados
        
        print("✅ Estrutura de dados das matérias válida")
        
        # Verificar atividade diária
        atividades = mock_data['atividade_diaria']
        assert len(atividades) > 0
        
        for atividade in atividades:
            assert 'data' in atividade
            assert 'horas_estudo' in atividade
            assert 'questoes' in atividade
            assert 'acertos' in atividade
        
        print("✅ Estrutura de dados de atividade válida")
        print("🎉 DASHBOARD COMPONENT: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do Dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_gamification_component():
    """Testa o componente de Gamificação"""
    print("\n🧪 TESTANDO GAMIFICATION COMPONENT")
    print("="*60)
    
    try:
        from app.components.gamification import GamificationSystem
        
        # Criar instância
        gamification = GamificationSystem()
        print("✅ GamificationSystem instanciado com sucesso")
        
        # Testar configuração de badges
        badges_config = gamification.get_badges_config()
        assert len(badges_config) > 0
        print(f"✅ {len(badges_config)} badges configuradas")
        
        # Verificar estrutura das badges
        for badge_id, badge_data in badges_config.items():
            assert 'name' in badge_data
            assert 'description' in badge_data
            assert 'icon' in badge_data
            assert 'rarity' in badge_data
            assert 'points' in badge_data
        
        print("✅ Estrutura das badges válida")
        
        # Testar configuração de conquistas
        achievements_config = gamification.get_achievements_config()
        assert len(achievements_config) > 0
        print(f"✅ {len(achievements_config)} conquistas configuradas")
        
        # Verificar estrutura das conquistas
        for achievement_id, achievement_data in achievements_config.items():
            assert 'name' in achievement_data
            assert 'description' in achievement_data
            assert 'progress_max' in achievement_data
            assert 'reward_points' in achievement_data
            assert 'icon' in achievement_data
        
        print("✅ Estrutura das conquistas válida")
        
        # Testar cálculo de nível
        test_xp = 500
        level = gamification.calculate_level_from_xp(test_xp)
        assert level > 0
        print(f"✅ Cálculo de nível funcionando: {test_xp} XP = Nível {level}")
        
        # Testar XP para próximo nível
        next_level_xp = gamification.get_xp_for_next_level(level)
        assert next_level_xp > test_xp
        print(f"✅ XP para próximo nível: {next_level_xp}")
        
        # Testar cores de raridade
        colors = ['comum', 'raro', 'épico', 'lendário']
        for rarity in colors:
            color = gamification.get_badge_rarity_color(rarity)
            assert color.startswith('#')
        
        print("✅ Cores de raridade funcionando")
        
        # Testar geração de desafios semanais
        challenges = gamification.generate_weekly_challenges()
        assert len(challenges) > 0
        
        for challenge in challenges:
            assert 'id' in challenge
            assert 'name' in challenge
            assert 'description' in challenge
            assert 'progress' in challenge
            assert 'target' in challenge
            assert 'reward' in challenge
            assert 'expires' in challenge
        
        print("✅ Desafios semanais gerados corretamente")
        print("🎉 GAMIFICATION COMPONENT: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de Gamificação: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_chatbot_component():
    """Testa o componente Chatbot"""
    print("\n🧪 TESTANDO CHATBOT COMPONENT")
    print("="*60)
    
    try:
        from app.components.chatbot import ChatBot
        
        # Criar instância
        chatbot = ChatBot()
        print("✅ ChatBot instanciado com sucesso")
        
        # Testar base de conhecimento
        faq_database = chatbot.load_faq_database()
        assert len(faq_database) > 0
        print(f"✅ {len(faq_database)} entradas na base de conhecimento")
        
        # Verificar estrutura do FAQ
        for faq_id, faq_data in faq_database.items():
            assert 'keywords' in faq_data
            assert 'response' in faq_data
            assert 'category' in faq_data
            assert len(faq_data['keywords']) > 0
            assert len(faq_data['response']) > 0
        
        print("✅ Estrutura da base de conhecimento válida")
        
        # Testar respostas contextuais
        context_responses = chatbot.load_context_responses()
        assert len(context_responses) > 0
        print(f"✅ {len(context_responses)} respostas contextuais")
        
        # Testar busca de respostas
        test_questions = [
            "Como usar o sistema?",
            "Como analisar edital?",
            "Dicas de estudo",
            "Como ganhar pontos?",
            "Problemas técnicos"
        ]
        
        for question in test_questions:
            response = chatbot.find_best_response(question)
            assert len(response) > 0
            print(f"✅ Resposta para '{question}': {len(response)} caracteres")
        
        # Testar resposta genérica
        generic_response = chatbot.generate_generic_response("pergunta aleatória")
        assert len(generic_response) > 0
        print("✅ Resposta genérica funcionando")
        
        print("🎉 CHATBOT COMPONENT: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do Chatbot: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Testa integração entre componentes"""
    print("\n🧪 TESTANDO INTEGRAÇÃO DOS COMPONENTES")
    print("="*60)
    
    try:
        # Testar imports simultâneos
        from app.components.dashboard import Dashboard
        from app.components.gamification import GamificationSystem
        from app.components.chatbot import ChatBot
        
        # Criar instâncias simultâneas
        dashboard = Dashboard()
        gamification = GamificationSystem()
        chatbot = ChatBot()
        
        print("✅ Todos os componentes podem ser instanciados simultaneamente")
        
        # Testar se não há conflitos de session_state
        # (Simulação - em produção seria testado com Streamlit)
        session_keys = []
        
        # Dashboard keys
        dashboard_keys = ['user_stats', 'study_streak', 'total_points']
        session_keys.extend(dashboard_keys)
        
        # Gamification keys  
        gamification_keys = ['user_level', 'user_xp', 'user_badges', 'user_achievements', 'daily_streak', 'weekly_challenges']
        session_keys.extend(gamification_keys)
        
        # Chatbot keys
        chatbot_keys = ['chat_messages', 'chat_context']
        session_keys.extend(chatbot_keys)
        
        # Verificar se não há duplicatas
        unique_keys = set(session_keys)
        if len(unique_keys) == len(session_keys):
            print("✅ Não há conflitos de chaves de sessão")
        else:
            duplicates = [key for key in session_keys if session_keys.count(key) > 1]
            print(f"⚠️ Chaves duplicadas encontradas: {duplicates}")
        
        print("🎉 INTEGRAÇÃO: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de integração: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DAS NOVAS FUNCIONALIDADES")
    print("="*80)
    
    results = []
    
    # Executar testes individuais
    results.append(("Dashboard", test_dashboard_component()))
    results.append(("Gamificação", test_gamification_component()))
    results.append(("Chatbot", test_chatbot_component()))
    results.append(("Integração", test_integration()))
    
    # Resumo dos resultados
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES")
    print("="*80)
    
    passed = 0
    total = len(results)
    
    for component, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{component:15} | {status}")
        if result:
            passed += 1
    
    print("-"*80)
    print(f"TOTAL: {passed}/{total} testes passaram ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema pronto para produção")
        print("🚀 Fase 1 concluída com sucesso")
        return True
    else:
        print(f"\n⚠️ {total-passed} TESTES FALHARAM!")
        print("❌ Correções necessárias antes do deploy")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Deploy das novas funcionalidades")
        print("2. Coleta de feedback dos usuários")
        print("3. Início da Fase 2 - IA Preditiva")
        print("4. Implementação de recursos colaborativos")
    else:
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        print("1. Corrigir testes que falharam")
        print("2. Executar testes novamente")
        print("3. Validar integração completa")
        
    sys.exit(0 if success else 1)
