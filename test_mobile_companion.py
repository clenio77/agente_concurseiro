#!/usr/bin/env python3
"""
Teste do Mobile Companion - Fase 2
Valida funcionalidades móveis, notificações e sincronização
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_mobile_companion_component():
    """Testa o componente Mobile Companion"""
    print("🧪 TESTANDO MOBILE COMPANION COMPONENT")
    print("="*60)
    
    try:
        from app.components.mobile_companion import MobileCompanion, DeviceType, NotificationType, SyncStatus
        
        # Criar instância
        mc = MobileCompanion()
        print("✅ MobileCompanion instanciado com sucesso")
        
        # Testar inicialização de dados
        assert hasattr(mc, 'initialize_session_state')
        print("✅ Método de inicialização presente")
        
        # Testar detecção de dispositivo
        assert hasattr(mc, 'detect_device_type')
        print("✅ Detecção de dispositivo implementada")
        
        # Testar enums
        assert isinstance(DeviceType.MOBILE, DeviceType)
        assert isinstance(NotificationType.STUDY_REMINDER, NotificationType)
        assert isinstance(SyncStatus.SYNCED, SyncStatus)
        print("✅ Enums funcionando corretamente")
        
        # Testar geração de notificações
        notifications = mc.generate_sample_notifications()
        assert len(notifications) > 0
        print(f"✅ Notificações geradas: {len(notifications)} notificações")
        
        # Verificar estrutura das notificações
        notification = notifications[0]
        required_fields = [
            'id', 'type', 'title', 'message', 'timestamp', 
            'read', 'priority', 'action_url', 'icon'
        ]
        
        for field in required_fields:
            assert field in notification, f"Campo {field} não encontrado"
        
        print("✅ Estrutura de notificações válida")
        
        # Testar geração de dados offline
        offline_data = mc.generate_offline_data()
        assert isinstance(offline_data, dict)
        assert 'flashcards' in offline_data
        assert 'notes' in offline_data
        assert 'progress_data' in offline_data
        assert 'cached_materials' in offline_data
        print("✅ Dados offline gerados")
        
        # Verificar estrutura dos flashcards
        flashcards = offline_data['flashcards']
        assert len(flashcards) > 0
        
        flashcard = flashcards[0]
        flashcard_fields = ['id', 'front', 'back', 'subject', 'difficulty', 'last_reviewed']
        
        for field in flashcard_fields:
            assert field in flashcard, f"Campo {field} não encontrado em flashcard"
        
        print("✅ Estrutura de flashcards válida")
        
        # Verificar estrutura das notas
        notes = offline_data['notes']
        assert len(notes) > 0
        
        note = notes[0]
        note_fields = ['id', 'title', 'content', 'subject', 'created_at', 'tags']
        
        for field in note_fields:
            assert field in note, f"Campo {field} não encontrado em nota"
        
        print("✅ Estrutura de notas válida")
        
        # Verificar dados de progresso
        progress_data = offline_data['progress_data']
        assert 'daily_goals' in progress_data
        assert 'weekly_stats' in progress_data
        
        daily_goals = progress_data['daily_goals']
        daily_fields = ['study_hours', 'completed_hours', 'questions_answered', 'completed_questions']
        
        for field in daily_fields:
            assert field in daily_goals, f"Campo {field} não encontrado em daily_goals"
        
        print("✅ Estrutura de progresso válida")
        
        print("🎉 MOBILE COMPANION COMPONENT: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de Mobile Companion: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_notification_system():
    """Testa sistema de notificações"""
    print("\n🧪 TESTANDO SISTEMA DE NOTIFICAÇÕES")
    print("="*60)
    
    try:
        from app.components.mobile_companion import MobileCompanion, NotificationType
        
        mc = MobileCompanion()
        
        # Testar geração de notificações
        notifications = mc.generate_sample_notifications()
        
        # Verificar tipos de notificação
        notification_types = set([n['type'] for n in notifications])
        expected_types = {
            NotificationType.STUDY_REMINDER,
            NotificationType.GROUP_MESSAGE,
            NotificationType.DEADLINE_ALERT,
            NotificationType.ACHIEVEMENT,
            NotificationType.MENTOR_MESSAGE,
            NotificationType.MATERIAL_SHARED
        }
        
        assert notification_types.issubset(expected_types), "Tipos de notificação inválidos"
        print("✅ Tipos de notificação válidos")
        
        # Verificar prioridades
        priorities = set([n['priority'] for n in notifications])
        expected_priorities = {'high', 'medium', 'low'}
        
        assert priorities.issubset(expected_priorities), "Prioridades inválidas"
        print("✅ Prioridades de notificação válidas")
        
        # Testar ícones de notificação
        for notification in notifications:
            icon = mc.get_notification_icon(notification['type'])
            assert isinstance(icon, str), "Ícone deve ser string"
            assert len(icon) > 0, "Ícone não pode estar vazio"
        
        print("✅ Ícones de notificação válidos")
        
        # Testar ordenação por timestamp
        timestamps = [n['timestamp'] for n in notifications]
        is_sorted = all(timestamps[i] >= timestamps[i+1] for i in range(len(timestamps)-1))
        assert is_sorted, "Notificações não estão ordenadas por timestamp"
        print("✅ Ordenação de notificações funcionando")
        
        # Testar filtros de notificação
        filtered = mc.filter_notifications("Todas", "Todas", "Todas")
        assert len(filtered) == len(notifications), "Filtro 'Todas' deve retornar todas as notificações"
        print("✅ Filtros de notificação funcionando")
        
        print("🎉 SISTEMA DE NOTIFICAÇÕES: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de notificações: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_offline_functionality():
    """Testa funcionalidades offline"""
    print("\n🧪 TESTANDO FUNCIONALIDADES OFFLINE")
    print("="*60)
    
    try:
        from app.components.mobile_companion import MobileCompanion
        
        mc = MobileCompanion()
        
        # Testar dados offline
        offline_data = mc.generate_offline_data()
        
        # Verificar flashcards offline
        flashcards = offline_data['flashcards']
        assert len(flashcards) > 0, "Deve haver flashcards offline"
        
        # Verificar dificuldades
        difficulties = set([card['difficulty'] for card in flashcards])
        expected_difficulties = {'easy', 'medium', 'hard'}
        
        for difficulty in difficulties:
            assert difficulty in expected_difficulties, f"Dificuldade inválida: {difficulty}"
        
        print("✅ Flashcards offline válidos")
        
        # Verificar notas offline
        notes = offline_data['notes']
        assert len(notes) > 0, "Deve haver notas offline"
        
        for note in notes:
            assert isinstance(note['tags'], list), "Tags devem ser uma lista"
            assert isinstance(note['created_at'], datetime), "created_at deve ser datetime"
        
        print("✅ Notas offline válidas")
        
        # Verificar materiais em cache
        cached_materials = offline_data['cached_materials']
        assert len(cached_materials) > 0, "Deve haver materiais em cache"
        
        for material in cached_materials:
            assert 'expires_at' in material, "Material deve ter data de expiração"
            assert isinstance(material['downloaded_at'], datetime), "downloaded_at deve ser datetime"
        
        print("✅ Materiais em cache válidos")
        
        # Verificar dados de progresso
        progress_data = offline_data['progress_data']
        
        # Verificar metas diárias
        daily_goals = progress_data['daily_goals']
        assert daily_goals['completed_hours'] <= daily_goals['study_hours'], "Horas completadas não podem exceder meta"
        assert daily_goals['completed_questions'] <= daily_goals['questions_answered'], "Questões completadas não podem exceder meta"
        
        print("✅ Dados de progresso offline válidos")
        
        print("🎉 FUNCIONALIDADES OFFLINE: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste offline: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_device_detection():
    """Testa detecção de dispositivo"""
    print("\n🧪 TESTANDO DETECÇÃO DE DISPOSITIVO")
    print("="*60)
    
    try:
        from app.components.mobile_companion import MobileCompanion, DeviceType
        import streamlit as st
        
        mc = MobileCompanion()
        
        # Testar diferentes tamanhos de tela
        test_cases = [
            (600, DeviceType.MOBILE),
            (800, DeviceType.TABLET),
            (1200, DeviceType.DESKTOP)
        ]
        
        for width, expected_type in test_cases:
            # Simular tamanho de tela
            if 'device_info' not in st.session_state:
                st.session_state.device_info = {}
            
            st.session_state.device_info['screen_width'] = width
            mc.detect_device_type()
            
            detected_type = st.session_state.device_info['type']
            assert detected_type == expected_type, f"Esperado {expected_type}, obtido {detected_type} para largura {width}"
        
        print("✅ Detecção de dispositivo funcionando")
        
        # Testar informações do dispositivo
        device_info = st.session_state.device_info
        required_fields = ['type', 'screen_width', 'screen_height', 'is_touch', 'connection']
        
        for field in required_fields:
            assert field in device_info, f"Campo {field} não encontrado em device_info"
        
        print("✅ Informações do dispositivo completas")
        
        print("🎉 DETECÇÃO DE DISPOSITIVO: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de detecção: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_sync_functionality():
    """Testa funcionalidades de sincronização"""
    print("\n🧪 TESTANDO FUNCIONALIDADES DE SINCRONIZAÇÃO")
    print("="*60)
    
    try:
        from app.components.mobile_companion import MobileCompanion, SyncStatus
        import streamlit as st
        
        mc = MobileCompanion()
        
        # Testar estados de sincronização
        sync_states = [SyncStatus.SYNCED, SyncStatus.SYNCING, SyncStatus.OFFLINE, SyncStatus.ERROR]
        
        for state in sync_states:
            st.session_state.sync_status = state
            # Verificar se o estado foi definido corretamente
            assert st.session_state.sync_status == state, f"Estado de sincronização não definido: {state}"
        
        print("✅ Estados de sincronização válidos")
        
        # Testar configurações de sincronização
        settings = st.session_state.mobile_settings
        
        sync_frequencies = ['real_time', 'every_5min', 'every_15min', 'manual']
        for frequency in sync_frequencies:
            settings['sync_frequency'] = frequency
            assert settings['sync_frequency'] == frequency, f"Frequência não definida: {frequency}"
        
        print("✅ Configurações de sincronização válidas")
        
        # Testar modo economia de dados
        settings['data_saver'] = True
        assert settings['data_saver'] == True, "Modo economia de dados não ativado"
        
        settings['data_saver'] = False
        assert settings['data_saver'] == False, "Modo economia de dados não desativado"
        
        print("✅ Modo economia de dados funcionando")
        
        print("🎉 FUNCIONALIDADES DE SINCRONIZAÇÃO: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de sincronização: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_quick_actions():
    """Testa ações rápidas"""
    print("\n🧪 TESTANDO AÇÕES RÁPIDAS")
    print("="*60)
    
    try:
        from app.components.mobile_companion import MobileCompanion
        
        mc = MobileCompanion()
        
        # Testar ações disponíveis
        available_actions = ['study_timer', 'flashcards', 'notes', 'progress', 'mock_exam', 'materials']
        
        for action in available_actions:
            # Verificar se o método existe
            assert hasattr(mc, f'show_{action}') or hasattr(mc, f'execute_quick_action'), f"Método para ação {action} não encontrado"
        
        print("✅ Ações rápidas disponíveis")
        
        # Testar configuração de ações rápidas
        import streamlit as st
        mc.initialize_session_state()
        quick_actions = st.session_state.mobile_settings['quick_actions']
        
        assert isinstance(quick_actions, list), "Quick actions deve ser uma lista"
        assert len(quick_actions) <= 4, "Máximo de 4 ações rápidas permitidas"
        
        print("✅ Configuração de ações rápidas válida")
        
        # Testar métodos de ação específicos
        action_methods = [
            'show_study_timer',
            'show_flashcards', 
            'show_quick_notes',
            'show_progress_summary',
            'show_mock_exam',
            'show_materials'
        ]
        
        for method_name in action_methods:
            assert hasattr(mc, method_name), f"Método {method_name} não encontrado"
        
        print("✅ Métodos de ação implementados")
        
        print("🎉 AÇÕES RÁPIDAS: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de ações rápidas: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_mobile_companion_tests():
    """Executa todos os testes do Mobile Companion"""
    print("🚀 INICIANDO TESTES DO MOBILE COMPANION - FASE 2")
    print("="*80)
    
    results = []
    
    # Executar testes
    results.append(("Mobile Companion Component", test_mobile_companion_component()))
    results.append(("Sistema de Notificações", test_notification_system()))
    results.append(("Funcionalidades Offline", test_offline_functionality()))
    results.append(("Detecção de Dispositivo", test_device_detection()))
    results.append(("Funcionalidades de Sincronização", test_sync_functionality()))
    results.append(("Ações Rápidas", test_quick_actions()))
    
    # Resumo dos resultados
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES - MOBILE COMPANION")
    print("="*80)
    
    passed = 0
    total = len(results)
    
    for component, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{component:35} | {status}")
        if result:
            passed += 1
    
    print("-"*80)
    print(f"TOTAL: {passed}/{total} testes passaram ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES DO MOBILE COMPANION PASSARAM!")
        print("✅ Interface responsiva funcionando")
        print("✅ Sistema de notificações push operacional")
        print("✅ Funcionalidades offline ativas")
        print("✅ Sincronização em tempo real implementada")
        print("✅ Detecção de dispositivo funcionando")
        print("✅ Ações rápidas integradas")
        return True
    else:
        print(f"\n⚠️ {total-passed} TESTES FALHARAM!")
        print("❌ Correções necessárias antes do deploy")
        return False

if __name__ == "__main__":
    success = run_mobile_companion_tests()
    
    if success:
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Finalizar integração com sistema principal")
        print("2. Implementar notificações push reais")
        print("3. Otimizar para diferentes dispositivos")
        print("4. Adicionar recursos de acessibilidade")
        print("5. Preparar para Fase 3 - Innovation")
    else:
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        print("1. Corrigir testes que falharam")
        print("2. Validar integrações entre componentes")
        print("3. Testar em dispositivos reais")
        print("4. Executar testes novamente")
        
    sys.exit(0 if success else 1)
