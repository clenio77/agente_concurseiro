import json
import re
from datetime import datetime
from typing import Dict, List


class WritingTool:
    def __init__(self):
        self.name = "WritingTool"
        self.description = "Sistema avançado de avaliação de redações específico por banca"

        # Padrões específicos por banca
        self.banca_patterns = self._initialize_banca_patterns()

        # Banco de temas por banca
        self.tema_bank = self._initialize_tema_bank()

        # Critérios de avaliação por tipo de redação
        self.evaluation_criteria = self._initialize_evaluation_criteria()

    def _initialize_banca_patterns(self) -> Dict:
        """Inicializa padrões específicos por banca"""
        return {
            'CESPE': {
                'tipos_redacao': ['dissertativo-argumentativo', 'texto_tecnico'],
                'extensao_minima': 20,  # linhas
                'extensao_maxima': 30,
                'estrutura_preferida': 'classica',  # intro, desenvolvimento, conclusão
                'estilo': 'formal_tecnico',
                'peso_criterios': {
                    'estrutura': 0.25,
                    'argumentacao': 0.30,
                    'gramatica': 0.20,
                    'coesao': 0.15,
                    'adequacao_tema': 0.10
                },
                'caracteristicas': [
                    'linguagem_tecnica_juridica',
                    'argumentacao_solida',
                    'citacao_legislacao',
                    'impessoalidade',
                    'objetividade'
                ]
            },
            'FCC': {
                'tipos_redacao': ['dissertativo-argumentativo', 'relatorio'],
                'extensao_minima': 25,
                'extensao_maxima': 35,
                'estrutura_preferida': 'expandida',  # intro, 2+ desenvolvimento, conclusão
                'estilo': 'formal_academico',
                'peso_criterios': {
                    'estrutura': 0.20,
                    'argumentacao': 0.25,
                    'gramatica': 0.25,
                    'coesao': 0.20,
                    'adequacao_tema': 0.10
                },
                'caracteristicas': [
                    'norma_culta_rigorosa',
                    'desenvolvimento_extenso',
                    'exemplificacao_abundante',
                    'conectivos_variados',
                    'conclusao_propositiva'
                ]
            },
            'VUNESP': {
                'tipos_redacao': ['dissertativo-argumentativo', 'artigo_opiniao'],
                'extensao_minima': 20,
                'extensao_maxima': 30,
                'estrutura_preferida': 'flexivel',
                'estilo': 'formal_contextualizado',
                'peso_criterios': {
                    'estrutura': 0.20,
                    'argumentacao': 0.30,
                    'gramatica': 0.20,
                    'coesao': 0.15,
                    'adequacao_tema': 0.15
                },
                'caracteristicas': [
                    'contextualizacao_social',
                    'exemplos_atuais',
                    'linguagem_acessivel',
                    'propostas_viaveis',
                    'consciencia_cidada'
                ]
            },
            'FGV': {
                'tipos_redacao': ['dissertativo-argumentativo', 'parecer_tecnico'],
                'extensao_minima': 25,
                'extensao_maxima': 40,
                'estrutura_preferida': 'analitica',
                'estilo': 'formal_analitico',
                'peso_criterios': {
                    'estrutura': 0.15,
                    'argumentacao': 0.35,
                    'gramatica': 0.20,
                    'coesao': 0.15,
                    'adequacao_tema': 0.15
                },
                'caracteristicas': [
                    'analise_profunda',
                    'multiplas_perspectivas',
                    'fundamentacao_teorica',
                    'raciocinio_logico',
                    'sintese_conclusiva'
                ]
            },
            'IBFC': {
                'tipos_redacao': ['dissertativo-argumentativo'],
                'extensao_minima': 20,
                'extensao_maxima': 25,
                'estrutura_preferida': 'simples',
                'estilo': 'formal_direto',
                'peso_criterios': {
                    'estrutura': 0.25,
                    'argumentacao': 0.25,
                    'gramatica': 0.25,
                    'coesao': 0.15,
                    'adequacao_tema': 0.10
                },
                'caracteristicas': [
                    'clareza_objetividade',
                    'argumentos_diretos',
                    'linguagem_simples',
                    'estrutura_clara',
                    'conclusao_objetiva'
                ]
            }
        }

    def _initialize_tema_bank(self) -> Dict:
        """Inicializa banco de temas por banca"""
        return {
            'CESPE': [
                {
                    'tema': 'A efetividade do controle externo na Administração Pública brasileira',
                    'contexto': 'Considerando os mecanismos de controle externo exercidos pelo Tribunal de Contas da União...',
                    'tipo': 'texto_tecnico',
                    'ano': 2023,
                    'cargo': 'Analista de Controle Externo'
                },
                {
                    'tema': 'Inteligência artificial na prestação de serviços públicos',
                    'contexto': 'O uso crescente de tecnologias de IA no setor público...',
                    'tipo': 'dissertativo-argumentativo',
                    'ano': 2023,
                    'cargo': 'Analista Judiciário'
                },
                {
                    'tema': 'Sustentabilidade ambiental e desenvolvimento econômico',
                    'contexto': 'O equilíbrio entre crescimento econômico e preservação ambiental...',
                    'tipo': 'dissertativo-argumentativo',
                    'ano': 2022,
                    'cargo': 'Analista Ambiental'
                }
            ],
            'FCC': [
                {
                    'tema': 'Educação digital e inclusão social no Brasil',
                    'contexto': 'A pandemia acelerou a digitalização da educação...',
                    'tipo': 'dissertativo-argumentativo',
                    'ano': 2023,
                    'cargo': 'Analista Educacional'
                },
                {
                    'tema': 'Gestão de recursos hídricos em tempos de crise',
                    'contexto': 'A escassez hídrica em diversas regiões do país...',
                    'tipo': 'relatorio',
                    'ano': 2022,
                    'cargo': 'Engenheiro Civil'
                }
            ],
            'VUNESP': [
                {
                    'tema': 'Mobilidade urbana sustentável nas grandes cidades',
                    'contexto': 'O crescimento populacional urbano e seus desafios...',
                    'tipo': 'dissertativo-argumentativo',
                    'ano': 2023,
                    'cargo': 'Analista de Planejamento'
                },
                {
                    'tema': 'Saúde mental no trabalho pós-pandemia',
                    'contexto': 'Os impactos da pandemia na saúde mental dos trabalhadores...',
                    'tipo': 'artigo_opiniao',
                    'ano': 2023,
                    'cargo': 'Psicólogo'
                }
            ],
            'FGV': [
                {
                    'tema': 'Compliance e ética na gestão pública',
                    'contexto': 'A importância dos programas de compliance no setor público...',
                    'tipo': 'parecer_tecnico',
                    'ano': 2023,
                    'cargo': 'Auditor'
                }
            ],
            'IBFC': [
                {
                    'tema': 'Tecnologia e modernização do serviço público',
                    'contexto': 'A transformação digital na administração pública...',
                    'tipo': 'dissertativo-argumentativo',
                    'ano': 2023,
                    'cargo': 'Técnico Administrativo'
                }
            ]
        }

    def _initialize_evaluation_criteria(self) -> Dict:
        """Inicializa critérios de avaliação por tipo"""
        return {
            'dissertativo-argumentativo': {
                'criterios': ['estrutura', 'argumentacao', 'gramatica', 'coesao', 'adequacao_tema'],
                'descricoes': {
                    'estrutura': 'Organização em introdução, desenvolvimento e conclusão',
                    'argumentacao': 'Qualidade e consistência dos argumentos apresentados',
                    'gramatica': 'Correção gramatical, ortográfica e pontuação',
                    'coesao': 'Articulação entre ideias e parágrafos',
                    'adequacao_tema': 'Aderência ao tema proposto e compreensão da proposta'
                }
            },
            'texto_tecnico': {
                'criterios': ['estrutura', 'fundamentacao', 'gramatica', 'tecnica', 'adequacao_caso'],
                'descricoes': {
                    'estrutura': 'Organização lógica e sequencial do texto técnico',
                    'fundamentacao': 'Embasamento técnico e jurídico adequado',
                    'gramatica': 'Correção da linguagem técnica e formal',
                    'tecnica': 'Uso apropriado de terminologia técnica',
                    'adequacao_caso': 'Adequação às especificidades do caso apresentado'
                }
            },
            'relatorio': {
                'criterios': ['estrutura', 'analise', 'gramatica', 'objetividade', 'conclusoes'],
                'descricoes': {
                    'estrutura': 'Organização clara em seções e subseções',
                    'analise': 'Qualidade da análise dos dados apresentados',
                    'gramatica': 'Correção linguística e clareza',
                    'objetividade': 'Linguagem objetiva e imparcial',
                    'conclusoes': 'Conclusões fundamentadas e propostas viáveis'
                }
            }
        }

    def evaluate_essay_by_banca(self, essay_text: str, banca: str, tipo_redacao: str = None,
                               tema: str = None) -> Dict:
        """Avalia redação seguindo padrões específicos da banca"""

        # Verificar se a banca é suportada
        if banca not in self.banca_patterns:
            return {"error": f"Banca {banca} não suportada. Bancas disponíveis: {list(self.banca_patterns.keys())}"}

        banca_config = self.banca_patterns[banca]

        # Determinar tipo de redação se não especificado
        if not tipo_redacao:
            tipo_redacao = banca_config['tipos_redacao'][0]  # Usar o primeiro como padrão

        # Verificar se o tipo é suportado pela banca
        if tipo_redacao not in banca_config['tipos_redacao']:
            return {"error": f"Tipo '{tipo_redacao}' não suportado pela banca {banca}"}

        # Obter critérios de avaliação
        criterios = self.evaluation_criteria.get(tipo_redacao, {}).get('criterios', [])
        pesos = banca_config['peso_criterios']

        # Análise preliminar do texto
        analise_preliminar = self._analyze_text_structure(essay_text)

        # Avaliação por critério
        evaluation = {
            "banca": banca,
            "tipo_redacao": tipo_redacao,
            "tema": tema,
            "analise_preliminar": analise_preliminar,
            "scores_por_criterio": {},
            "score_final": 0,
            "feedback_detalhado": {},
            "pontos_fortes": [],
            "pontos_fracos": [],
            "sugestoes_melhoria": [],
            "adequacao_banca": {},
            "timestamp": datetime.now().isoformat()
        }

        # Avaliar cada critério
        total_score = 0
        for criterio in criterios:
            if criterio in pesos:
                score = self._evaluate_criterion_by_banca(essay_text, criterio, banca, analise_preliminar)
                peso = pesos[criterio]
                score_ponderado = score * peso

                evaluation["scores_por_criterio"][criterio] = {
                    "score_bruto": score,
                    "peso": peso,
                    "score_ponderado": score_ponderado
                }

                total_score += score_ponderado

                # Gerar feedback específico
                feedback = self._generate_criterion_feedback(criterio, score, banca, analise_preliminar)
                evaluation["feedback_detalhado"][criterio] = feedback

        evaluation["score_final"] = round(total_score * 10, 1)  # Converter para escala 0-10

        # Análise de adequação à banca
        evaluation["adequacao_banca"] = self._analyze_banca_compliance(essay_text, banca, analise_preliminar)

        # Gerar pontos fortes, fracos e sugestões
        evaluation["pontos_fortes"] = self._identify_strengths_by_banca(evaluation["scores_por_criterio"], banca)
        evaluation["pontos_fracos"] = self._identify_weaknesses_by_banca(evaluation["scores_por_criterio"], banca)
        evaluation["sugestoes_melhoria"] = self._generate_improvement_suggestions_by_banca(evaluation, banca)

        return evaluation

    def _analyze_text_structure(self, text: str) -> Dict:
        """Analisa estrutura básica do texto"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        words = text.split()

        # Análise de conectivos
        conectivos_argumentativos = [
            'portanto', 'assim', 'logo', 'consequentemente', 'por isso',
            'porque', 'visto que', 'uma vez que', 'já que', 'pois',
            'entretanto', 'contudo', 'porém', 'todavia', 'no entanto',
            'ademais', 'além disso', 'outrossim', 'também', 'ainda'
        ]

        conectivos_encontrados = [c for c in conectivos_argumentativos if c in text.lower()]

        # Análise de linguagem formal
        indicadores_formalidade = [
            'destarte', 'outrossim', 'ademais', 'conquanto', 'não obstante',
            'mister', 'cumpre', 'urge', 'impende', 'consoante'
        ]

        formalidade_score = len([i for i in indicadores_formalidade if i in text.lower()])

        return {
            "num_paragrafos": len(paragraphs),
            "num_sentencas": len(sentences),
            "num_palavras": len(words),
            "media_palavras_por_sentenca": len(words) / max(len(sentences), 1),
            "conectivos_encontrados": conectivos_encontrados,
            "num_conectivos": len(conectivos_encontrados),
            "formalidade_score": formalidade_score,
            "tem_introducao": len(paragraphs) > 0,
            "tem_desenvolvimento": len(paragraphs) >= 2,
            "tem_conclusao": len(paragraphs) >= 3,
            "extensao_adequada": 150 <= len(words) <= 400  # Aproximação para linhas
        }

    def _evaluate_criterion_by_banca(self, text: str, criterio: str, banca: str, analise: Dict) -> float:
        """Avalia critério específico considerando padrões da banca"""

        banca_config = self.banca_patterns[banca]
        caracteristicas = banca_config['caracteristicas']

        if criterio == 'estrutura':
            return self._evaluate_structure_by_banca(text, banca, analise)
        elif criterio == 'argumentacao':
            return self._evaluate_argumentation_by_banca(text, banca, analise)
        elif criterio == 'gramatica':
            return self._evaluate_grammar_by_banca(text, banca, analise)
        elif criterio == 'coesao':
            return self._evaluate_cohesion_by_banca(text, banca, analise)
        elif criterio == 'adequacao_tema':
            return self._evaluate_theme_adherence_by_banca(text, banca, analise)
        elif criterio == 'fundamentacao':
            return self._evaluate_technical_foundation(text, banca, analise)
        elif criterio == 'tecnica':
            return self._evaluate_technical_language(text, banca, analise)
        elif criterio == 'objetividade':
            return self._evaluate_objectivity(text, banca, analise)
        else:
            return 0.7  # Score padrão para critérios não implementados

    def _evaluate_structure_by_banca(self, text: str, banca: str, analise: Dict) -> float:
        """Avalia estrutura considerando preferências da banca"""

        banca_config = self.banca_patterns[banca]
        estrutura_preferida = banca_config['estrutura_preferida']

        score = 0.5  # Base

        # Verificar número de parágrafos
        num_paragrafos = analise['num_paragrafos']

        if estrutura_preferida == 'classica':
            # CESPE prefere estrutura clássica (3-4 parágrafos)
            if 3 <= num_paragrafos <= 4:
                score += 0.3
            elif num_paragrafos == 5:
                score += 0.2
            else:
                score += 0.1

        elif estrutura_preferida == 'expandida':
            # FCC prefere desenvolvimento mais extenso (4-5 parágrafos)
            if 4 <= num_paragrafos <= 5:
                score += 0.3
            elif num_paragrafos == 6:
                score += 0.2
            else:
                score += 0.1

        elif estrutura_preferida == 'flexivel':
            # VUNESP aceita estruturas mais flexíveis
            if num_paragrafos >= 3:
                score += 0.3
            else:
                score += 0.1

        # Verificar presença de introdução, desenvolvimento e conclusão
        if analise['tem_introducao'] and analise['tem_desenvolvimento'] and analise['tem_conclusao']:
            score += 0.2

        return min(1.0, score)

    def _evaluate_argumentation_by_banca(self, text: str, banca: str, analise: Dict) -> float:
        """Avalia argumentação considerando estilo da banca"""

        banca_config = self.banca_patterns[banca]
        caracteristicas = banca_config['caracteristicas']

        score = 0.4  # Base

        # Verificar conectivos argumentativos
        num_conectivos = analise['num_conectivos']
        if num_conectivos >= 5:
            score += 0.2
        elif num_conectivos >= 3:
            score += 0.15
        else:
            score += 0.05

        # Características específicas por banca
        if 'argumentacao_solida' in caracteristicas:
            # CESPE valoriza argumentação técnica sólida
            termos_tecnicos = ['legislação', 'jurisprudência', 'doutrina', 'princípio', 'norma']
            count_tecnicos = sum(1 for termo in termos_tecnicos if termo in text.lower())
            score += min(0.2, count_tecnicos * 0.05)

        elif 'desenvolvimento_extenso' in caracteristicas:
            # FCC valoriza desenvolvimento extenso com exemplos
            if analise['media_palavras_por_sentenca'] > 15:
                score += 0.15
            exemplos = text.lower().count('exemplo') + text.lower().count('por exemplo')
            score += min(0.1, exemplos * 0.05)

        elif 'multiplas_perspectivas' in caracteristicas:
            # FGV valoriza análise de múltiplas perspectivas
            perspectivas = ['por outro lado', 'entretanto', 'contudo', 'no entanto']
            count_perspectivas = sum(1 for p in perspectivas if p in text.lower())
            score += min(0.2, count_perspectivas * 0.1)

        return min(1.0, score)

    def _evaluate_grammar_by_banca(self, text: str, banca: str, analise: Dict) -> float:
        """Avalia gramática considerando rigor da banca"""

        score = 0.6  # Base

        # Verificar indicadores de formalidade
        formalidade_score = analise['formalidade_score']
        score += min(0.2, formalidade_score * 0.05)

        # Verificar estrutura das sentenças
        media_palavras = analise['media_palavras_por_sentenca']
        if 12 <= media_palavras <= 20:  # Sentenças bem estruturadas
            score += 0.15
        elif media_palavras > 25:  # Sentenças muito longas
            score -= 0.1

        # Penalizar erros comuns (simulação)
        erros_comuns = ['mim fazer', 'para eu', 'entre eu', 'há anos atrás']
        for erro in erros_comuns:
            if erro in text.lower():
                score -= 0.1

        return max(0.0, min(1.0, score))

    def _evaluate_cohesion_by_banca(self, text: str, banca: str, analise: Dict) -> float:
        """Avalia coesão considerando padrões da banca"""

        score = 0.5  # Base

        # Verificar uso de conectivos
        num_conectivos = analise['num_conectivos']
        num_paragrafos = analise['num_paragrafos']

        if num_paragrafos > 1:
            conectivos_por_paragrafo = num_conectivos / num_paragrafos
            if conectivos_por_paragrafo >= 2:
                score += 0.3
            elif conectivos_por_paragrafo >= 1:
                score += 0.2
            else:
                score += 0.1

        # Verificar repetições excessivas
        palavras = text.lower().split()
        palavras_unicas = set(palavras)
        diversidade_lexical = len(palavras_unicas) / len(palavras) if palavras else 0

        if diversidade_lexical > 0.6:
            score += 0.2
        elif diversidade_lexical > 0.4:
            score += 0.1

        return min(1.0, score)

    def _evaluate_theme_adherence_by_banca(self, text: str, banca: str, analise: Dict) -> float:
        """Avalia adequação ao tema"""

        # Simulação básica - em implementação real usaria NLP
        score = 0.7  # Base assumindo adequação razoável

        # Verificar se o texto tem desenvolvimento suficiente
        if analise['num_palavras'] < 100:
            score -= 0.3
        elif analise['num_palavras'] > 500:
            score -= 0.1

        # Verificar estrutura mínima
        if analise['tem_introducao'] and analise['tem_desenvolvimento'] and analise['tem_conclusao']:
            score += 0.2

        return min(1.0, score)

    def _evaluate_technical_foundation(self, text: str, banca: str, analise: Dict) -> float:
        """Avalia fundamentação técnica"""

        score = 0.5  # Base

        # Verificar termos técnicos
        termos_tecnicos = [
            'legislação', 'jurisprudência', 'doutrina', 'princípio', 'norma',
            'regulamento', 'decreto', 'portaria', 'resolução', 'instrução'
        ]

        count_tecnicos = sum(1 for termo in termos_tecnicos if termo in text.lower())
        score += min(0.3, count_tecnicos * 0.05)

        # Verificar citações ou referências
        if 'art.' in text.lower() or 'artigo' in text.lower():
            score += 0.1

        if 'lei' in text.lower():
            score += 0.1

        return min(1.0, score)

    def _evaluate_technical_language(self, text: str, banca: str, analise: Dict) -> float:
        """Avalia uso de linguagem técnica"""

        score = 0.6  # Base

        # Verificar formalidade
        score += min(0.2, analise['formalidade_score'] * 0.04)

        # Verificar impessoalidade
        pronomes_pessoais = ['eu', 'meu', 'minha', 'nosso', 'nossa']
        count_pessoais = sum(1 for p in pronomes_pessoais if p in text.lower().split())

        if count_pessoais == 0:
            score += 0.2
        elif count_pessoais <= 2:
            score += 0.1
        else:
            score -= 0.1

        return max(0.0, min(1.0, score))

    def _evaluate_objectivity(self, text: str, banca: str, analise: Dict) -> float:
        """Avalia objetividade"""

        score = 0.6  # Base

        # Verificar concisão
        if analise['media_palavras_por_sentenca'] <= 18:
            score += 0.2
        elif analise['media_palavras_por_sentenca'] > 25:
            score -= 0.1

        # Verificar ausência de subjetividade excessiva
        termos_subjetivos = ['acredito', 'penso', 'acho', 'sinto', 'creio']
        count_subjetivos = sum(1 for t in termos_subjetivos if t in text.lower())

        if count_subjetivos == 0:
            score += 0.2
        else:
            score -= count_subjetivos * 0.05

        return max(0.0, min(1.0, score))

    def _generate_criterion_feedback(self, criterio: str, score: float, banca: str, analise: Dict) -> str:
        """Gera feedback específico para cada critério"""

        if score >= 0.8:
            nivel = "Excelente"
        elif score >= 0.6:
            nivel = "Bom"
        elif score >= 0.4:
            nivel = "Regular"
        else:
            nivel = "Precisa melhorar"

        feedbacks = {
            'estrutura': f"{nivel} organização textual. " +
                        ("Estrutura bem definida com introdução, desenvolvimento e conclusão." if score >= 0.6
                         else "Trabalhe na organização em parágrafos bem definidos."),

            'argumentacao': f"{nivel} desenvolvimento argumentativo. " +
                           ("Argumentos consistentes e bem fundamentados." if score >= 0.6
                            else "Desenvolva melhor os argumentos com exemplos e fundamentação."),

            'gramatica': f"{nivel} domínio da norma culta. " +
                        ("Linguagem formal adequada." if score >= 0.6
                         else "Revise aspectos gramaticais e use linguagem mais formal."),

            'coesao': f"{nivel} articulação entre ideias. " +
                     ("Bom uso de conectivos e progressão textual." if score >= 0.6
                      else "Use mais conectivos para articular melhor as ideias."),

            'adequacao_tema': f"{nivel} aderência ao tema. " +
                             ("Texto bem focado no tema proposto." if score >= 0.6
                              else "Mantenha maior foco no tema central.")
        }

        return feedbacks.get(criterio, f"{nivel} desempenho neste critério.")

    def _analyze_banca_compliance(self, text: str, banca: str, analise: Dict) -> Dict:
        """Analisa adequação aos padrões específicos da banca"""

        banca_config = self.banca_patterns[banca]
        compliance = {}

        # Verificar extensão
        num_palavras = analise['num_palavras']
        extensao_min = banca_config['extensao_minima'] * 8  # Aproximação: 8 palavras por linha
        extensao_max = banca_config['extensao_maxima'] * 8

        if extensao_min <= num_palavras <= extensao_max:
            compliance['extensao'] = {
                'status': 'adequado',
                'comentario': f'Extensão adequada ({num_palavras} palavras)'
            }
        else:
            compliance['extensao'] = {
                'status': 'inadequado',
                'comentario': f'Extensão fora do padrão. Recomendado: {extensao_min}-{extensao_max} palavras'
            }

        # Verificar estrutura
        estrutura_ok = analise['tem_introducao'] and analise['tem_desenvolvimento'] and analise['tem_conclusao']
        compliance['estrutura'] = {
            'status': 'adequado' if estrutura_ok else 'inadequado',
            'comentario': 'Estrutura bem definida' if estrutura_ok else 'Defina melhor introdução, desenvolvimento e conclusão'
        }

        # Verificar formalidade
        formalidade_adequada = analise['formalidade_score'] >= 2
        compliance['formalidade'] = {
            'status': 'adequado' if formalidade_adequada else 'inadequado',
            'comentario': 'Linguagem formal adequada' if formalidade_adequada else 'Use linguagem mais formal'
        }

        return compliance

    def _identify_strengths_by_banca(self, scores: Dict, banca: str) -> List[str]:
        """Identifica pontos fortes baseados nos scores"""

        strengths = []

        for criterio, data in scores.items():
            if data['score_bruto'] >= 0.8:
                criterio_nome = criterio.replace('_', ' ').title()
                strengths.append(f"Excelente {criterio_nome}")

        return strengths

    def _identify_weaknesses_by_banca(self, scores: Dict, banca: str) -> List[str]:
        """Identifica pontos fracos baseados nos scores"""

        weaknesses = []

        for criterio, data in scores.items():
            if data['score_bruto'] < 0.6:
                criterio_nome = criterio.replace('_', ' ').title()
                weaknesses.append(f"{criterio_nome} precisa de atenção")

        return weaknesses

    def _generate_improvement_suggestions_by_banca(self, evaluation: Dict, banca: str) -> List[str]:
        """Gera sugestões específicas de melhoria"""

        suggestions = []
        banca_config = self.banca_patterns[banca]
        scores = evaluation['scores_por_criterio']

        # Sugestões baseadas em pontos fracos
        for criterio, data in scores.items():
            if data['score_bruto'] < 0.6:
                if criterio == 'estrutura':
                    suggestions.append("Organize melhor o texto em parágrafos bem definidos")
                elif criterio == 'argumentacao':
                    suggestions.append("Desenvolva argumentos com mais exemplos e fundamentação")
                elif criterio == 'gramatica':
                    suggestions.append("Revise aspectos gramaticais e use linguagem mais formal")
                elif criterio == 'coesao':
                    suggestions.append("Use mais conectivos para articular as ideias")

        # Sugestões específicas da banca
        caracteristicas = banca_config['caracteristicas']

        if 'argumentacao_solida' in caracteristicas:
            suggestions.append("Para CESPE: Use fundamentação técnica e jurídica")

        if 'desenvolvimento_extenso' in caracteristicas:
            suggestions.append("Para FCC: Desenvolva argumentos mais extensamente")

        if 'contextualizacao_social' in caracteristicas:
            suggestions.append("Para VUNESP: Contextualize socialmente o tema")

        return suggestions[:5]  # Limitar a 5 sugestões

    def get_tema_by_banca(self, banca: str, tipo: str = None) -> Dict:
        """Retorna tema aleatório da banca especificada"""

        if banca not in self.tema_bank:
            return {"error": f"Banca {banca} não encontrada"}

        temas = self.tema_bank[banca]

        if tipo:
            temas_filtrados = [t for t in temas if t['tipo'] == tipo]
            if temas_filtrados:
                temas = temas_filtrados

        if not temas:
            return {"error": "Nenhum tema encontrado"}

        import random
        return random.choice(temas)

    def generate_example_essay(self, banca: str, tema: str, num_linhas: int = 25) -> Dict:
        """Gera uma redação de exemplo personalizada baseada no tema e banca especificados."""
        if banca not in self.banca_patterns:
            return {"error": f"Banca {banca} não suportada para geração de exemplo."}

        # Se não foi fornecido tema, usar um tema padrão
        if not tema or tema.strip() == "":
            tema = "A importância da educação no século XXI"

        banca_config = self.banca_patterns[banca]

        # Gerar redação personalizada usando IA
        try:
            # Prompt personalizado baseado na banca e tema
            prompt = f"""
            Escreva uma redação dissertativo-argumentativa sobre o tema: "{tema}"

            Características da banca {banca}:
            - Estrutura: {banca_config['estrutura_preferida']}
            - Estilo: {banca_config['estilo']}
            - Extensão: {banca_config['extensao_minima']}-{banca_config['extensao_maxima']} linhas
            - Características valorizadas: {', '.join(banca_config['caracteristicas'])}

            A redação deve ter aproximadamente {num_linhas} linhas e seguir a estrutura:
            1. Introdução com contextualização e tese
            2. Desenvolvimento 1 com argumentos e exemplos
            3. Desenvolvimento 2 com contrapontos ou aprofundamento
            4. Conclusão com síntese e proposta

            Seja específico ao tema, use linguagem formal e argumentação consistente.
            Não use frases genéricas ou placeholders.
            """

            # Gerar conteúdo personalizado baseado no tema
            redacao_personalizada = self._generate_personalized_content(tema, banca, num_linhas)

            return {
                "example_essay": redacao_personalizada,
                "banca": banca,
                "tema": tema,
                "num_linhas": num_linhas
            }

        except Exception as e:
            # Fallback para redação básica se houver erro
            return self._generate_fallback_essay(tema, banca)

    def _generate_personalized_content(self, tema: str, banca: str, num_linhas: int) -> str:
        """Gera conteúdo personalizado baseado no tema"""

        # Analisar o tema para gerar conteúdo relevante
        tema_lower = tema.lower()

        # Templates baseados em categorias de temas
        if any(palavra in tema_lower for palavra in ['educação', 'ensino', 'escola', 'professor']):
            return self._generate_education_essay(tema, banca)
        elif any(palavra in tema_lower for palavra in ['segurança', 'violência', 'crime', 'polícia']):
            return self._generate_security_essay(tema, banca)
        elif any(palavra in tema_lower for palavra in ['meio ambiente', 'sustentabilidade', 'ecologia', 'natureza']):
            return self._generate_environment_essay(tema, banca)
        elif any(palavra in tema_lower for palavra in ['tecnologia', 'digital', 'internet', 'inovação']):
            return self._generate_technology_essay(tema, banca)
        elif any(palavra in tema_lower for palavra in ['saúde', 'medicina', 'hospital', 'sus']):
            return self._generate_health_essay(tema, banca)
        else:
            return self._generate_generic_essay(tema, banca)

    def _generate_education_essay(self, tema: str, banca: str) -> str:
        """Gera redação sobre educação com variações por banca"""

        # Variações por banca
        if banca == "CESPE":
            intro = f"A questão da {tema.lower()} representa um dos maiores desafios contemporâneos da sociedade brasileira. No contexto atual, é fundamental compreender as múltiplas dimensões desse tema e suas implicações para o desenvolvimento nacional."

            dev1 = f"Primeiramente, cabe destacar que {tema.lower()} possui impacto direto na formação cidadã e no progresso social. As políticas públicas voltadas para essa área demonstram resultados significativos quando implementadas de forma consistente e com recursos adequados."

        elif banca == "FCC":
            intro = f"O tema {tema.lower()} constitui uma das principais preocupações da agenda pública brasileira. A análise dessa questão revela a necessidade de abordagens inovadoras e investimentos estratégicos para garantir resultados efetivos."

            dev1 = f"Inicialmente, é necessário reconhecer que {tema.lower()} influencia diretamente a qualidade de vida dos cidadãos e o desenvolvimento socioeconômico. A experiência internacional demonstra que países que priorizam essa área obtêm melhores indicadores de progresso humano."

        elif banca == "VUNESP":
            intro = f"A temática relacionada a {tema.lower()} assume relevância crescente no debate público contemporâneo. A complexidade dos desafios envolvidos exige reflexão aprofundada sobre as estratégias mais adequadas para enfrentá-los."

            dev1 = f"Em primeira análise, observa-se que {tema.lower()} está intrinsecamente relacionada ao exercício da cidadania e à construção de uma sociedade mais justa. Os dados estatísticos evidenciam a correlação positiva entre investimentos nessa área e melhoria dos indicadores sociais."

        else:  # FGV, IBFC e outras
            intro = f"A discussão sobre {tema.lower()} ocupa posição central no cenário nacional, demandando análise criteriosa de suas múltiplas facetas. O entendimento dessa questão é essencial para a formulação de políticas públicas eficazes."

            dev1 = f"Sob uma perspectiva inicial, verifica-se que {tema.lower()} exerce influência determinante na formação social e no desenvolvimento humano. As evidências empíricas corroboram a importância de investimentos sustentados e bem direcionados nessa área."

        # Desenvolvimento 2 e conclusão comuns com pequenas variações
        dev2 = f"Por outro lado, os desafios relacionados a {tema.lower()} exigem uma abordagem multidisciplinar e o envolvimento de diversos setores da sociedade. A superação das dificuldades atuais demanda investimento em infraestrutura, capacitação profissional e inovação metodológica."

        if banca in ["CESPE", "FCC"]:
            conc = f"Portanto, {tema.lower()} deve ser tratada como prioridade nacional, com políticas integradas que promovam a equidade e a qualidade. Somente através do comprometimento coletivo será possível construir um futuro mais justo e próspero para todos os brasileiros."
        else:
            conc = f"Em síntese, {tema.lower()} requer atenção prioritária do poder público e da sociedade civil organizada. A implementação de medidas coordenadas e sustentáveis é fundamental para alcançar os objetivos de desenvolvimento social e humano almejados pela nação."

        return "\n\n".join([intro, dev1, dev2, conc])

    def _generate_security_essay(self, tema: str, banca: str) -> str:
        """Gera redação sobre segurança pública"""
        intro = f"A problemática da {tema.lower()} constitui uma das principais preocupações da sociedade brasileira contemporânea. A complexidade desse fenômeno exige análise criteriosa de suas causas estruturais e das possíveis soluções integradas."

        dev1 = f"Inicialmente, cabe ressaltar que {tema.lower()} está intrinsecamente relacionada a fatores socioeconômicos como desigualdade, desemprego e falta de oportunidades. A prevenção eficaz requer investimentos em educação, geração de emprego e programas sociais inclusivos."

        dev2 = f"Ademais, o enfrentamento da {tema.lower()} demanda o fortalecimento das instituições de segurança pública e do sistema de justiça. A modernização dos equipamentos, a capacitação dos profissionais e a integração entre os órgãos são medidas essenciais para a efetividade das ações."

        conc = f"Em síntese, a solução para {tema.lower()} passa pela implementação de políticas públicas integradas que abordem tanto os aspectos preventivos quanto repressivos. O Estado, em parceria com a sociedade civil, deve promover ações coordenadas para garantir a segurança e o bem-estar de todos os cidadãos."

        return "\n\n".join([intro, dev1, dev2, conc])

    def _generate_environment_essay(self, tema: str, banca: str) -> str:
        """Gera redação sobre meio ambiente"""
        intro = f"A questão ambiental relacionada a {tema.lower()} representa um dos maiores desafios do século XXI. A urgência dessa temática exige reflexão profunda sobre os modelos de desenvolvimento e as práticas sustentáveis necessárias para preservar o planeta para as futuras gerações."

        dev1 = f"Primeiramente, é fundamental reconhecer que {tema.lower()} impacta diretamente a qualidade de vida das populações e a biodiversidade dos ecossistemas. As evidências científicas demonstram a necessidade de mudanças imediatas nos padrões de consumo e produção."

        dev2 = f"Além disso, o enfrentamento dos problemas relacionados a {tema.lower()} requer cooperação internacional e políticas públicas efetivas. A transição para uma economia verde, o investimento em energias renováveis e a educação ambiental são estratégias fundamentais para a sustentabilidade."

        conc = f"Conclui-se que {tema.lower()} demanda ação urgente e coordenada de governos, empresas e sociedade civil. A preservação ambiental não é apenas uma responsabilidade ética, mas uma necessidade vital para garantir a continuidade da vida no planeta."

        return "\n\n".join([intro, dev1, dev2, conc])

    def _generate_technology_essay(self, tema: str, banca: str) -> str:
        """Gera redação sobre tecnologia"""
        intro = f"A revolução tecnológica relacionada a {tema.lower()} tem transformado profundamente as relações sociais, econômicas e culturais na sociedade contemporânea. Compreender os impactos dessa transformação é essencial para navegar os desafios e oportunidades do mundo digital."

        dev1 = f"Por um lado, {tema.lower()} oferece possibilidades inéditas de conectividade, acesso à informação e inovação. As ferramentas digitais democratizam o conhecimento, facilitam a comunicação global e criam novas oportunidades de trabalho e empreendedorismo."

        dev2 = f"Contudo, a expansão da {tema.lower()} também apresenta desafios significativos, como a exclusão digital, questões de privacidade e segurança de dados. A necessidade de regulamentação adequada e educação digital torna-se cada vez mais urgente para garantir o uso ético e responsável da tecnologia."

        conc = f"Portanto, {tema.lower()} deve ser encarada como uma ferramenta de transformação social positiva, desde que acompanhada de políticas públicas inclusivas e educação para a cidadania digital. O futuro depende da capacidade de aproveitar os benefícios tecnológicos minimizando seus riscos."

        return "\n\n".join([intro, dev1, dev2, conc])

    def _generate_health_essay(self, tema: str, banca: str) -> str:
        """Gera redação sobre saúde"""
        intro = f"A questão da {tema.lower()} constitui um direito fundamental garantido pela Constituição Federal e um pilar essencial para o desenvolvimento humano. No contexto brasileiro, os desafios do sistema de saúde exigem análise criteriosa e propostas efetivas de melhoria."

        dev1 = f"Em primeiro lugar, é importante destacar que {tema.lower()} está diretamente relacionada à qualidade de vida da população e ao desenvolvimento socioeconômico do país. O Sistema Único de Saúde (SUS), apesar de suas limitações, representa uma conquista democrática que deve ser fortalecida e aprimorada."

        dev2 = f"Entretanto, os desafios relacionados a {tema.lower()} incluem subfinanciamento, desigualdades regionais e falta de profissionais especializados. A superação dessas dificuldades requer investimento em infraestrutura, formação profissional e políticas de prevenção e promoção da saúde."

        conc = f"Em conclusão, {tema.lower()} deve ser tratada como prioridade nacional, com políticas integradas que garantam acesso universal e equitativo aos serviços de saúde. Somente através do comprometimento do Estado e da sociedade será possível construir um sistema de saúde eficiente e humanizado."

        return "\n\n".join([intro, dev1, dev2, conc])

    def _generate_generic_essay(self, tema: str, banca: str) -> str:
        """Gera redação genérica para temas diversos"""
        intro = f"A temática relacionada a {tema.lower()} representa uma questão relevante na sociedade contemporânea. A complexidade desse assunto exige análise cuidadosa de seus múltiplos aspectos e das possíveis soluções para os desafios apresentados."

        dev1 = f"Inicialmente, é fundamental compreender que {tema.lower()} possui implicações significativas para o desenvolvimento social e econômico. Os dados disponíveis demonstram a necessidade de abordagens inovadoras e políticas públicas efetivas para lidar com essa questão."

        dev2 = f"Além disso, o enfrentamento dos problemas relacionados a {tema.lower()} requer a participação ativa de diversos setores da sociedade. A cooperação entre governo, iniciativa privada e organizações civis é essencial para a implementação de soluções sustentáveis e duradouras."

        conc = f"Portanto, {tema.lower()} demanda atenção prioritária e ações coordenadas que considerem tanto os aspectos imediatos quanto as consequências de longo prazo. O sucesso das intervenções depende do comprometimento coletivo e da adoção de estratégias baseadas em evidências científicas."

        return "\n\n".join([intro, dev1, dev2, conc])

    def _generate_fallback_essay(self, tema: str, banca: str) -> Dict:
        """Gera redação básica em caso de erro"""
        redacao_basica = f"""A questão de {tema} representa um desafio importante na sociedade contemporânea.

