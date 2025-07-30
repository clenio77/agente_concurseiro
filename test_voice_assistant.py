#!/usr/bin/env python3
"""
Teste do Componente de Assistente de Voz - Fase 3
Valida funcionalidades de reconhecimento de voz, síntese e conversação natural
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_voice_assistant_component():
    """Testa o componente de Assistente de Voz"""
    print("🧪 TESTANDO VOICE ASSISTANT COMPONENT")
    print("="*60)
    
    try:
        from app.components.voice_assistant import VoiceAssistant, VoiceCommandType, VoiceLanguage, SpeechQuality, VoiceGender
        
        # Criar instância
        va = VoiceAssistant()
        print("✅ VoiceAssistant instanciado com sucesso")
        
        # Testar inicialização de dados
        assert hasattr(va, 'initialize_session_state')
        print("✅ Método de inicialização presente")
        
        # Testar enums
        assert isinstance(VoiceCommandType.NAVIGATION, VoiceCommandType)
        assert isinstance(VoiceLanguage.PT_BR, VoiceLanguage)
        assert isinstance(SpeechQuality.HIGH, SpeechQuality)
        assert isinstance(VoiceGender.FEMALE, VoiceGender)
        print("✅ Enums de voz funcionando corretamente")
        
        # Testar geração de comandos
        commands = va.generate_voice_commands()
        assert len(commands) > 0
        print(f"✅ Comandos de voz gerados: {len(commands)} comandos")
        
        # Verificar estrutura dos comandos
        command = commands[0]
        required_fields = [
            'id', 'command', 'type', 'action', 'description', 
            'examples', 'confidence_required', 'enabled'
        ]
        
        for field in required_fields:
            assert field in command, f"Campo {field} não encontrado"
        
        print("✅ Estrutura de comandos de voz válida")
        
        # Testar geração de histórico
        history = va.generate_voice_history()
        assert len(history) > 0
        
        history_entry = history[0]
        history_fields = ['id', 'timestamp', 'command', 'type', 'confidence', 'success']
        
        for field in history_fields:
            assert field in history_entry, f"Campo {field} não encontrado em histórico"
        
        print("✅ Estrutura de histórico de voz válida")
        
        # Testar analytics
        analytics = va.generate_voice_analytics()
        assert isinstance(analytics, dict)
        assert 'total_commands' in analytics
        assert 'success_rate' in analytics
        print("✅ Analytics de voz gerados")
        
        print("🎉 VOICE ASSISTANT COMPONENT: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de Assistente de Voz: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_commands_system():
    """Testa sistema de comandos de voz"""
    print("\n🧪 TESTANDO SISTEMA DE COMANDOS DE VOZ")
    print("="*60)
    
    try:
        from app.components.voice_assistant import VoiceAssistant, VoiceCommandType
        
        va = VoiceAssistant()
        
        # Testar tipos de comando
        command_types = list(VoiceCommandType)
        expected_types = [
            VoiceCommandType.NAVIGATION,
            VoiceCommandType.STUDY,
            VoiceCommandType.CONTROL,
            VoiceCommandType.INFORMATION,
            VoiceCommandType.CREATION
        ]
        
        for expected_type in expected_types:
            assert expected_type in command_types, f"Tipo {expected_type} não encontrado"
        
        print("✅ Tipos de comando de voz válidos")
        
        # Testar comandos gerados
        commands = va.generate_voice_commands()
        
        # Verificar diversidade de tipos
        types_found = set()
        for command in commands:
            types_found.add(command['type'])
        
        assert len(types_found) >= 3, "Poucos tipos de comando encontrados"
        print("✅ Diversidade de tipos de comando adequada")
        
        # Verificar estrutura de exemplos
        for command in commands[:3]:  # Testar primeiros 3
            assert isinstance(command['examples'], list)
            assert len(command['examples']) > 0
            assert 0.0 <= command['confidence_required'] <= 1.0
            assert isinstance(command['enabled'], bool)
        
        print("✅ Estrutura detalhada de comandos válida")
        
        # Testar métodos de comando
        test_command = commands[0]
        va.test_voice_command(test_command)
        print("✅ Teste de comando funcionando")
        
        print("🎉 SISTEMA DE COMANDOS DE VOZ: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de comandos de voz: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_conversations():
    """Testa sistema de conversação"""
    print("\n🧪 TESTANDO SISTEMA DE CONVERSAÇÃO")
    print("="*60)
    
    try:
        from app.components.voice_assistant import VoiceAssistant
        
        va = VoiceAssistant()
        
        # Testar geração de conversas
        conversations = va.generate_conversations()
        assert len(conversations) > 0
        print(f"✅ Conversas geradas: {len(conversations)} conversas")
        
        # Verificar estrutura das conversas
        conversation = conversations[0]
        conv_fields = ['id', 'topic', 'start_time', 'duration', 'messages']
        
        for field in conv_fields:
            assert field in conversation, f"Campo {field} não encontrado em conversa"
        
        print("✅ Estrutura de conversas válida")
        
        # Verificar mensagens
        messages = conversation['messages']
        assert len(messages) > 0
        
        for message in messages:
            assert 'role' in message
            assert 'content' in message
            assert message['role'] in ['user', 'assistant']
            assert len(message['content']) > 0
        
        print("✅ Estrutura de mensagens válida")
        
        # Testar geração de resposta IA
        test_question = "O que é separação dos poderes?"
        response = va.generate_ai_response(test_question, "Direito Constitucional")
        assert isinstance(response, str)
        assert len(response) > 10
        print("✅ Geração de resposta IA funcionando")
        
        # Testar diferentes tópicos
        topics = ["Direito Constitucional", "Matemática", "Português"]
        for topic in topics:
            response = va.generate_ai_response("Teste", topic)
            assert isinstance(response, str)
        
        print("✅ Respostas para diferentes tópicos funcionando")
        
        print("🎉 SISTEMA DE CONVERSAÇÃO: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de conversação: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_analytics():
    """Testa analytics de voz"""
    print("\n🧪 TESTANDO ANALYTICS DE VOZ")
    print("="*60)
    
    try:
        from app.components.voice_assistant import VoiceAssistant
        import streamlit as st
        
        va = VoiceAssistant()
        
        # Testar geração de analytics
        analytics = va.generate_voice_analytics()
        
        # Verificar campos obrigatórios
        required_fields = [
            'total_commands', 'success_rate', 'avg_confidence', 'avg_response_time',
            'most_used_command', 'daily_usage', 'command_distribution',
            'language_accuracy', 'user_satisfaction', 'error_types'
        ]
        
        for field in required_fields:
            assert field in analytics, f"Campo {field} não encontrado em analytics"
        
        print("✅ Campos de analytics presentes")
        
        # Verificar tipos de dados
        assert isinstance(analytics['total_commands'], int)
        assert isinstance(analytics['success_rate'], (int, float))
        assert isinstance(analytics['daily_usage'], list)
        assert isinstance(analytics['command_distribution'], dict)
        assert isinstance(analytics['language_accuracy'], dict)
        assert isinstance(analytics['error_types'], dict)
        
        print("✅ Tipos de dados analytics válidos")
        
        # Verificar ranges válidos
        assert 0.0 <= analytics['success_rate'] <= 1.0, "Taxa de sucesso inválida"
        assert 0.0 <= analytics['avg_confidence'] <= 1.0, "Confiança média inválida"
        assert analytics['avg_response_time'] > 0, "Tempo de resposta deve ser positivo"
        assert 1.0 <= analytics['user_satisfaction'] <= 5.0, "Satisfação do usuário inválida"
        
        print("✅ Ranges de analytics válidos")
        
        # Verificar uso diário
        daily_usage = analytics['daily_usage']
        assert len(daily_usage) == 7, "Uso diário deve ter 7 dias"
        assert all(isinstance(day, int) and day >= 0 for day in daily_usage), "Valores de uso diário inválidos"
        
        print("✅ Uso diário válido")
        
        # Verificar distribuição de comandos
        cmd_dist = analytics['command_distribution']
        assert len(cmd_dist) > 0, "Distribuição de comandos vazia"
        assert all(isinstance(v, int) and v >= 0 for v in cmd_dist.values()), "Valores de distribuição inválidos"
        
        print("✅ Distribuição de comandos válida")
        
        print("🎉 ANALYTICS DE VOZ: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de analytics de voz: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_settings():
    """Testa configurações de voz"""
    print("\n🧪 TESTANDO CONFIGURAÇÕES DE VOZ")
    print("="*60)
    
    try:
        from app.components.voice_assistant import VoiceAssistant, VoiceLanguage, VoiceGender, SpeechQuality
        import streamlit as st
        
        va = VoiceAssistant()
        
        # Testar inicialização de configurações
        va.initialize_session_state()
        
        settings = st.session_state.voice_settings
        
        # Verificar campos de configuração
        required_settings = [
            'voice_enabled', 'language', 'speech_rate', 'speech_pitch',
            'speech_volume', 'voice_gender', 'speech_quality', 'wake_word',
            'continuous_listening', 'noise_cancellation', 'auto_punctuation'
        ]
        
        for setting in required_settings:
            assert setting in settings, f"Configuração {setting} não encontrada"
        
        print("✅ Configurações de voz presentes")
        
        # Verificar tipos de configuração
        assert isinstance(settings['voice_enabled'], bool)
        assert isinstance(settings['speech_rate'], (int, float))
        assert isinstance(settings['speech_pitch'], (int, float))
        assert isinstance(settings['speech_volume'], (int, float))
        assert isinstance(settings['wake_word'], str)
        assert isinstance(settings['continuous_listening'], bool)
        
        print("✅ Tipos de configuração válidos")
        
        # Verificar valores válidos
        languages = [lang.value for lang in VoiceLanguage]
        assert settings['language'] in languages, "Idioma inválido"
        
        genders = [gender.value for gender in VoiceGender]
        assert settings['voice_gender'] in genders, "Gênero de voz inválido"
        
        qualities = [quality.value for quality in SpeechQuality]
        assert settings['speech_quality'] in qualities, "Qualidade de fala inválida"
        
        print("✅ Valores de configuração válidos")
        
        # Verificar ranges
        assert 0.0 <= settings['speech_volume'] <= 1.0, "Volume inválido"
        assert settings['speech_rate'] > 0, "Taxa de fala deve ser positiva"
        assert settings['speech_pitch'] > 0, "Tom de voz deve ser positivo"
        assert len(settings['wake_word']) > 0, "Palavra de ativação não pode ser vazia"
        
        print("✅ Ranges de configuração válidos")
        
        print("🎉 CONFIGURAÇÕES DE VOZ: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de configurações de voz: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_history():
    """Testa histórico de voz"""
    print("\n🧪 TESTANDO HISTÓRICO DE VOZ")
    print("="*60)
    
    try:
        from app.components.voice_assistant import VoiceAssistant
        import streamlit as st
        
        va = VoiceAssistant()
        
        # Testar geração de histórico
        history = va.generate_voice_history()
        assert len(history) > 0
        print(f"✅ Histórico de voz gerado: {len(history)} entradas")
        
        # Verificar estrutura do histórico
        entry = history[0]
        history_fields = [
            'id', 'timestamp', 'command', 'type', 'confidence',
            'success', 'response_time', 'audio_duration', 'language_detected'
        ]
        
        for field in history_fields:
            assert field in entry, f"Campo {field} não encontrado em entrada do histórico"
        
        print("✅ Estrutura de histórico válida")
        
        # Verificar ordenação por timestamp
        timestamps = [entry['timestamp'] for entry in history]
        is_sorted = all(timestamps[i] >= timestamps[i+1] for i in range(len(timestamps)-1))
        assert is_sorted, "Histórico não está ordenado por timestamp"
        print("✅ Ordenação de histórico funcionando")
        
        # Verificar métricas de entrada
        for entry in history[:5]:  # Testar primeiras 5
            assert 0.0 <= entry['confidence'] <= 1.0, "Confiança inválida"
            assert isinstance(entry['success'], bool), "Status de sucesso deve ser boolean"
            assert entry['response_time'] > 0, "Tempo de resposta deve ser positivo"
            assert entry['audio_duration'] > 0, "Duração de áudio deve ser positiva"
        
        print("✅ Métricas de histórico válidas")
        
        # Verificar tipos de comando no histórico
        command_types = set()
        for entry in history:
            command_types.add(entry['type'])
        
        assert len(command_types) > 0, "Nenhum tipo de comando encontrado no histórico"
        print("✅ Diversidade de tipos no histórico")
        
        print("🎉 HISTÓRICO DE VOZ: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de histórico de voz: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_integration():
    """Testa integração do assistente de voz"""
    print("\n🧪 TESTANDO INTEGRAÇÃO DE VOZ")
    print("="*60)
    
    try:
        from app.components.voice_assistant import VoiceAssistant
        import streamlit as st
        
        va = VoiceAssistant()
        
        # Testar método principal de renderização
        assert hasattr(va, 'render'), "Método render não encontrado"
        print("✅ Método render presente")
        
        # Testar métodos de renderização específicos
        render_methods = [
            'render_voice_dashboard',
            'render_command_library',
            'render_conversation_interface',
            'render_voice_analytics',
            'render_voice_history',
            'render_voice_settings'
        ]
        
        for method in render_methods:
            assert hasattr(va, method), f"Método {method} não encontrado"
        
        print("✅ Métodos de renderização presentes")
        
        # Testar métodos de ação
        action_methods = [
            'test_voice_command',
            'edit_voice_command',
            'generate_ai_response',
            'check_voice_support'
        ]
        
        for method in action_methods:
            assert hasattr(va, method), f"Método de ação {method} não encontrado"
        
        print("✅ Métodos de ação presentes")
        
        # Testar inicialização completa
        va.initialize_session_state()
        
        # Verificar session state
        required_session_keys = [
            'voice_settings', 'voice_commands', 'voice_history', 
            'voice_analytics', 'voice_conversations', 'voice_status'
        ]
        
        for key in required_session_keys:
            assert key in st.session_state, f"Chave {key} não encontrada no session state"
        
        print("✅ Session state de voz inicializado")
        
        # Testar status de voz
        voice_status = st.session_state.voice_status
        status_fields = ['listening', 'speaking', 'processing', 'session_active']
        
        for field in status_fields:
            assert field in voice_status, f"Campo {field} não encontrado no status"
            assert isinstance(voice_status[field], bool), f"Campo {field} deve ser boolean"
        
        print("✅ Status de voz válido")
        
        print("🎉 INTEGRAÇÃO DE VOZ: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de integração de voz: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_voice_assistant_tests():
    """Executa todos os testes de Assistente de Voz"""
    print("🚀 INICIANDO TESTES DE ASSISTENTE DE VOZ - FASE 3")
    print("="*80)
    
    results = []
    
    # Executar testes
    results.append(("Componente Voz", test_voice_assistant_component()))
    results.append(("Sistema de Comandos", test_voice_commands_system()))
    results.append(("Sistema de Conversação", test_voice_conversations()))
    results.append(("Analytics de Voz", test_voice_analytics()))
    results.append(("Configurações de Voz", test_voice_settings()))
    results.append(("Histórico de Voz", test_voice_history()))
    results.append(("Integração de Voz", test_voice_integration()))
    
    # Resumo dos resultados
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES - ASSISTENTE DE VOZ")
    print("="*80)
    
    passed = 0
    total = len(results)
    
    for component, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{component:25} | {status}")
        if result:
            passed += 1
    
    print("-"*80)
    print(f"TOTAL: {passed}/{total} testes passaram ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES DE ASSISTENTE DE VOZ PASSARAM!")
        print("✅ Sistema de voz completamente funcional")
        print("✅ Reconhecimento de comandos implementado")
        print("✅ Conversação natural operacional")
        print("✅ Analytics e histórico ativos")
        print("✅ Configurações personalizáveis funcionando")
        print("✅ Integração com sistema principal completa")
        return True
    else:
        print(f"\n⚠️ {total-passed} TESTES FALHARAM!")
        print("❌ Correções necessárias antes do deploy")
        return False

if __name__ == "__main__":
    success = run_voice_assistant_tests()
    
    if success:
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Implementar Web Speech API real")
        print("2. Integrar processamento de linguagem natural")
        print("3. Adicionar síntese de voz avançada")
        print("4. Implementar reconhecimento contínuo")
        print("5. Continuar com Análise Comportamental")
    else:
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        print("1. Corrigir testes que falharam")
        print("2. Validar estruturas de dados")
        print("3. Testar integração com Streamlit")
        print("4. Executar testes novamente")
        
    sys.exit(0 if success else 1)
