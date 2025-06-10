import json
import re
from typing import Dict, List, Tuple
from datetime import datetime
import os

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

            else:
                result = {"error": "Ação não reconhecida. Use 'evaluate_essay', 'get_tema' ou 'get_banca_info'."}

            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            return json.dumps({
                'error': f'Erro na ferramenta de redação: {str(e)}'
            }, indent=2, ensure_ascii=False)
        """Avalia uma redação com base em critérios específicos"""
        if not criteria:
            criteria = ["Estrutura", "Argumentação", "Gramática", "Coesão", "Adequação ao tema"]
        
        evaluation = {
            "score": 0,
            "feedback": {},
            "suggestions": [],
            "strengths": [],
            "weaknesses": []
        }
        
        # Avaliação por critério
        for criterion in criteria:
            # Simulação de avaliação - em produção usaria análise mais sofisticada
            if criterion == "Estrutura":
                score = self._evaluate_structure(essay_text)
                feedback = self._generate_structure_feedback(score, essay_text)
            elif criterion == "Argumentação":
                score = self._evaluate_argumentation(essay_text)
                feedback = self._generate_argumentation_feedback(score, essay_text)
            elif criterion == "Gramática":
                score = self._evaluate_grammar(essay_text)
                feedback = self._generate_grammar_feedback(score, essay_text)
            elif criterion == "Coesão":
                score = self._evaluate_cohesion(essay_text)
                feedback = self._generate_cohesion_feedback(score, essay_text)
            elif criterion == "Adequação ao tema":
                score = self._evaluate_theme_adherence(essay_text)
                feedback = self._generate_theme_feedback(score, essay_text)
            else:
                score = 7.0  # Valor padrão
                feedback = "Critério não implementado para avaliação detalhada."
            
            evaluation["feedback"][criterion] = {
                "score": score,
                "comments": feedback
            }
            evaluation["score"] += score
        
        # Calcular média
        evaluation["score"] = round(evaluation["score"] / len(criteria), 1)
        
        # Gerar sugestões, pontos fortes e fracos
        evaluation["suggestions"] = self._generate_suggestions(evaluation["feedback"])
        evaluation["strengths"] = self._identify_strengths(evaluation["feedback"])
        evaluation["weaknesses"] = self._identify_weaknesses(evaluation["feedback"])
        
        return evaluation
    
    def _evaluate_structure(self, text: str) -> float:
        """Avalia a estrutura da redação"""
        # Implementação simplificada
        paragraphs = text.split("\n\n")
        if len(paragraphs) >= 4:  # Introdução, 2+ desenvolvimento, conclusão
            return 8.5
        elif len(paragraphs) == 3:  # Estrutura básica
            return 7.0
        else:
            return 5.0
    
    def _evaluate_argumentation(self, text: str) -> float:
        """Avalia a qualidade da argumentação"""
        # Implementação simplificada
        argument_markers = ["porque", "portanto", "assim", "logo", "dessa forma", 
                           "visto que", "uma vez que", "considerando"]
        count = sum(1 for marker in argument_markers if marker in text.lower())
        if count >= 5:
            return 8.0
        elif count >= 3:
            return 7.0
        else:
            return 6.0
    
    def _evaluate_grammar(self, text: str) -> float:
        """Avalia aspectos gramaticais"""
        # Implementação simplificada
        return 7.5  # Valor padrão
    
    def _evaluate_cohesion(self, text: str) -> float:
        """Avalia coesão textual"""
        # Implementação simplificada
        cohesion_markers = ["entretanto", "contudo", "porém", "todavia", "no entanto",
                           "ademais", "além disso", "outrossim", "por fim", "finalmente"]
        count = sum(1 for marker in cohesion_markers if marker in text.lower())
        if count >= 6:
            return 9.0
        elif count >= 3:
            return 7.5
        else:
            return 6.0
    
    def _evaluate_theme_adherence(self, text: str) -> float:
        """Avalia aderência ao tema"""
        # Implementação simplificada
        return 8.0  # Valor padrão
    
    def _generate_structure_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre estrutura"""
        if score >= 8.0:
            return "Excelente estruturação com introdução clara, desenvolvimento bem organizado e conclusão coesa."
        elif score >= 7.0:
            return "Boa estrutura, mas pode melhorar a organização dos parágrafos e a transição entre ideias."
        else:
            return "Estrutura precisa ser aprimorada. Certifique-se de incluir introdução, desenvolvimento e conclusão bem definidos."
    
    def _generate_argumentation_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre argumentação"""
        if score >= 8.0:
            return "Argumentação sólida com uso eficaz de exemplos e evidências."
        elif score >= 7.0:
            return "Argumentos razoáveis, mas podem ser fortalecidos com mais exemplos concretos."
        else:
            return "Argumentação fraca. Desenvolva melhor suas ideias e utilize exemplos para sustentá-las."
    
    def _generate_grammar_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre gramática"""
        if score >= 8.0:
            return "Excelente domínio das regras gramaticais e ortográficas."
        elif score >= 7.0:
            return "Bom domínio gramatical com poucos erros que não comprometem a compreensão."
        else:
            return "Diversos erros gramaticais e ortográficos que prejudicam a qualidade do texto."
    
    def _generate_cohesion_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre coesão"""
        if score >= 8.0:
            return "Excelente uso de conectivos e elementos de coesão textual."
        elif score >= 7.0:
            return "Boa coesão, mas pode melhorar a transição entre parágrafos."
        else:
            return "Problemas de coesão textual. Utilize mais conectivos para ligar suas ideias."
    
    def _generate_theme_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre aderência ao tema"""
        if score >= 8.0:
            return "Excelente aderência ao tema proposto, com abordagem completa e relevante."
        elif score >= 7.0:
            return "Boa aderência ao tema, mas alguns aspectos importantes não foram abordados."
        else:
            return "Tangenciamento do tema. Procure abordar o tema de forma mais direta e completa."
    
    def _generate_suggestions(self, feedback: Dict) -> List[str]:
        """Gera sugestões de melhoria"""
        suggestions = []
        for criterion, data in feedback.items():
            if data["score"] < 7.0:
                if criterion == "Estrutura":
                    suggestions.append("Organize seu texto em pelo menos 4 parágrafos: introdução, 2 de desenvolvimento e conclusão.")
                elif criterion == "Argumentação":
                    suggestions.append("Utilize mais conectivos argumentativos e exemplos concretos para fortalecer suas ideias.")
                elif criterion == "Gramática":
                    suggestions.append("Revise cuidadosamente a ortografia e pontuação do texto.")
                elif criterion == "Coesão":
                    suggestions.append("Utilize mais elementos de transição entre parágrafos e ideias.")
                elif criterion == "Adequação ao tema":
                    suggestions.append("Mantenha o foco no tema proposto, evitando digressões.")
        return suggestions
    
    def _identify_strengths(self, feedback: Dict) -> List[str]:
        """Identifica pontos fortes"""
        strengths = []
        for criterion, data in feedback.items():
            if data["score"] >= 8.0:
                strengths.append(f"Excelente {criterion.lower()}")
        return strengths
    
    def _identify_weaknesses(self, feedback: Dict) -> List[str]:
        """Identifica pontos fracos"""
        weaknesses = []
        for criterion, data in feedback.items():
            if data["score"] < 7.0:
                weaknesses.append(f"Fraco desempenho em {criterion.lower()}")
        return weaknesses
    
    def _run(self, essay_text: str, essay_type: str = "Dissertativo-Argumentativo") -> str:
        """Interface principal da ferramenta"""
        try:
            # Definir critérios com base no tipo de redação
            if essay_type == "Dissertativo-Argumentativo":
                criteria = ["Estrutura", "Argumentação", "Gramática", "Coesão", "Adequação ao tema"]
            elif essay_type == "Peça Processual":
                criteria = ["Estrutura", "Fundamentação", "Gramática", "Técnica", "Adequação ao caso"]
            else:
                criteria = ["Estrutura", "Conteúdo", "Gramática", "Coesão", "Adequação"]
            
            # Avaliar redação
            evaluation = self.evaluate_essay(essay_text, essay_type, criteria)
            
            return json.dumps(evaluation, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'error': f'Erro ao avaliar redação: {str(e)}',
                'essay_type': essay_type
            }, indent=2, ensure_ascii=False)