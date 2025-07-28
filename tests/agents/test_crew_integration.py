from unittest.mock import MagicMock, patch

import pytest

from app.crew import run_crew


class TestCrewIntegration:
    """Testes de integração para agentes CrewAI"""

    @pytest.fixture
    def sample_crew_params(self):
        """Parâmetros de exemplo para execução do crew"""
        return {
            "cargo": "Analista Judiciário",
            "concurso": "TRF",
            "banca": "CESPE",
            "cidade": "Brasília",
            "study_hours": 20,
            "study_months": 6
        }

    @patch('app.crew.create_search_agent')
    @patch('app.crew.create_study_plan_agent')
    @patch('app.crew.create_mock_exam_agent')
    @patch('app.crew.create_writing_agent')
    @patch('app.crew.create_coordinator_agent')
    @patch('app.crew.create_spaced_repetition_agent')
    @patch('app.crew.create_performance_prediction_agent')
    @patch('crewai.Crew')
    def test_crew_complete_workflow(self, mock_crew_class, mock_perf_agent,
                                   mock_spaced_agent, mock_coord_agent,
                                   mock_writing_agent, mock_exam_agent,
                                   mock_study_agent, mock_search_agent,
                                   sample_crew_params):
        """Testa workflow completo do crew"""

        # Mock dos agentes
        mock_search_agent.return_value = MagicMock()
        mock_study_agent.return_value = MagicMock()
        mock_exam_agent.return_value = MagicMock()
        mock_writing_agent.return_value = MagicMock()
        mock_coord_agent.return_value = MagicMock()
        mock_spaced_agent.return_value = MagicMock()
        mock_perf_agent.return_value = MagicMock()

        # Mock do resultado do crew
        mock_result = MagicMock()
        mock_result.tasks_output = [
            MagicMock(raw="Dados de provas encontrados"),
            MagicMock(raw='{"semanas": [{"topico": "Português", "horas": 4}]}'),
            MagicMock(raw="Simulado com 20 questões"),
            MagicMock(raw='{"revisoes": [{"dia": 1, "topico": "Português"}]}'),
            MagicMock(raw='{"predicao": 75.5, "probabilidade": 0.8}')
        ]

        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = mock_result
        mock_crew_class.return_value = mock_crew_instance

        # Executar crew
        result = run_crew(**sample_crew_params)

        # Verificar estrutura do resultado
        assert "exam_data" in result
        assert "study_plan" in result
        assert "mock_exam" in result
        assert "spaced_repetition_plan" in result
        assert "performance_prediction" in result

        # Verificar que o crew foi chamado
        mock_crew_class.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()

    @patch('app.crew.create_search_agent')
    @patch('app.crew.create_study_plan_agent')
    @patch('app.crew.create_mock_exam_agent')
    @patch('app.crew.create_spaced_repetition_agent')
    @patch('app.crew.create_performance_prediction_agent')
    @patch('crewai.Crew')
    def test_crew_with_different_bancas(self, mock_crew_class, mock_perf_agent,
                                       mock_spaced_agent, mock_exam_agent,
                                       mock_study_agent, mock_search_agent):
        """Testa crew com diferentes bancas"""

        # Mock setup
        mock_search_agent.return_value = MagicMock()
        mock_study_agent.return_value = MagicMock()
        mock_exam_agent.return_value = MagicMock()
        mock_spaced_agent.return_value = MagicMock()
        mock_perf_agent.return_value = MagicMock()

        mock_result = MagicMock()
        mock_result.tasks_output = [
            MagicMock(raw="Dados de provas"),
            MagicMock(raw='{"semanas": []}'),
            MagicMock(raw="Simulado"),
            MagicMock(raw='{"revisoes": []}'),
            MagicMock(raw='{"predicao": 70.0}')
        ]

        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = mock_result
        mock_crew_class.return_value = mock_crew_instance

        # Testar com diferentes bancas
        bancas = ["CESPE", "FCC", "VUNESP", "FGV", "IBFC"]

        for banca in bancas:
            params = {
                "cargo": "Analista",
                "concurso": "Teste",
                "banca": banca,
                "cidade": "São Paulo",
                "study_hours": 15,
                "study_months": 4
            }

            result = run_crew(**params)

            assert "exam_data" in result
            assert "study_plan" in result
            assert "mock_exam" in result
            assert "spaced_repetition_plan" in result
            assert "performance_prediction" in result

    @patch('app.crew.create_search_agent')
    @patch('app.crew.create_study_plan_agent')
    @patch('app.crew.create_mock_exam_agent')
    @patch('app.crew.create_spaced_repetition_agent')
    @patch('app.crew.create_performance_prediction_agent')
    @patch('crewai.Crew')
    def test_crew_with_different_study_hours(self, mock_crew_class, mock_perf_agent,
                                            mock_spaced_agent, mock_exam_agent,
                                            mock_study_agent, mock_search_agent):
        """Testa crew com diferentes horas de estudo"""

        # Mock setup
        mock_search_agent.return_value = MagicMock()
        mock_study_agent.return_value = MagicMock()
        mock_exam_agent.return_value = MagicMock()
        mock_spaced_agent.return_value = MagicMock()
        mock_perf_agent.return_value = MagicMock()

        mock_result = MagicMock()
        mock_result.tasks_output = [
            MagicMock(raw="Dados de provas"),
            MagicMock(raw='{"semanas": []}'),
            MagicMock(raw="Simulado"),
            MagicMock(raw='{"revisoes": []}'),
            MagicMock(raw='{"predicao": 70.0}')
        ]

        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = mock_result
        mock_crew_class.return_value = mock_crew_instance

        # Testar com diferentes horas de estudo
        study_hours_list = [10, 15, 20, 25, 30]

        for hours in study_hours_list:
            params = {
                "cargo": "Analista",
                "concurso": "Teste",
                "banca": "CESPE",
                "cidade": "Brasília",
                "study_hours": hours,
                "study_months": 6
            }

            result = run_crew(**params)

            assert "exam_data" in result
            assert "study_plan" in result
            assert "mock_exam" in result
            assert "spaced_repetition_plan" in result
            assert "performance_prediction" in result

    @patch('app.crew.create_search_agent')
    @patch('app.crew.create_study_plan_agent')
    @patch('app.crew.create_mock_exam_agent')
    @patch('app.crew.create_spaced_repetition_agent')
    @patch('app.crew.create_performance_prediction_agent')
    @patch('crewai.Crew')
    def test_crew_with_different_study_months(self, mock_crew_class, mock_perf_agent,
                                             mock_spaced_agent, mock_exam_agent,
                                             mock_study_agent, mock_search_agent):
        """Testa crew com diferentes meses de estudo"""

        # Mock setup
        mock_search_agent.return_value = MagicMock()
        mock_study_agent.return_value = MagicMock()
        mock_exam_agent.return_value = MagicMock()
        mock_spaced_agent.return_value = MagicMock()
        mock_perf_agent.return_value = MagicMock()

        mock_result = MagicMock()
        mock_result.tasks_output = [
            MagicMock(raw="Dados de provas"),
            MagicMock(raw='{"semanas": []}'),
            MagicMock(raw="Simulado"),
            MagicMock(raw='{"revisoes": []}'),
            MagicMock(raw='{"predicao": 70.0}')
        ]

        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = mock_result
        mock_crew_class.return_value = mock_crew_instance

        # Testar com diferentes meses de estudo
        study_months_list = [3, 6, 9, 12]

        for months in study_months_list:
            params = {
                "cargo": "Analista",
                "concurso": "Teste",
                "banca": "CESPE",
                "cidade": "Brasília",
                "study_hours": 20,
                "study_months": months
            }

            result = run_crew(**params)

            assert "exam_data" in result
            assert "study_plan" in result
            assert "mock_exam" in result
            assert "spaced_repetition_plan" in result
            assert "performance_prediction" in result

    @patch('app.crew.create_search_agent')
    @patch('app.crew.create_study_plan_agent')
    @patch('app.crew.create_mock_exam_agent')
    @patch('app.crew.create_spaced_repetition_agent')
    @patch('app.crew.create_performance_prediction_agent')
    @patch('crewai.Crew')
    def test_crew_error_handling(self, mock_crew_class, mock_perf_agent,
                                mock_spaced_agent, mock_exam_agent,
                                mock_study_agent, mock_search_agent):
        """Testa tratamento de erros no crew"""

        # Mock setup
        mock_search_agent.return_value = MagicMock()
        mock_study_agent.return_value = MagicMock()
        mock_exam_agent.return_value = MagicMock()
        mock_spaced_agent.return_value = MagicMock()
        mock_perf_agent.return_value = MagicMock()

        # Simular erro no crew
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.side_effect = Exception("Erro no crew")
        mock_crew_class.return_value = mock_crew_instance

        params = {
            "cargo": "Analista",
            "concurso": "Teste",
            "banca": "CESPE",
            "cidade": "Brasília",
            "study_hours": 20,
            "study_months": 6
        }

        # Deve lançar exceção
        with pytest.raises(Exception) as exc_info:
            run_crew(**params)

        assert "Erro no crew" in str(exc_info.value)

    @patch('app.crew.create_search_agent')
    @patch('app.crew.create_study_plan_agent')
    @patch('app.crew.create_mock_exam_agent')
    @patch('app.crew.create_spaced_repetition_agent')
    @patch('app.crew.create_performance_prediction_agent')
    @patch('crewai.Crew')
    def test_crew_task_output_validation(self, mock_crew_class, mock_perf_agent,
                                        mock_spaced_agent, mock_exam_agent,
                                        mock_study_agent, mock_search_agent):
        """Testa validação das saídas das tarefas"""

        # Mock setup
        mock_search_agent.return_value = MagicMock()
        mock_study_agent.return_value = MagicMock()
        mock_exam_agent.return_value = MagicMock()
        mock_spaced_agent.return_value = MagicMock()
        mock_perf_agent.return_value = MagicMock()

        # Mock com saídas específicas para validação
        mock_result = MagicMock()
        mock_result.tasks_output = [
            MagicMock(raw="Provas encontradas: TRF 2023, TRF 2022"),
            MagicMock(raw='{"semanas": [{"topico": "Português", "horas": 4, "objetivos": ["Gramática", "Interpretação"]}]}'),
            MagicMock(raw="Simulado TRF CESPE - 20 questões\n1. Questão sobre português\n2. Questão sobre direito"),
            MagicMock(raw='{"revisoes": [{"dia": 1, "topico": "Português", "tipo": "flashcard"}, {"dia": 3, "topico": "Direito", "tipo": "simulado"}]}'),
            MagicMock(raw='{"predicao": 78.5, "probabilidade": 0.85, "fatores": ["consistencia", "tempo_estudo"]}')
        ]

        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = mock_result
        mock_crew_class.return_value = mock_crew_instance

        params = {
            "cargo": "Analista Judiciário",
            "concurso": "TRF",
            "banca": "CESPE",
            "cidade": "Brasília",
            "study_hours": 20,
            "study_months": 6
        }

        result = run_crew(**params)

        # Validar conteúdo das saídas
        assert "exam_data" in result
        assert "study_plan" in result
        assert "mock_exam" in result
        assert "spaced_repetition_plan" in result
        assert "performance_prediction" in result

        # Validar conteúdo específico
        assert "TRF" in result["exam_data"]
        assert "semanas" in result["study_plan"]
        assert "questões" in result["mock_exam"].lower()
        assert "revisoes" in result["spaced_repetition_plan"]
        assert "predicao" in result["performance_prediction"]

    @patch('app.crew.create_search_agent')
    @patch('app.crew.create_study_plan_agent')
    @patch('app.crew.create_mock_exam_agent')
    @patch('app.crew.create_spaced_repetition_agent')
    @patch('app.crew.create_performance_prediction_agent')
    @patch('crewai.Crew')
    def test_crew_agent_creation(self, mock_crew_class, mock_perf_agent,
                                mock_spaced_agent, mock_exam_agent,
                                mock_study_agent, mock_search_agent):
        """Testa criação correta dos agentes"""

        # Mock setup
        mock_search_agent.return_value = MagicMock()
        mock_study_agent.return_value = MagicMock()
        mock_exam_agent.return_value = MagicMock()
        mock_spaced_agent.return_value = MagicMock()
        mock_perf_agent.return_value = MagicMock()

        mock_result = MagicMock()
        mock_result.tasks_output = [
            MagicMock(raw="Dados de provas"),
            MagicMock(raw='{"semanas": []}'),
            MagicMock(raw="Simulado"),
            MagicMock(raw='{"revisoes": []}'),
            MagicMock(raw='{"predicao": 70.0}')
        ]

        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = mock_result
        mock_crew_class.return_value = mock_crew_instance

        params = {
            "cargo": "Analista",
            "concurso": "Teste",
            "banca": "CESPE",
            "cidade": "Brasília",
            "study_hours": 20,
            "study_months": 6
        }

        run_crew(**params)

        # Verificar se todos os agentes foram criados
        mock_search_agent.assert_called_once()
        mock_study_agent.assert_called_once()
        mock_exam_agent.assert_called_once()
        mock_spaced_agent.assert_called_once()
        mock_perf_agent.assert_called_once()

        # Verificar se o crew foi criado com os agentes corretos
        mock_crew_class.assert_called_once()
        call_args = mock_crew_class.call_args

        # Verificar se os agentes estão na lista de agentes
        agents_arg = call_args[1]['agents']
        assert len(agents_arg) == 5  # 5 agentes principais

        # Verificar se as tarefas estão na lista de tarefas
        tasks_arg = call_args[1]['tasks']
        assert len(tasks_arg) == 5  # 5 tarefas principais
