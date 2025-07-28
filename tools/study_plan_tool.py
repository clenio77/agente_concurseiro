import datetime
import json

from crewai.tools import BaseTool


class StudyPlanTool(BaseTool):
    name: str = "Ferramenta de Plano de Estudo"
    description: str = "Cria um plano de estudo semanal personalizado com base nas metas e no tempo disponível do usuário."

    def _run(self, metas: str, tempo_disponivel: str) -> str:
        """Cria um plano de estudo semanal personalizado."""
        try:
            semana = {
                "Segunda-feira": "Revisar Português (2h), Exercícios de Matemática (1h)",
                "Terça-feira": "Estudar Direito Constitucional (3h)",
                "Quarta-feira": "Simulado Geral (3h)",
                "Quinta-feira": "Revisar Direito Administrativo (2h), Redação (1h)",
                "Sexta-feira": "Exercícios de Raciocínio Lógico (2h), Leitura de Atualidades (1h)",
                "Sábado": "Revisão semanal e simulado de disciplina específica (4h)",
                "Domingo": "Descanso ou leitura leve"
            }

            plano = {
                "objetivo": metas,
                "disponibilidade": tempo_disponivel,
                "plano_semanal": semana,
                "data_geracao": datetime.datetime.now().isoformat()
            }

            return json.dumps(plano, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao gerar plano de estudo: {e}"

# O decorador @tool não é necessário se você instancia a classe diretamente
# e a passa para o Agent. Se a ferramenta fosse uma função simples,
# o decorador seria usado nela. A estrutura de classe já é a forma correta
# de definir uma ferramenta complexa.