É fundamental analisar os diversos aspectos relacionados a este tema, considerando suas implicações sociais, econômicas e culturais.

Por outro lado, é necessário buscar soluções efetivas que possam contribuir para o desenvolvimento e bem-estar da população.

Em conclusão, {tema} requer atenção e ações coordenadas de todos os setores da sociedade."""

        return {
            "example_essay": redacao_basica,
            "banca": banca,
            "tema": tema,
            "error": "Redação gerada em modo básico devido a limitações técnicas"
        }

    def _run(self, action: str, params_json: str = None) -> str:
        """Interface principal da ferramenta"""
        try:
            if params_json:
                params = json.loads(params_json)
            else:
                params = {}

            if action == "evaluate_essay":
                essay_text = params.get('essay_text', '')
                banca = params.get('banca', 'CESPE')
                tipo_redacao = params.get('tipo_redacao')
                tema = params.get('tema')

                result = self.evaluate_essay_by_banca(essay_text, banca, tipo_redacao, tema)

            elif action == "get_tema":
                banca = params.get('banca', 'CESPE')
                tipo = params.get('tipo')

                result = self.get_tema_by_banca(banca, tipo)

            elif action == "get_banca_info":
                banca = params.get('banca', 'CESPE')

                if banca in self.banca_patterns:
                    result = self.banca_patterns[banca]
                else:
                    result = {"error": f"Banca {banca} não encontrada"}

            elif action == "generate_example_essay":
                banca = params.get('banca', 'CESPE')
                tema = params.get('tema', 'A importância da educação no século XXI')
                num_linhas = params.get('num_linhas', 25) # Novo parâmetro
                result = self.generate_example_essay(banca, tema, num_linhas)

            else:
                result = {"error": "Ação não reconhecida. Use 'evaluate_essay', 'get_tema', 'get_banca_info' ou 'generate_example_essay'."}

            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            return json.dumps({
                'error': f'Erro na ferramenta de redação: {str(e)}'
            }, indent=2, ensure_ascii=False)
