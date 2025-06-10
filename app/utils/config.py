import json
import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Carrega configurações do aplicativo"""
    config_path = "config/app_config.json"
    
    # Verificar se o arquivo existe
    if not os.path.exists(config_path):
        # Criar configuração padrão
        default_config = {
            "app": {
                "name": "Assistente de Preparação para Concursos",
                "version": "2.0.0",
                "debug": True,
                "environment": "development"
            },
            "features": {
                "dashboard": True,
                "study_plan": True,
                "materials": True,
                "writing": True,
                "mock_exam": True,
                "spaced_repetition": True,
                "performance_prediction": True,
                "calendar_integration": False,
                "notifications": True
            },
            "api_keys": {
                "openai": "",
                "serp": "",
                "google_calendar": "",
                "outlook": ""
            },
            "default_settings": {
                "study_hours": 20,
                "study_months": 6,
                "default_banca": "CESPE",
                "default_difficulty": "medium",
                "questions_per_quiz": 10,
                "session_timeout_minutes": 120
            },
            "database": {
                "type": "sqlite",
                "path": "data/app.db",
                "backup_enabled": True,
                "backup_interval_hours": 24
            },
            "crew_ai": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 2000,
                "timeout": 30
            },
            "ui": {
                "theme": "light",
                "language": "pt-BR",
                "items_per_page": 20,
                "auto_save": True,
                "show_tips": True
            },
            "study": {
                "supported_bancas": ["CESPE", "FCC", "VUNESP", "FGV", "IBFC"],
                "supported_subjects": [
                    "Português", "Matemática", "Direito Constitucional",
                    "Direito Administrativo", "Informática", "Conhecimentos Específicos",
                    "Atualidades", "Raciocínio Lógico"
                ],
                "difficulty_levels": ["easy", "medium", "hard", "mixed"]
            },
            "notifications": {
                "email_enabled": False,
                "push_enabled": True,
                "study_reminders": True,
                "performance_alerts": True,
                "daily_quiz": True
            }
        }
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Salvar configuração padrão
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    # Carregar configuração existente
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Erro ao carregar configuração: {str(e)}")
        return {}

def save_config(config: Dict[str, Any]) -> bool:
    """Salva configurações do aplicativo"""
    config_path = "config/app_config.json"
    
    try:
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Salvar configuração
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Erro ao salvar configuração: {str(e)}")
        return False

def get_api_key(service: str) -> str:
    """Obtém chave de API para um serviço específico"""
    config = load_config()
    
    # Verificar se a chave existe na configuração
    if "api_keys" in config and service in config["api_keys"]:
        return config["api_keys"][service]
    
    # Verificar se a chave existe como variável de ambiente
    env_key = f"{service.upper()}_API_KEY"
    if env_key in os.environ:
        return os.environ[env_key]
    
    return ""