"""
🧪 Testes para Voice Assistant - Assistente de Voz
Validação completa do componente de reconhecimento de voz
"""

import pytest
import streamlit as st
from datetime import datetime
from app.components.voice_assistant import (
    VoiceAssistant,
    VoiceCommandType,
    VoiceLanguage,
    VoiceGender
)

class TestVoiceAssistant:
    """Testes para o componente Voice Assistant"""
    
    def setup_method(self):
        """Setup para cada teste"""
        # Limpar session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        self.voice_assistant = VoiceAssistant()
    
    def test_voice_assistant_initialization(self):
        """Testar inicialização do assistente de voz"""
        assert self.voice_assistant is not None
        assert 'voice_settings' in st.session_state
        assert 'voice_commands' in st.session_state
        assert 'voice_history' in st.session_state
        assert 'voice_analytics' in st.session_state
    
    def test_voice_settings_default_values(self):
        """Testar valores padrão das configurações"""
        settings = st.session_state.voice_settings
        
        assert settings['enabled'] == True
        assert settings['language'] == VoiceLanguage.PT_BR.value
        assert settings['voice_gender'] == VoiceGender.FEMALE.value
        assert settings['speech_rate'] == 1.0
        assert settings['volume'] == 0.8
        assert settings['auto_read'] == False
        assert settings['wake_word'] == "agente"
        assert settings['continuous_listening'] == False
    
    def test_voice_commands_generation(self):
        """Testar geração de comandos de voz"""
        commands = st.session_state.voice_commands
        
        assert len(commands) == 10
        assert all('id' in cmd for cmd in commands)
        assert all('command' in cmd for cmd in commands)
        assert all('type' in cmd for cmd in commands)
        assert all('action' in cmd for cmd in commands)
        assert all('examples' in cmd for cmd in commands)
        
        # Verificar tipos de comando
        command_types = [cmd['type'] for cmd in commands]
        assert VoiceCommandType.NAVIGATION.value in command_types
        assert VoiceCommandType.CONTENT_READ.value in command_types
        assert VoiceCommandType.QUIZ_CONTROL.value in command_types
    
    def test_voice_command_processing_success(self):
        """Testar processamento bem-sucedido de comando"""
        result = self.voice_assistant.process_voice_command("ler questão")
        
        assert result['success'] == True
        assert 'command_id' in result
        assert 'action' in result
        assert 'confidence' in result
        assert 'response' in result
        assert 'timestamp' in result
        
        # Verificar se foi adicionado ao histórico
        assert len(st.session_state.voice_history) == 1
        history_entry = st.session_state.voice_history[0]
        assert history_entry['success'] == True
        assert history_entry['command'] == "ler questão"
    
    def test_voice_command_processing_failure(self):
        """Testar processamento de comando não reconhecido"""
        result = self.voice_assistant.process_voice_command("comando inexistente")
        
        assert result['success'] == False
        assert 'error' in result
        assert 'suggestion' in result
        assert result['error'] == 'Comando não reconhecido'
        
        # Verificar histórico
        assert len(st.session_state.voice_history) == 1
        history_entry = st.session_state.voice_history[0]
        assert history_entry['success'] == False
        assert history_entry['confidence'] == 0.0
    
    def test_text_to_speech_simulation(self):
        """Testar simulação de síntese de voz"""
        test_text = "Este é um teste de síntese de voz"
        result = self.voice_assistant.text_to_speech_simulation(test_text)
        
        assert result['text'] == test_text
        assert result['language'] == VoiceLanguage.PT_BR.value
        assert result['voice_gender'] == VoiceGender.FEMALE.value
        assert result['speech_rate'] == 1.0
        assert result['volume'] == 0.8
        assert 'estimated_duration' in result
        assert result['status'] == 'ready_to_play'
        
        # Testar cálculo de duração
        words = len(test_text.split())
        expected_duration = (words * 0.6) / 1.0  # speech_rate = 1.0
        assert abs(result['estimated_duration'] - expected_duration) < 0.1
    
    def test_voice_suggestions_by_context(self):
        """Testar sugestões de comandos por contexto"""
        # Contexto geral
        general_suggestions = self.voice_assistant.get_voice_suggestions("general")
        assert len(general_suggestions) == 3
        assert any("ajuda" in suggestion for suggestion in general_suggestions)
        
        # Contexto de quiz
        quiz_suggestions = self.voice_assistant.get_voice_suggestions("quiz")
        assert len(quiz_suggestions) == 3
        assert any("próxima questão" in suggestion for suggestion in quiz_suggestions)
        
        # Contexto de dashboard
        dashboard_suggestions = self.voice_assistant.get_voice_suggestions("dashboard")
        assert len(dashboard_suggestions) == 3
        assert any("mostrar desempenho" in suggestion for suggestion in dashboard_suggestions)
        
        # Contexto inexistente (deve retornar geral)
        unknown_suggestions = self.voice_assistant.get_voice_suggestions("unknown")
        assert unknown_suggestions == general_suggestions
    
    def test_voice_analytics_structure(self):
        """Testar estrutura dos analytics de voz"""
        analytics = st.session_state.voice_analytics
        
        # Verificar campos obrigatórios
        required_fields = [
            'total_commands', 'successful_recognitions', 'accuracy_rate',
            'average_response_time', 'most_used_commands', 'usage_by_type',
            'daily_usage', 'satisfaction_score', 'error_types'
        ]
        
        for field in required_fields:
            assert field in analytics
        
        # Verificar tipos de dados
        assert isinstance(analytics['total_commands'], int)
        assert isinstance(analytics['accuracy_rate'], float)
        assert isinstance(analytics['most_used_commands'], list)
        assert isinstance(analytics['usage_by_type'], dict)
        assert isinstance(analytics['daily_usage'], list)
        
        # Verificar comandos mais usados
        most_used = analytics['most_used_commands']
        assert len(most_used) == 5
        assert all('command' in cmd and 'count' in cmd for cmd in most_used)
    
    def test_command_recognition_examples(self):
        """Testar reconhecimento de diferentes exemplos de comando"""
        test_cases = [
            ("ir para dashboard", True),
            ("abrir dashboard", True),
            ("mostrar painel", True),
            ("ler questão", True),
            ("leia a pergunta", True),
            ("fale a questão", True),
            ("iniciar simulado", True),
            ("começar prova", True),
            ("comando inválido", False),
            ("", False)
        ]
        
        for command, should_succeed in test_cases:
            result = self.voice_assistant.process_voice_command(command)
            assert result['success'] == should_succeed, f"Falha no comando: {command}"
    
    def test_voice_history_tracking(self):
        """Testar rastreamento do histórico de comandos"""
        # Executar vários comandos
        commands = ["ler questão", "próxima questão", "comando inválido", "pausar"]
        
        for cmd in commands:
            self.voice_assistant.process_voice_command(cmd)
        
        # Verificar histórico
        history = st.session_state.voice_history
        assert len(history) == len(commands)
        
        # Verificar estrutura dos entries
        for entry in history:
            assert 'timestamp' in entry
            assert 'command' in entry
            assert 'success' in entry
            assert 'confidence' in entry
            assert 'response_time' in entry
            
            # Verificar timestamp válido
            datetime.fromisoformat(entry['timestamp'])
    
    def test_speech_rate_adjustment(self):
        """Testar ajuste da velocidade de fala"""
        test_text = "Teste de velocidade de fala"
        
        # Testar diferentes velocidades
        speech_rates = [0.5, 1.0, 1.5, 2.0]
        
        for rate in speech_rates:
            st.session_state.voice_settings['speech_rate'] = rate
            result = self.voice_assistant.text_to_speech_simulation(test_text)
            
            assert result['speech_rate'] == rate
            
            # Verificar se a duração é inversamente proporcional à velocidade
            words = len(test_text.split())
            expected_duration = (words * 0.6) / rate
            assert abs(result['estimated_duration'] - expected_duration) < 0.1

