import hashlib
import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

# Configurar logger local
logger = logging.getLogger(__name__)

# Exceções locais
class ExternalServiceError(Exception):
    def __init__(self, service: str, message: str, details: Dict = None):
        self.service = service
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class RateLimitError(Exception):
    def __init__(self, service: str, retry_after: int, details: Dict = None):
        self.service = service
        self.retry_after = retry_after
        self.details = details or {}
        super().__init__(f"Rate limit exceeded for {service}")

def log_agent_execution(logger, agent_name: str, action: str, duration: float, success: bool, error: str = None):
    """Função local para logging de execução de agentes"""
    level = logging.INFO if success else logging.ERROR
    message = f"Agent {agent_name} executed {action} in {duration:.2f}s"
    if error:
        message += f" with error: {error}"
    logger.log(level, message)

class QuestionAPITool:
    """Ferramenta para integração com APIs de questões de concursos"""

    def __init__(self):
        self.name = "QuestionAPITool"
        self.description = "Ferramenta para buscar questões de concursos em APIs externas"

        # Configurações das APIs
        self.apis = {
            "qconcursos": {
                "base_url": "https://api.qconcursos.com",
                "api_key": None,  # Configurar via variável de ambiente
                "rate_limit": {"requests": 100, "window": 3600},  # 100 requests/hora
                "endpoints": {
                    "search": "/questions/search",
                    "details": "/questions/{id}",
                    "subjects": "/subjects",
                    "exams": "/exams"
                }
            },
            "cespe": {
                "base_url": "https://api.cespe.unb.br",
                "api_key": None,
                "rate_limit": {"requests": 50, "window": 3600},
                "endpoints": {
                    "questions": "/questions",
                    "exams": "/exams"
                }
            },
            "fcc": {
                "base_url": "https://api.fcc.org.br",
                "api_key": None,
                "rate_limit": {"requests": 80, "window": 3600},
                "endpoints": {
                    "questions": "/questions",
                    "exams": "/exams"
                }
            }
        }

        # Cache local para reduzir chamadas à API
        self.cache = {}
        self.cache_ttl = 3600  # 1 hora

        # Controle de rate limiting
        self.request_history = {}

        # Headers padrão
        self.default_headers = {
            "User-Agent": "AgenteConcurseiro/2.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _get_api_key(self, api_name: str) -> Optional[str]:
        """Obtém chave da API do ambiente"""
        env_var = f"{api_name.upper()}_API_KEY"
        return os.getenv(env_var)

    def _check_rate_limit(self, api_name: str) -> bool:
        """Verifica rate limit para a API"""
        if api_name not in self.request_history:
            self.request_history[api_name] = []

        current_time = time.time()
        window_start = current_time - self.apis[api_name]["rate_limit"]["window"]

        # Limpar histórico antigo
        self.request_history[api_name] = [
            req_time for req_time in self.request_history[api_name]
            if req_time > window_start
        ]

        # Verificar se excedeu o limite
        if len(self.request_history[api_name]) >= self.apis[api_name]["rate_limit"]["requests"]:
            return False

        # Adicionar requisição atual
        self.request_history[api_name].append(current_time)
        return True

    def _get_cache_key(self, api_name: str, params: Dict[str, Any]) -> str:
        """Gera chave de cache"""
        param_str = json.dumps(params, sort_keys=True)
        return f"{api_name}:{hashlib.md5(param_str.encode()).hexdigest()}"

    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Obtém dados do cache"""
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
            else:
                del self.cache[cache_key]
        return None

    def _save_to_cache(self, cache_key: str, data: Dict[str, Any]):
        """Salva dados no cache"""
        self.cache[cache_key] = (data, time.time())

    def _make_request(self, api_name: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Faz requisição para a API"""

        # Verificar rate limit
        if not self._check_rate_limit(api_name):
            raise RateLimitError(
                service=api_name,
                retry_after=self.apis[api_name]["rate_limit"]["window"],
                details={"api": api_name, "endpoint": endpoint}
            )

        # Obter configurações da API
        api_config = self.apis[api_name]
        api_key = self._get_api_key(api_name)

        # Preparar headers
        headers = self.default_headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        # Preparar URL
        url = f"{api_config['base_url']}{endpoint}"

        # Fazer requisição
        try:
            start_time = time.time()

            if params:
                response = requests.get(url, headers=headers, params=params, timeout=30)
            else:
                response = requests.get(url, headers=headers, timeout=30)

            duration = time.time() - start_time

            # Log da requisição
            log_agent_execution(
                logger,
                f"{api_name}_api",
                endpoint,
                duration,
                response.status_code < 400,
                None if response.status_code < 400 else f"HTTP {response.status_code}"
            )

            # Verificar status da resposta
            if response.status_code == 429:
                raise RateLimitError(
                    service=api_name,
                    retry_after=int(response.headers.get("Retry-After", 300)),
                    details={"api": api_name, "endpoint": endpoint}
                )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            raise ExternalServiceError(
                service=api_name,
                message=f"Erro na requisição para {api_name}: {str(e)}",
                details={"endpoint": endpoint, "params": params}
            )

    def search_questions(self, api_name: str, query: str, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Busca questões na API especificada"""

        if api_name not in self.apis:
            raise ValueError(f"API '{api_name}' não suportada")

        # Preparar parâmetros
        params = {"q": query}
        if filters:
            params.update(filters)

        # Verificar cache
        cache_key = self._get_cache_key(api_name, params)
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            logger.info(f"Retrieved from cache: {api_name} search for '{query}'")
            return cached_result

        # Fazer requisição
        endpoint = self.apis[api_name]["endpoints"]["search"]
        result = self._make_request(api_name, endpoint, params)

        # Salvar no cache
        self._save_to_cache(cache_key, result)

        return result

    def get_question_details(self, api_name: str, question_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma questão específica"""

        if api_name not in self.apis:
            raise ValueError(f"API '{api_name}' não suportada")

        # Verificar cache
        cache_key = f"{api_name}:question:{question_id}"
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result

        # Fazer requisição
        endpoint = self.apis[api_name]["endpoints"]["details"].format(id=question_id)
        result = self._make_request(api_name, endpoint)

        # Salvar no cache
        self._save_to_cache(cache_key, result)

        return result

    def get_subjects(self, api_name: str) -> List[Dict[str, Any]]:
        """Obtém lista de disciplinas disponíveis"""

        if api_name not in self.apis:
            raise ValueError(f"API '{api_name}' não suportada")

        # Verificar cache
        cache_key = f"{api_name}:subjects"
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result

        # Fazer requisição
        endpoint = self.apis[api_name]["endpoints"]["subjects"]
        result = self._make_request(api_name, endpoint)

        # Salvar no cache
        self._save_to_cache(cache_key, result)

        return result

    def get_exams(self, api_name: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Obtém lista de concursos disponíveis"""

        if api_name not in self.apis:
            raise ValueError(f"API '{api_name}' não suportada")

        # Verificar cache
        cache_key = self._get_cache_key(f"{api_name}:exams", filters or {})
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result

        # Fazer requisição
        endpoint = self.apis[api_name]["endpoints"]["exams"]
        result = self._make_request(api_name, endpoint, filters)

        # Salvar no cache
        self._save_to_cache(cache_key, result)

        return result

    def create_mock_exam(self, api_name: str, subjects: List[str], num_questions: int = 20) -> Dict[str, Any]:
        """Cria um simulado com questões da API"""

        questions = []

        # Buscar questões para cada disciplina
        for subject in subjects:
            try:
                subject_questions = self.search_questions(
                    api_name,
                    subject,
                    {"limit": num_questions // len(subjects)}
                )

                if "questions" in subject_questions:
                    questions.extend(subject_questions["questions"])

            except Exception as e:
                logger.warning(f"Erro ao buscar questões de {subject}: {e}")
                continue

        # Embaralhar questões
        import random
        random.shuffle(questions)

        # Limitar número de questões
        questions = questions[:num_questions]

        return {
            "exam_id": f"mock_{api_name}_{int(time.time())}",
            "title": f"Simulado {api_name.upper()}",
            "subjects": subjects,
            "num_questions": len(questions),
            "questions": questions,
            "created_at": datetime.utcnow().isoformat()
        }

    def get_question_statistics(self, api_name: str, question_id: str) -> Dict[str, Any]:
        """Obtém estatísticas de uma questão (se disponível)"""

        try:
            question_data = self.get_question_details(api_name, question_id)

            # Extrair estatísticas se disponíveis
            stats = {
                "question_id": question_id,
                "api": api_name,
                "difficulty": question_data.get("difficulty", "unknown"),
                "success_rate": question_data.get("success_rate", 0),
                "attempts": question_data.get("attempts", 0),
                "correct_answers": question_data.get("correct_answers", 0),
                "wrong_answers": question_data.get("wrong_answers", 0)
            }

            return stats

        except Exception as e:
            logger.error(f"Erro ao obter estatísticas da questão {question_id}: {e}")
            return {
                "question_id": question_id,
                "api": api_name,
                "error": str(e)
            }

    def _run(self, action: str, params_json: str) -> str:
        """Método principal da ferramenta"""

        try:
            params = json.loads(params_json)
            action = action.lower()

            if action == "search_questions":
                api_name = params.get("api_name", "qconcursos")
                query = params.get("query", "")
                filters = params.get("filters", {})

                result = self.search_questions(api_name, query, filters)
                return json.dumps(result, ensure_ascii=False)

            elif action == "get_question_details":
                api_name = params.get("api_name", "qconcursos")
                question_id = params.get("question_id")

                if not question_id:
                    raise ValueError("question_id é obrigatório")

                result = self.get_question_details(api_name, question_id)
                return json.dumps(result, ensure_ascii=False)

            elif action == "get_subjects":
                api_name = params.get("api_name", "qconcursos")
                result = self.get_subjects(api_name)
                return json.dumps(result, ensure_ascii=False)

            elif action == "get_exams":
                api_name = params.get("api_name", "qconcursos")
                filters = params.get("filters", {})
                result = self.get_exams(api_name, filters)
                return json.dumps(result, ensure_ascii=False)

            elif action == "create_mock_exam":
                api_name = params.get("api_name", "qconcursos")
                subjects = params.get("subjects", [])
                num_questions = params.get("num_questions", 20)

                if not subjects:
                    raise ValueError("subjects é obrigatório")

                result = self.create_mock_exam(api_name, subjects, num_questions)
                return json.dumps(result, ensure_ascii=False)

            elif action == "get_question_statistics":
                api_name = params.get("api_name", "qconcursos")
                question_id = params.get("question_id")

                if not question_id:
                    raise ValueError("question_id é obrigatório")

                result = self.get_question_statistics(api_name, question_id)
                return json.dumps(result, ensure_ascii=False)

            else:
                return json.dumps({
                    "error": f"Ação '{action}' não reconhecida",
                    "available_actions": [
                        "search_questions",
                        "get_question_details",
                        "get_subjects",
                        "get_exams",
                        "create_mock_exam",
                        "get_question_statistics"
                    ]
                }, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Erro na QuestionAPITool: {e}")
            return json.dumps({
                "error": f"Erro na ferramenta: {str(e)}"
            }, ensure_ascii=False)

# Instância global
question_api_tool = QuestionAPITool()
