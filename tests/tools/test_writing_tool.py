import json

import pytest

from tools.writing_tool import WritingTool


class TestWritingTool:
    """Testes unitários para WritingTool"""

    @pytest.fixture
    def writing_tool(self):
        """Fixture para criar instância do WritingTool"""
        return WritingTool()

    @pytest.fixture
    def sample_essay(self):
        """Redação de exemplo para testes"""
        return """
        A sustentabilidade ambiental é um tema de extrema relevância na sociedade contemporânea. 
        O desenvolvimento econômico deve ser equilibrado com a preservação dos recursos naturais 
        para garantir um futuro viável para as próximas gerações.
        
        Em primeiro lugar, é fundamental reconhecer que os recursos naturais são finitos. 
        A exploração desenfreada pode levar ao esgotamento de matérias-primas essenciais, 
        comprometendo não apenas o meio ambiente, mas também a própria economia.
        
        Além disso, as mudanças climáticas representam um desafio global que requer 
        ações coordenadas entre países e setores da sociedade. A implementação de 
        políticas públicas eficazes é essencial para mitigar os impactos ambientais.
        
        Portanto, é necessário buscar um modelo de desenvolvimento que concilie 
        crescimento econômico com responsabilidade ambiental, através de tecnologias 
        limpas e práticas sustentáveis.
        """

    def test_writing_tool_initialization(self, writing_tool):
        """Testa inicialização do WritingTool"""
        assert writing_tool.name == "WritingTool"
        assert "avaliação de redações" in writing_tool.description.lower()
        assert "CESPE" in writing_tool.banca_patterns
        assert "FCC" in writing_tool.banca_patterns
        assert "VUNESP" in writing_tool.banca_patterns

    def test_evaluate_essay_by_banca_cespe(self, writing_tool, sample_essay):
        """Testa avaliação de redação para banca CESPE"""
        result = writing_tool.evaluate_essay_by_banca(sample_essay, "CESPE")

        assert "error" not in result
        assert result["banca"] == "CESPE"
        assert result["tipo_redacao"] == "dissertativo-argumentativo"
        assert "score_final" in result
        assert result["score_final"] > 0
        assert result["score_final"] <= 10
        assert "scores_por_criterio" in result
        assert "feedback_detalhado" in result
        assert "pontos_fortes" in result
        assert "pontos_fracos" in result
        assert "sugestoes_melhoria" in result

    def test_evaluate_essay_by_banca_fcc(self, writing_tool, sample_essay):
        """Testa avaliação de redação para banca FCC"""
        result = writing_tool.evaluate_essay_by_banca(sample_essay, "FCC")

        assert "error" not in result
        assert result["banca"] == "FCC"
        assert "score_final" in result
        assert result["score_final"] > 0
        assert result["score_final"] <= 10

    def test_evaluate_essay_by_banca_vunesp(self, writing_tool, sample_essay):
        """Testa avaliação de redação para banca VUNESP"""
        result = writing_tool.evaluate_essay_by_banca(sample_essay, "VUNESP")

        assert "error" not in result
        assert result["banca"] == "VUNESP"
        assert "score_final" in result
        assert result["score_final"] > 0
        assert result["score_final"] <= 10

    def test_evaluate_essay_by_banca_fgv(self, writing_tool, sample_essay):
        """Testa avaliação de redação para banca FGV"""
        result = writing_tool.evaluate_essay_by_banca(sample_essay, "FGV")

        assert "error" not in result
        assert result["banca"] == "FGV"
        assert "score_final" in result
        assert result["score_final"] > 0
        assert result["score_final"] <= 10

    def test_evaluate_essay_by_banca_ibfc(self, writing_tool, sample_essay):
        """Testa avaliação de redação para banca IBFC"""
        result = writing_tool.evaluate_essay_by_banca(sample_essay, "IBFC")

        assert "error" not in result
        assert result["banca"] == "IBFC"
        assert "score_final" in result
        assert result["score_final"] > 0
        assert result["score_final"] <= 10

    def test_evaluate_essay_invalid_banca(self, writing_tool, sample_essay):
        """Testa avaliação com banca inválida"""
        result = writing_tool.evaluate_essay_by_banca(sample_essay, "BANCA_INVALIDA")

        assert "error" in result
        assert "não suportada" in result["error"].lower()

    def test_evaluate_essay_empty_text(self, writing_tool):
        """Testa avaliação com texto vazio"""
        result = writing_tool.evaluate_essay_by_banca("", "CESPE")

        assert "error" not in result
        assert result["score_final"] >= 0
        assert result["score_final"] <= 10

    def test_evaluate_essay_very_short_text(self, writing_tool):
        """Testa avaliação com texto muito curto"""
        short_text = "Texto muito curto."
        result = writing_tool.evaluate_essay_by_banca(short_text, "CESPE")

        assert "error" not in result
        assert result["score_final"] >= 0
        assert result["score_final"] <= 10

    def test_get_tema_by_banca(self, writing_tool):
        """Testa obtenção de temas por banca"""
        result = writing_tool.get_tema_by_banca("CESPE")

        assert "error" not in result
        assert "temas" in result
        assert len(result["temas"]) > 0

        # Verificar estrutura do tema
        tema = result["temas"][0]
        assert "tema" in tema
        assert "contexto" in tema
        assert "tipo" in tema
        assert "ano" in tema
        assert "cargo" in tema

    def test_get_tema_by_banca_invalid(self, writing_tool):
        """Testa obtenção de temas com banca inválida"""
        result = writing_tool.get_tema_by_banca("BANCA_INVALIDA")

        assert "error" in result
        assert "não suportada" in result["error"].lower()

    def test_get_banca_info(self, writing_tool):
        """Testa obtenção de informações da banca"""
        result = writing_tool.get_banca_info("CESPE")

        assert "error" not in result
        assert "banca" in result
        assert "caracteristicas" in result
        assert "tipos_redacao" in result
        assert "extensao_minima" in result
        assert "extensao_maxima" in result

    def test_get_banca_info_invalid(self, writing_tool):
        """Testa obtenção de informações com banca inválida"""
        result = writing_tool.get_banca_info("BANCA_INVALIDA")

        assert "error" in result
        assert "não suportada" in result["error"].lower()

    def test_run_method_evaluate_essay(self, writing_tool, sample_essay):
        """Testa método _run com ação evaluate_essay"""
        params = {
            "essay_text": sample_essay,
            "banca": "CESPE",
            "tipo_redacao": "dissertativo-argumentativo",
            "tema": "Sustentabilidade ambiental"
        }

        result = writing_tool._run("evaluate_essay", json.dumps(params))
        result_dict = json.loads(result)

        assert "error" not in result_dict
        assert result_dict["banca"] == "CESPE"
        assert "score_final" in result_dict

    def test_run_method_get_tema(self, writing_tool):
        """Testa método _run com ação get_tema"""
        params = {"banca": "CESPE"}

        result = writing_tool._run("get_tema", json.dumps(params))
        result_dict = json.loads(result)

        assert "error" not in result_dict
        assert "temas" in result_dict

    def test_run_method_get_banca_info(self, writing_tool):
        """Testa método _run com ação get_banca_info"""
        params = {"banca": "CESPE"}

        result = writing_tool._run("get_banca_info", json.dumps(params))
        result_dict = json.loads(result)

        assert "error" not in result_dict
        assert "banca" in result_dict

    def test_run_method_invalid_action(self, writing_tool):
        """Testa método _run com ação inválida"""
        params = {"banca": "CESPE"}

        result = writing_tool._run("acao_invalida", json.dumps(params))
        result_dict = json.loads(result)

        assert "error" in result_dict
        assert "não reconhecida" in result_dict["error"].lower()

    def test_run_method_invalid_json(self, writing_tool):
        """Testa método _run com JSON inválido"""
        result = writing_tool._run("evaluate_essay", "json_invalido")
        result_dict = json.loads(result)

        assert "error" in result_dict
        assert "erro na ferramenta" in result_dict["error"].lower()

    def test_evaluation_criteria_structure(self, writing_tool):
        """Testa estrutura dos critérios de avaliação"""
        criterios = writing_tool.evaluation_criteria

        # Verificar tipos de redação
        assert "dissertativo-argumentativo" in criterios
        assert "texto_tecnico" in criterios
        assert "relatorio" in criterios

        # Verificar estrutura dos critérios
        for tipo, config in criterios.items():
            assert "criterios" in config
            assert isinstance(config["criterios"], list)
            assert len(config["criterios"]) > 0

    def test_banca_patterns_structure(self, writing_tool):
        """Testa estrutura dos padrões das bancas"""
        patterns = writing_tool.banca_patterns

        for banca, config in patterns.items():
            assert "tipos_redacao" in config
            assert "extensao_minima" in config
            assert "extensao_maxima" in config
            assert "estrutura_preferida" in config
            assert "estilo" in config
            assert "peso_criterios" in config
            assert "caracteristicas" in config

            # Verificar tipos de redação
            assert isinstance(config["tipos_redacao"], list)
            assert len(config["tipos_redacao"]) > 0

            # Verificar pesos dos critérios
            assert isinstance(config["peso_criterios"], dict)
            assert sum(config["peso_criterios"].values()) > 0.9  # Deve somar aproximadamente 1.0

    def test_tema_bank_structure(self, writing_tool):
        """Testa estrutura do banco de temas"""
        tema_bank = writing_tool.tema_bank

        for banca, temas in tema_bank.items():
            assert isinstance(temas, list)
            assert len(temas) > 0

            for tema in temas:
                assert "tema" in tema
                assert "contexto" in tema
                assert "tipo" in tema
                assert "ano" in tema
                assert "cargo" in tema