def test_voice_assistant_component():
    """Teste de integração do componente"""
    # Limpar session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Testar inicialização
    voice_assistant = VoiceAssistant()
    assert voice_assistant is not None
    
    # Testar session state
    assert 'voice_settings' in st.session_state
    assert 'voice_commands' in st.session_state
    assert 'voice_history' in st.session_state
    assert 'voice_analytics' in st.session_state

def test_voice_command_types_enum():
    """Testar enum de tipos de comando"""
    assert VoiceCommandType.NAVIGATION.value == "navigation"
    assert VoiceCommandType.CONTENT_READ.value == "content_read"
    assert VoiceCommandType.QUIZ_CONTROL.value == "quiz_control"
    assert VoiceCommandType.STUDY_PLAN.value == "study_plan"
    assert VoiceCommandType.ANALYTICS.value == "analytics"
    assert VoiceCommandType.SETTINGS.value == "settings"

def test_voice_language_enum():
    """Testar enum de idiomas"""
    assert VoiceLanguage.PT_BR.value == "pt-BR"
    assert VoiceLanguage.EN_US.value == "en-US"
    assert VoiceLanguage.ES_ES.value == "es-ES"

def test_voice_gender_enum():
    """Testar enum de gênero de voz"""
    assert VoiceGender.MALE.value == "male"
    assert VoiceGender.FEMALE.value == "female"
    assert VoiceGender.NEUTRAL.value == "neutral"

if __name__ == "__main__":
    # Executar testes
    pytest.main([__file__, "-v"])