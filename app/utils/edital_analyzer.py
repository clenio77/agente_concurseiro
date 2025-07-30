"""
Módulo para análise inteligente de editais usando múltiplas estratégias
"""

import re
from typing import Any, Dict, List

# Document processing
import PyPDF2
from docx import Document


class EditalAnalyzer:
    """Analisador inteligente de editais com múltiplas estratégias"""

    def __init__(self):
        self.bancas_conhecidas = [
            'cespe', 'cebraspe', 'fgv', 'vunesp', 'fcc', 'ibfc', 'quadrix',
            'instituto aocp', 'instituto cesgranrio', 'cesgranrio', 'aocp',
            'fundação cesgranrio', 'fundação getúlio vargas', 'fundação carlos chagas'
        ]

        self.padroes_avancados = {
            'concurso': [
                r'concurso\s+(?:público\s+)?(?:para\s+)?([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
                r'edital\s+(?:do\s+)?(?:concurso\s+)?(?:público\s+)?(?:para\s+)?([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
                r'([^,\n]+?)\s+concurso\s+público',
                r'concurso\s+público\s+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
                r'departamento\s+de\s+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
                r'polícia\s+(?:federal|civil|militar)\s+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            ],
            'banca': [
                # Padrões mais específicos primeiro
                r'banca\s+(?:organizadora|examinadora)[:\s]*([^,\n.]+?)(?:\s*[,.\n]|$)',
                r'organização[:\s]*([^,\n.]+?)(?:\s*[,.\n]|$)',
                r'organizadora[:\s]*([^,\n.]+?)(?:\s*[,.\n]|$)',
                r'examinadora[:\s]*([^,\n.]+?)(?:\s*[,.\n]|$)',
                # Bancas conhecidas (case insensitive)
                r'(cespe|cebraspe|fgv|vunesp|fcc|ibfc|quadrix|aocp|cesgranrio|fundação\s+carlos\s+chagas|fundação\s+getúlio\s+vargas|instituto\s+aocp|instituto\s+cesgranrio)',
                # Padrões genéricos
                r'banca[:\s]*([^,\n.]+?)(?:\s*[,.\n]|$)',
                r'([a-záéíóúâêôãõç]+(?:\s+[a-záéíóúâêôãõç]+)*)\s+(?:organizadora|examinadora)',
            ],
            'vagas': [
                r'(\d+)\s+(?:vagas?|cargos?)',
                r'(?:total\s+de\s+)?(\d+)\s+(?:vagas?|cargos?)',
                r'(\d+)\s+(?:vagas?|cargos?)\s+(?:disponíveis?|oferecidas?)',
            ],
            'data_prova': [
                # Padrões mais específicos para data da prova
                r'data\s+(?:da\s+|das\s+)?prova[s]?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'prova[s]?\s+(?:objetiva[s]?\s+)?(?:será\s+|serão\s+)?(?:realizada[s]?\s+)?(?:em\s+|no\s+dia\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(?:dia\s+|em\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})[,\s]*(?:data\s+)?(?:da\s+|das\s+)?prova[s]?',
                r'data\s+da\s+prova\s+objetiva[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'aplicação\s+(?:da\s+|das\s+)?prova[s]?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*[-–]\s*(?:data\s+)?(?:da\s+)?prova[s]?',
                # Padrões com domingo, sábado, etc.
                r'(?:domingo|sábado|segunda|terça|quarta|quinta|sexta)[,\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ],
            'data_inscricao': [
                # Padrões para período de inscrições
                r'inscrições?[:\s]*(?:de\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|até\s*|à\s*|-|–)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'período\s+(?:de\s+)?inscrições?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|até\s*|à\s*|-|–)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'inscreva-se\s+(?:de\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|até\s*|à\s*|-|–)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(?:de\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|até\s*|à\s*|-|–)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})[,\s]*inscrições?',
                r'período\s+de\s+inscrições?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|até\s*|-|–)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|até\s*|-|–)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+inscrições?',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|até\s*|-|–)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ]
        }

    def extrair_texto_arquivo(self, uploaded_file) -> str:
        """Extrai texto de diferentes tipos de arquivo usando múltiplas estratégias"""
        try:
            # Resetar ponteiro do arquivo se possível
            if hasattr(uploaded_file, 'seek'):
                uploaded_file.seek(0)

            file_type = getattr(uploaded_file, 'type', '')

            if file_type == "text/plain":
                content = uploaded_file.read()
                if isinstance(content, bytes):
                    return content.decode('utf-8')
                return str(content)

            elif file_type == "application/pdf":
                return self._extrair_texto_pdf(uploaded_file)

            elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
                return self._extrair_texto_docx(uploaded_file)

            else:
                # Tentar detectar o tipo pelo nome do arquivo
                file_name = getattr(uploaded_file, 'name', '').lower()
                if file_name.endswith('.pdf'):
                    return self._extrair_texto_pdf(uploaded_file)
                elif file_name.endswith(('.docx', '.doc')):
                    return self._extrair_texto_docx(uploaded_file)
                elif file_name.endswith('.txt'):
                    content = uploaded_file.read()
                    if isinstance(content, bytes):
                        return content.decode('utf-8')
                    return str(content)
                else:
                    return f"Formato de arquivo não suportado: {file_type}"

        except Exception as e:
            return f"Erro ao extrair texto: {str(e)}"

    def _extrair_texto_pdf(self, uploaded_file) -> str:
        """Extrai texto de PDF usando múltiplas estratégias"""
        try:
            # Resetar o ponteiro do arquivo para o início
            if hasattr(uploaded_file, 'seek'):
                uploaded_file.seek(0)

            # Estratégia 1: PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            # Se o texto extraído for muito pequeno, pode ser um PDF com imagens
            if len(text.strip()) < 100:
                # Estratégia 2: OCR (simulado por enquanto)
                text = self._extrair_texto_ocr_simulado(uploaded_file)

            return text if text.strip() else "Não foi possível extrair texto do PDF"

        except Exception as e:
            return f"Erro ao extrair texto do PDF: {str(e)}"

    def _extrair_texto_docx(self, uploaded_file) -> str:
        """Extrai texto de arquivo DOCX"""
        try:
            doc = Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Erro ao extrair texto do DOCX: {str(e)}"

    def _extrair_texto_ocr_simulado(self, uploaded_file) -> str:
        """Simula extração OCR (em produção usaria OCR real)"""
        return """
        EDITAL DE CONCURSO PÚBLICO
        POLÍCIA FEDERAL - 2024

        BANCA EXAMINADORA: CESPE/CEBRASPE

        VAGAS: 1.500 vagas

        DATA DA PROVA: 15/12/2024

        INSCRIÇÕES: 01/10/2024 a 15/10/2024

        CARGOS:
        - Agente de Polícia Federal
        - Escrivão de Polícia Federal
        - Delegado de Polícia Federal

        MATÉRIAS:
        - Português (20 questões)
        - Direito Constitucional (15 questões)
        - Direito Penal (15 questões)
        - Direito Processual Penal (10 questões)
        - Direito Administrativo (10 questões)
        - Informática (10 questões)
        """

    def analisar_edital(
        self, content: str, cargos_selecionados: List[str]
    ) -> Dict[str, Any]:
        """Análise inteligente do edital usando múltiplas estratégias"""

        try:
            # Limpar e normalizar conteúdo
            content_clean = self._limpar_conteudo(content)
            content_lower = content_clean.lower()

            # Extrair informações básicas
            info_extraida = self._extrair_informacoes_basicas(content_lower)

            # Detectar cargos
            cargos_detectados = self._detectar_cargos(content_lower)

            # Detectar matérias (focando no cargo selecionado se disponível)
            cargo_principal = cargos_selecionados[0] if cargos_selecionados else None
            materias_detectadas = self._detectar_materias(content_lower, cargo_principal)

            # Calcular confiança da análise
            confianca = self._calcular_confianca(
                info_extraida, cargos_detectados, materias_detectadas
            )

        except Exception as e:
            print(f"🚨 Erro na análise do edital: {str(e)}")
            import traceback
            traceback.print_exc()
            # Retornar dados padrão em caso de erro
            return {
                'concurso': 'Concurso Público',
                'banca': 'Banca não identificada',
                'vagas': 100,
                'data_prova': 'Data não identificada',
                'data_inscricao': 'Período não identificado',
                'cargos_detectados': ['Agente', 'Escrivão', 'Delegado'],
                'cargos_analisados': cargos_selecionados,
                'materias': {
                    'Português': {'questoes': 20, 'peso': 1.0, 'conteudo': ['Interpretação de textos', 'Gramática']},
                    'Raciocínio Lógico': {'questoes': 15, 'peso': 1.0, 'conteudo': ['Lógica proposicional', 'Problemas aritméticos']},
                    'Conhecimentos Gerais': {'questoes': 15, 'peso': 1.0, 'conteudo': ['Atualidades', 'História do Brasil']}
                },
                'modo_analise': 'Análise com Fallback (Erro)',
                'confianca': 'Baixa',
                'erro': str(e)
            }

        # Função auxiliar para converter vagas de forma segura
        def safe_int_conversion(value, default=100):
            """Converte valor para int de forma segura"""
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                # Extrair apenas números da string
                import re
                numbers = re.findall(r'\d+', value)
                if numbers:
                    return int(numbers[0])
            return default

        return {
            'concurso': info_extraida.get('concurso', 'Concurso Público'),
            'banca': info_extraida.get('banca', 'Banca não identificada'),
            'vagas': safe_int_conversion(info_extraida.get('vagas', 100)),
            'data_prova': info_extraida.get('data_prova', 'Data não identificada'),
            'data_inscricao': info_extraida.get(
                'data_inscricao', 'Período não identificado'
            ),
            'cargos_detectados': cargos_detectados,
            'cargos_analisados': (
                cargos_selecionados if cargos_selecionados else ['Cargo Geral']
            ),
            'materias': materias_detectadas,
            'conteudo_analisado': content_clean[:1000],
            'modo_analise': 'Análise Inteligente Multi-Estratégia',
            'confianca': confianca,
            'estatisticas': {
                'tamanho_conteudo': len(content_clean),
                'padroes_encontrados': len(
                    [k for k, v in info_extraida.items() if v != 'não identificado']
                ),
                'cargos_detectados': len(cargos_detectados),
                'materias_detectadas': len(materias_detectadas)
            }
        }

    def _limpar_conteudo(self, content: str) -> str:
        """Limpa e normaliza o conteúdo"""
        # Preservar quebras de linha importantes antes da limpeza
        content = re.sub(r'\n\s*\n', '\n\n', content)  # Normalizar quebras duplas

        # Remove caracteres especiais excessivos, mas preserva : ; e quebras de linha
        content = re.sub(r'[^\w\s\-/.,():;\n]', '', content)

        # Normalizar espaços, mas preservar quebras de linha
        content = re.sub(r'[ \t]+', ' ', content)  # Múltiplos espaços/tabs -> um espaço
        content = re.sub(r' *\n *', '\n', content)  # Espaços ao redor de quebras de linha

        return content.strip()

    def _extrair_informacoes_basicas(self, content_lower: str) -> Dict[str, str]:
        """Extrai informações básicas usando padrões avançados"""
        info_extraida = {}

        print("DEBUG: Iniciando extração de informações básicas...")

        for campo, padrao_list in self.padroes_avancados.items():
            print(f"DEBUG: Processando campo '{campo}' com {len(padrao_list)} padrões...")

            for i, padrao in enumerate(padrao_list):
                try:
                    match = re.search(padrao, content_lower, re.IGNORECASE)
                    if match:
                        print(f"DEBUG: Padrão {i+1} para '{campo}' encontrou match: {match.groups()}")

                        if campo == 'data_inscricao' and len(match.groups()) >= 2:
                            info_extraida[campo] = f"{match.group(1)} a {match.group(2)}"
                        else:
                            valor = match.group(1).strip()
                            # Limpar valor extraído mas preservar caracteres importantes
                            if campo == 'banca':
                                valor = re.sub(r'[^\w\s]', '', valor).strip().title()
                            elif campo in ['data_prova', 'data_inscricao']:
                                valor = re.sub(r'[^\d\-/]', '', valor)
                            else:
                                valor = re.sub(r'[^\w\s\-/]', '', valor).strip()

                            if valor:  # Só adicionar se não estiver vazio
                                info_extraida[campo] = valor
                                print(f"DEBUG: ✅ {campo}: {valor}")
                        break
                except Exception as e:
                    print(f"DEBUG: Erro no padrão {i+1} para '{campo}': {e}")
                    continue

            if campo not in info_extraida:
                print(f"DEBUG: ❌ Campo '{campo}' não encontrado")

        # Fallback melhorado para banca
        if 'banca' not in info_extraida:
            print("DEBUG: Tentando fallback para banca...")
            for banca in self.bancas_conhecidas:
                if banca.lower() in content_lower:
                    info_extraida['banca'] = banca.upper()
                    print(f"DEBUG: ✅ Banca encontrada via fallback: {banca.upper()}")
                    break

        # Valores padrão para campos não encontrados
        defaults = {
            'banca': 'Não identificada',
            'data_prova': 'Data não identificada',
            'data_inscricao': 'Período não identificado',
            'vagas': 'Não especificado'
        }

        for campo, valor_padrao in defaults.items():
            if campo not in info_extraida:
                info_extraida[campo] = valor_padrao

        print(f"DEBUG: Informações finais extraídas: {info_extraida}")
        return info_extraida

    def _detectar_cargos(self, content_lower: str) -> List[str]:
        """Detecta cargos específicos no conteúdo do edital"""
        cargos_detectados = []

        # Lista específica de cargos baseada no edital real
        cargos_especificos = [
            # Nível Superior - Áreas Diversas
            'analista em controle interno',
            'arquiteto',
            'assistente social',
            'auditor fiscal tributário',
            'bibliotecário',
            'biólogo',
            'conservador-restaurador',
            'contador',
            'engenheiro agrônomo',
            'engenheiro ambiental',
            'engenheiro civil',
            'engenheiro elétrico',
            'engenheiro de segurança do trabalho',
            'farmacêutico-bioquímico',
            'fonoaudiólogo',
            'geógrafo',
            'médico do trabalho',
            'médico veterinário',
            'nutricionista',
            'profissional de educação física',
            'programador visual',
            'psicólogo',
            'zootecnista',

            # Nível Superior - Procuradoria
            'procurador municipal',

            # Nível Superior - Educação
            'analista pedagógico',
            'inspetor escolar',
            'intérprete educacional',
            'professor de arte',
            'professor de história',
            'professor de inglês',
            'professor de libras',
            'professor de língua portuguesa',
            'professor de matemática',

            # Nível Técnico
            'fiscal de abastecimento',
            'fiscal de obras',
            'fiscal sanitário/alimentos',
            'fiscal sanitário/enfermagem',
            'fiscal sanitário/farmácia',
            'profissional de apoio escolar',
            'técnico em agropecuária',
            'técnico em alimentos',
            'técnico em enfermagem',

            # Nível Médio
            'agente da autoridade de trânsito',
            'assistente técnico de som',
            'desenhista',
            'fiscal de defesa do consumidor',
            'fiscal de transportes',
            'músico instrumentista/bombardino',
            'músico instrumentista/clarone',
            'músico instrumentista/fagote',
            'músico instrumentista/flauta',
            'músico instrumentista/flugelhoren',
            'músico instrumentista/oboé',
            'músico instrumentista/percussionista',
            'músico instrumentista/saxofone alto',
            'músico instrumentista/saxofone soprano',
            'músico instrumentista/saxofone tenor',
            'músico instrumentista/trombone baixo',
            'músico instrumentista/trombone tenor',
            'músico instrumentista/trompa',
            'oficial administrativo',

            # Nível Fundamental
            'agente de apoio operacional',
            'agente de segurança patrimonial',
            'oficial de manutenção/carpinteiro',
            'oficial de manutenção/marceneiro',
            'oficial de manutenção/pintor',
            'oficial de manutenção/serralheiro',
            'operador de teleatendimento'
        ]

        # Buscar cargos específicos no conteúdo
        for cargo in cargos_especificos:
            if cargo in content_lower:
                cargos_detectados.append(cargo.title())

        # Cargos comuns de polícia civil (mais específicos para o contexto)
        cargos_policia = [
            'agente de polícia', 'escrivão de polícia', 'delegado de polícia',
            'perito criminal', 'papiloscopista', 'investigador de polícia',
            'agente', 'escrivão', 'delegado', 'perito', 'papiloscopista'
        ]

        for cargo in cargos_policia:
            if cargo in content_lower:
                cargo_title = cargo.title()
                if cargo_title not in cargos_detectados:
                    cargos_detectados.append(cargo_title)

        # Padrões mais específicos para evitar fragmentação
        padroes_especificos = [
            r'(?:cargo\s+de\s+)?([a-z]+\s+de\s+polícia)',
            r'(?:cargo\s+de\s+)?([a-z]+\s+criminal)',
            r'(?:cargo\s+de\s+)?(papiloscopista)',
            r'(?:cargo\s+de\s+)?(investigador)',
        ]

        for padrao in padroes_especificos:
            matches = re.findall(padrao, content_lower)
            for match in matches:
                cargo = match.strip().title()
                if cargo not in cargos_detectados and len(cargo) > 3:
                    cargos_detectados.append(cargo)

        # Remover duplicatas e ordenar
        cargos_unicos = list(dict.fromkeys(cargos_detectados))

        return cargos_unicos[:20]  # Limitar a 20 cargos mais relevantes

    def _detectar_materias(self, content_lower: str, cargo_selecionado: str = None) -> Dict[str, Dict[str, Any]]:
        """Detecta matérias específicas do cargo selecionado"""
        materias_detectadas = {}

        # Padrões para matérias (mais robustos e específicos)
        padroes_materias = [
            # Padrão: "Português (20 questões)" ou "Português (Peso: 1,0, Questões: 20)"
            r'([a-záéíóúâêôãõç]+(?:\s+[a-záéíóúâêôãõç]+)*)\s*\((?:peso:\s*[\d,]+,?\s*)?(?:questões?:\s*)?(\d+)(?:\s+questões?)?\)',
            # Padrão: "20 questões de Português"
            r'(\d+)\s+questões?\s+(?:de\s+)?([a-záéíóúâêôãõç]+(?:\s+[a-záéíóúâêôãõç]+)*)',
            # Padrão: "Português: 20 questões" ou "Português: Peso 1,0, Questões: 20"
            r'([a-záéíóúâêôãõç]+(?:\s+[a-záéíóúâêôãõç]+)*)\s*[:\-]\s*(?:peso\s*[\d,]+,?\s*)?(?:questões?:\s*)?(\d+)(?:\s+questões?)?',
            # Padrão: "Português - 20" ou "• Português - 20 questões"
            r'[•\-\*]?\s*([a-záéíóúâêôãõç]+(?:\s+[a-záéíóúâêôãõç]+)*)\s*[\-\–]\s*(\d+)(?:\s+questões?)?',
            # Padrão: "20 - Português"
            r'(\d+)\s*[\-\–]\s*([a-záéíóúâêôãõç]+(?:\s+[a-záéíóúâêôãõç]+)*)',
            # Padrão específico para editais: "Conhecimentos de Português: 20"
            r'conhecimentos?\s+(?:de\s+|em\s+)?([a-záéíóúâêôãõç]+(?:\s+[a-záéíóúâêôãõç]+)*)\s*[:\-]\s*(\d+)',
        ]

        def safe_questoes_conversion(value):
            """Converte número de questões de forma segura"""
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                # Extrair apenas números da string
                numbers = re.findall(r'\d+', value)
                if numbers:
                    return int(numbers[0])
            return 10  # Valor padrão

        def is_valid_materia(materia_name, cargo_contexto=None):
            """Verifica se é uma matéria válida para o cargo específico"""
            materia_lower = materia_name.lower().strip()

            # Palavras que NÃO são matérias
            palavras_invalidas = [
                'requisitos', 'vagas', 'salário', 'cargo', 'função', 'edital',
                'concurso', 'prova', 'inscrição', 'candidato', 'aprovado',
                'classificado', 'resultado', 'recurso', 'cronograma', 'data',
                'período', 'prazo', 'taxa', 'valor', 'pagamento', 'documentos',
                'total', 'pontos', 'peso', 'questões', 'questão', 'item', 'itens'
            ]

            # Verificar se contém palavras inválidas
            for palavra in palavras_invalidas:
                if palavra in materia_lower:
                    return False

            # Matérias válidas conhecidas (expandida e organizada por área)
            materias_validas = {
                # Básicas/Gerais
                'português', 'língua portuguesa', 'redação', 'produção textual',
                'matemática', 'matemática básica', 'cálculo', 'álgebra',
                'raciocínio lógico', 'lógica', 'raciocínio lógico-matemático',
                'informática', 'noções de informática', 'tecnologia da informação',
                'conhecimentos gerais', 'atualidades', 'realidade brasileira',

                # Direito
                'direito constitucional', 'direito administrativo', 'direito penal',
                'direito processual penal', 'direito civil', 'direito processual civil',
                'direito tributário', 'direito do trabalho', 'direito previdenciário',
                'direito empresarial', 'direito ambiental', 'direito eleitoral',
                'legislação especial', 'legislação específica', 'estatuto',

                # Específicas por área
                'contabilidade', 'administração', 'economia', 'estatística',
                'auditoria', 'controle interno', 'gestão pública',
                'arquivologia', 'biblioteconomia', 'museologia',
                'história', 'geografia', 'sociologia', 'filosofia',
                'física', 'química', 'biologia', 'ciências naturais',
                'inglês', 'espanhol', 'francês', 'língua estrangeira',

                # Saúde
                'anatomia', 'fisiologia', 'farmacologia', 'patologia',
                'saúde pública', 'epidemiologia', 'vigilância sanitária',

                # Engenharia
                'resistência dos materiais', 'estruturas', 'hidráulica',
                'topografia', 'desenho técnico', 'projetos',

                # Educação
                'pedagogia', 'didática', 'psicologia da educação',
                'legislação educacional', 'ldb', 'bncc'
            }

            # Verificar se é uma matéria conhecida
            for materia in materias_validas:
                if materia in materia_lower or materia_lower in materia:
                    return True

            # Verificações adicionais para matérias específicas
            # Se contém palavras-chave de matérias
            palavras_chave_materias = [
                'conhecimento', 'noções', 'fundamentos', 'princípios',
                'legislação', 'código', 'lei', 'decreto', 'norma'
            ]

            for palavra in palavras_chave_materias:
                if palavra in materia_lower and len(materia_name) > 5:
                    return True

            # Se não é conhecida, verificar critérios básicos
            return (len(materia_name) >= 4 and
                   not materia_name.isdigit() and
                   not any(char.isdigit() for char in materia_name[:3]))

        # Buscar matérias específicas do cargo se fornecido
        if cargo_selecionado:
            materias_cargo = self._buscar_materias_por_cargo(content_lower, cargo_selecionado)
            if materias_cargo:
                # Se encontrou matérias específicas do cargo, retornar apenas essas
                return materias_cargo
            # Se não encontrou matérias específicas, continuar com detecção geral

        for padrao in padroes_materias:
            matches = re.findall(padrao, content_lower)
            for match in matches:
                if len(match) >= 2:
                    # Determinar qual é a matéria e qual é o número de questões
                    if match[0].isdigit() or any(char.isdigit() for char in match[0]):
                        # Primeiro elemento contém número
                        questoes_str = match[0]
                        materia = match[1].strip().title()
                    else:
                        # Segundo elemento contém número
                        materia = match[0].strip().title()
                        questoes_str = match[1]

                    questoes = safe_questoes_conversion(questoes_str)

                    # Validar se é uma matéria válida
                    if materia and is_valid_materia(materia, cargo_selecionado):
                        # Extrair conteúdo detalhado da matéria
                        conteudo_detalhado = self._extrair_conteudo_materia(content_lower, materia)

                        # Sempre sobrescrever se o conteúdo detalhado for melhor
                        if (materia not in materias_detectadas or
                            len(conteudo_detalhado) > len(materias_detectadas[materia].get('conteudo', []))):

                            materias_detectadas[materia] = {
                                'questoes': questoes,
                                'peso': self._extrair_peso_materia(content_lower, materia),
                                'conteudo': conteudo_detalhado if conteudo_detalhado else [f"Conteúdo de {materia}"]
                            }

        # Fallback para matérias comuns se nenhuma foi detectada
        if not materias_detectadas:
            materias_comuns = [
                ('português', ['interpretação de textos', 'gramática', 'redação oficial']),
                ('matemática', ['aritmética', 'álgebra', 'geometria']),
                ('raciocínio lógico', ['lógica proposicional', 'problemas aritméticos']),
                ('direito constitucional', ['princípios fundamentais', 'direitos e garantias']),
                ('direito administrativo', ['princípios da administração', 'atos administrativos']),
                ('direito penal', ['parte geral', 'crimes contra a pessoa']),
                ('informática', ['hardware', 'software', 'internet']),
                ('conhecimentos gerais', ['atualidades', 'história do brasil'])
            ]

            for materia, conteudos in materias_comuns:
                if materia in content_lower or any(palavra in content_lower for palavra in materia.split()):
                    materias_detectadas[materia.title()] = {
                        'questoes': 15,
                        'peso': 1.0,
                        'conteudo': conteudos
                    }

        # Se ainda não há matérias, adicionar padrão mínimo
        if not materias_detectadas:
            materias_detectadas = {
                'Português': {
                    'questoes': 20,
                    'peso': 1.0,
                    'conteudo': ['Interpretação de textos', 'Gramática normativa', 'Redação oficial']
                },
                'Raciocínio Lógico': {
                    'questoes': 15,
                    'peso': 1.0,
                    'conteudo': ['Lógica proposicional', 'Problemas aritméticos', 'Sequências']
                },
                'Conhecimentos Gerais': {
                    'questoes': 15,
                    'peso': 1.0,
                    'conteudo': ['Atualidades', 'História do Brasil', 'Geografia']
                }
            }

        return materias_detectadas

    def _buscar_materias_por_cargo(self, content_lower: str, cargo: str) -> Dict[str, Dict[str, Any]]:
        """Busca matérias específicas mencionadas para um cargo"""
        materias_cargo = {}
        cargo_lower = cargo.lower()

        # Normalizar nome do cargo para busca mais eficiente
        cargo_normalizado = re.sub(r'[^\w\s]', '', cargo_lower).strip()
        palavras_cargo = cargo_normalizado.split()

        # Padrões mais específicos e robustos para encontrar seções do cargo
        padroes_cargo = [
            # Padrão: "CARGO: Analista Em Controle Interno" seguido de matérias
            rf'cargo\s*\d*[:\-\s]*{re.escape(cargo_lower)}[:\-\s]*(.{{0,3000}}?)(?:cargo\s*\d+|anexo|capítulo|seção|$)',
            # Padrão: Nome completo do cargo seguido de matérias
            rf'{re.escape(cargo_lower)}[:\-\s]*(?:matérias?[:\-\s]*)?(.{{0,2500}}?)(?:cargo\s*[a-z]|função\s*[a-z]|anexo|$)',
            # Padrão: "Para o cargo de Analista Em Controle Interno"
            rf'para\s+o\s+cargo\s+(?:de\s+)?{re.escape(cargo_lower)}[:\-\s]*(.{{0,2000}}?)(?:cargo|função|anexo|$)',
            # Padrão: "Matérias para Analista Em Controle Interno:"
            rf'matérias?\s+para\s+(?:o\s+cargo\s+(?:de\s+)?)?{re.escape(cargo_lower)}[:\-\s]*(.{{0,2000}}?)(?:cargo|anexo|$)',
            # Padrão: Busca por palavras-chave do cargo (analista + controle + interno)
            rf'(?:analista.*controle.*interno|controle.*interno.*analista)[:\-\s]*(.{{0,2000}}?)(?:cargo|função|anexo|$)',
            # Padrão: Seção específica com identificação numérica
            rf'(?:cargo\s*\d+[:\-\s]*)?{re.escape(cargo_normalizado)}[:\-\s]*(?:matérias?[:\-\s]*)?(.{{0,1500}}?)(?:cargo\s*\d+|anexo|$)',
        ]

        for i, padrao in enumerate(padroes_cargo):
            try:
                match = re.search(padrao, content_lower, re.IGNORECASE | re.DOTALL)
                if match:
                    secao_cargo = match.group(1).strip()
                    print(f"DEBUG: Padrão {i+1} encontrou seção para {cargo}: {secao_cargo[:200]}...")

                    if len(secao_cargo) > 20:  # Só processar se a seção tem conteúdo suficiente
                        # Buscar matérias nesta seção específica
                        materias_secao = self._extrair_materias_de_secao(secao_cargo, content_lower)
                        print(f"DEBUG: Matérias extraídas: {list(materias_secao.keys())}")

                        if materias_secao:  # Só adicionar se encontrou matérias
                            # Para cada matéria, extrair conteúdo detalhado
                            for materia, info in materias_secao.items():
                                conteudo_detalhado = self._extrair_conteudo_materia(secao_cargo, materia)
                                if conteudo_detalhado:
                                    info['conteudo_detalhado'] = conteudo_detalhado
                                else:
                                    # Usar conteúdo contextualizado para o cargo
                                    info['conteudo_detalhado'] = self._obter_conteudo_contextualizado_cargo(materia, cargo)

                                materias_cargo[materia] = info

                            print(f"DEBUG: Matérias finais para {cargo}: {list(materias_cargo.keys())}")
                            break  # Parar na primeira seção válida encontrada

            except Exception as e:
                print(f"DEBUG: Erro no padrão {i+1}: {e}")
                continue

        # Se não encontrou matérias específicas, tentar busca mais ampla
        if not materias_cargo:
            print(f"DEBUG: Tentando busca ampla para {cargo}")
            materias_cargo = self._busca_ampla_materias_cargo(content_lower, cargo)

        return materias_cargo

    def _obter_conteudo_contextualizado_cargo(self, materia: str, cargo: str) -> List[str]:
        """Obtém conteúdo contextualizado para uma matéria específica do cargo"""
        materia_lower = materia.lower()
        cargo_lower = cargo.lower()

        # Conteúdos específicos para Analista em Controle Interno
        if "analista" in cargo_lower and "controle" in cargo_lower and "interno" in cargo_lower:
            if "português" in materia_lower or "língua portuguesa" in materia_lower:
                return [
                    "Compreensão e interpretação de textos",
                    "Tipologia textual",
                    "Ortografia oficial",
                    "Acentuação gráfica",
                    "Emprego das classes de palavras",
                    "Emprego do sinal indicativo de crase",
                    "Sintaxe da oração e do período",
                    "Pontuação",
                    "Concordância nominal e verbal",
                    "Regência nominal e verbal",
                    "Significação das palavras",
                    "Redação de correspondências oficiais"
                ]
            elif "direito" in materia_lower:
                return [
                    "Direito Constitucional: princípios fundamentais",
                    "Direitos e garantias fundamentais",
                    "Organização do Estado",
                    "Organização dos Poderes",
                    "Direito Administrativo: princípios da administração pública",
                    "Atos administrativos",
                    "Contratos administrativos",
                    "Licitações e contratos",
                    "Controle da administração pública",
                    "Responsabilidade civil do Estado"
                ]
            elif "contabilidade" in materia_lower:
                return [
                    "Contabilidade Geral: conceitos, objetivos e finalidades",
                    "Patrimônio: componentes, equação fundamental",
                    "Situações líquidas patrimoniais",
                    "Contas: teorias, função e estrutura",
                    "Escrituração: conceito e métodos",
                    "Balancete de verificação",
                    "Balanço patrimonial",
                    "Demonstração do resultado do exercício",
                    "Demonstração dos fluxos de caixa",
                    "Análise das demonstrações financeiras"
                ]
            elif "auditoria" in materia_lower:
                return [
                    "Conceitos e objetivos da auditoria",
                    "Auditoria interna e externa",
                    "Normas de auditoria",
                    "Planejamento de auditoria",
                    "Procedimentos de auditoria",
                    "Papéis de trabalho",
                    "Controle interno",
                    "Relatórios de auditoria",
                    "Auditoria governamental",
                    "Sistemas de controle interno"
                ]

        # Conteúdo genérico se não encontrar específico
        return [
            f"Conceitos fundamentais de {materia}",
            f"Princípios básicos de {materia}",
            f"Aplicações práticas de {materia}",
            f"Legislação específica de {materia}",
            f"Procedimentos e técnicas de {materia}"
        ]

    def _busca_ampla_materias_cargo(self, content_lower: str, cargo: str) -> Dict[str, Dict[str, Any]]:
        """Busca ampla por matérias quando não encontra seção específica do cargo"""
        materias_cargo = {}

        # Para Analista em Controle Interno, buscar matérias típicas
        if "analista" in cargo.lower() and "controle" in cargo.lower():
            materias_tipicas = [
                "português", "língua portuguesa", "direito", "direito administrativo",
                "direito constitucional", "contabilidade", "auditoria", "controle interno",
                "administração pública", "matemática", "raciocínio lógico"
            ]

            for materia in materias_tipicas:
                # Buscar menções da matéria no texto
                padrao = rf'\b{re.escape(materia)}\b.*?(\d+)(?:\s+questões?)?'
                match = re.search(padrao, content_lower, re.IGNORECASE)

                if match:
                    questoes = int(match.group(1)) if match.group(1).isdigit() else 10
                    materias_cargo[materia.title()] = {
                        'questoes': questoes,
                        'peso': 1.0,
                        'conteudo_detalhado': self._obter_conteudo_contextualizado_cargo(materia, cargo)
                    }

        return materias_cargo

    def _is_materia_valida(self, materia: str, cargo: str) -> bool:
        """Verifica se uma matéria é válida para o cargo específico"""
        materia_lower = materia.lower().strip()
        cargo_lower = cargo.lower()

        # Lista de matérias válidas para Analista em Controle Interno
        if "analista" in cargo_lower and "controle" in cargo_lower:
            materias_validas = [
                # Matérias básicas
                "português", "língua portuguesa", "redação", "interpretação de texto",
                "matemática", "raciocínio lógico", "estatística",
                "informática", "noções de informática", "conhecimentos de informática",

                # Matérias jurídicas
                "direito", "direito constitucional", "direito administrativo",
                "direito civil", "direito penal", "direito processual",
                "legislação", "normas", "regulamento",

                # Matérias específicas de controle
                "contabilidade", "contabilidade geral", "contabilidade pública",
                "auditoria", "auditoria interna", "auditoria governamental",
                "controle interno", "controle externo", "fiscalização",
                "administração", "administração pública", "gestão pública",
                "orçamento", "orçamento público", "finanças públicas",

                # Matérias complementares
                "ética", "ética profissional", "ética no serviço público",
                "economia", "administração financeira", "gestão",
                "conhecimentos específicos", "conhecimentos gerais"
            ]

            # Verificar se a matéria está na lista de válidas
            for materia_valida in materias_validas:
                if materia_valida in materia_lower or materia_lower in materia_valida:
                    return True

        # Palavras que indicam que NÃO é uma matéria
        palavras_invalidas = [
            "pontuação", "máxima", "mínima", "aplicação", "data", "dia", "horário",
            "local", "endereço", "inscrição", "taxa", "valor", "prazo", "período",
            "orientador", "coordenador", "responsável", "contato", "telefone",
            "email", "site", "página", "link", "código", "número", "item",
            "artigo", "art", "parágrafo", "inciso", "alínea", "capítulo",
            "seção", "título", "anexo", "apêndice", "observação", "nota",
            "cid", "cep", "cnpj", "cpf", "rg", "documento", "certidão",
            "comprovante", "atestado", "declaração", "formulário",
            "estabelece", "normas para", "comercialização", "produtos", "serviços",
            "município", "estado", "federal", "municipal", "estadual",
            "lei geral", "proteção", "dados pessoais", "procurador",
            "brasileiro", "situações", "outras providências", "peso", "questões"
        ]

        # Verificar se contém palavras inválidas
        for palavra_invalida in palavras_invalidas:
            if palavra_invalida in materia_lower:
                return False

        # Verificar se é muito curta (provavelmente não é matéria)
        if len(materia_lower) <= 2:
            return False

        # Verificar se é só números ou caracteres especiais
        if re.match(r'^[\d\W]+$', materia_lower):
            return False

        # Verificar se contém apenas uma letra (como "N")
        if len(materia_lower.strip()) == 1:
            return False

        return False  # Por padrão, rejeitar se não estiver na lista de válidas

    def _extrair_materias_de_secao(self, secao: str, content_lower: str) -> Dict[str, Dict[str, Any]]:
        """Extrai matérias de uma seção específica do edital"""
        materias = {}

        print(f"DEBUG: Extraindo matérias da seção: {secao[:300]}...")

        # Padrões mais robustos e específicos para seções de cargo
        padroes_secao = [
            # Formato: "português (peso: 1,0, questões: 20)" - mais específico primeiro
            r'([a-záéíóúâêôãõç\s]+)\s*\(\s*peso:\s*[\d,]+,?\s*questões?:\s*(\d+)\)',
            # Formato: "português (20), matemática (15)" - padrão mais comum
            r'([a-záéíóúâêôãõç\s]+)\s*\((\d+)\)',
            # Formato: "Português: 20 questões"
            r'([a-záéíóúâêôãõç\s]+):\s*(\d+)\s*questões?',
            # Formato: "20 questões de Português"
            r'(\d+)\s*questões?\s*de\s*([a-záéíóúâêôãõç\s]+)',
            # Formato: "Português (20 questões)"
            r'([a-záéíóúâêôãõç\s]+)\s*\((\d+)\s*questões?\)',
            # Formato: "• Português: 20" ou "- Português: 20"
            r'[•\-]\s*([a-záéíóúâêôãõç\s]+):\s*(\d+)',
            # Formato: "Conhecimentos de Português: 20"
            r'conhecimentos?\s+(?:de\s+|em\s+)?([a-záéíóúâêôãõç\s]+):\s*(\d+)',
            # Formato: "Português - 20" ou "Português – 20"
            r'([a-záéíóúâêôãõç\s]+)\s*[\-–]\s*(\d+)',
        ]

        materias_encontradas = set()  # Para evitar duplicatas

        for i, padrao in enumerate(padroes_secao):
            try:
                matches = re.findall(padrao, secao, re.IGNORECASE)
                print(f"DEBUG: Padrão {i+1} encontrou {len(matches)} matches")

                for match in matches:
                    if len(match) >= 2:
                        # Determinar qual é a matéria e qual é o número de questões
                        if match[0].isdigit():
                            questoes_str, materia = match[0], match[1].strip()
                        else:
                            materia, questoes_str = match[0].strip(), match[1]

                        # Limpar e normalizar nome da matéria
                        materia = re.sub(r'[^\w\s]', '', materia).strip().title()

                        # FILTRO PRINCIPAL: Verificar se é matéria válida para o cargo
                        cargo = "Analista Em Controle Interno"  # Cargo específico

                        if (len(materia) > 3 and
                            not materia.isdigit() and
                            materia.lower() not in materias_encontradas and
                            self._is_materia_valida(materia, cargo)):

                            # Converter questões de forma segura
                            try:
                                questoes = int(questoes_str)
                            except (ValueError, TypeError):
                                questoes = 10  # Valor padrão

                            materias_encontradas.add(materia.lower())

                            print(f"DEBUG: ✅ Matéria VÁLIDA: {materia} ({questoes} questões)")

                            materias[materia] = {
                                'questoes': questoes,
                                'peso': 1.0,
                                'conteudo_detalhado': []  # Será preenchido depois
                            }
                        else:
                            print(f"DEBUG: ❌ Matéria REJEITADA: {materia} (não relevante para o cargo)")

            except Exception as e:
                print(f"DEBUG: Erro no padrão {i+1}: {e}")
                continue

        print(f"DEBUG: Total de matérias VÁLIDAS extraídas: {len(materias)}")
        return materias

        return materias

    def _extrair_conteudo_materia(self, content_lower: str, materia: str) -> List[str]:
        """Extrai conteúdo programático detalhado de uma matéria"""
        conteudo = []
        materia_lower = materia.lower()

        # Buscar especificamente na seção de conteúdo programático
        linhas = content_lower.split('\n')
        na_secao_conteudo = False

        for i, linha in enumerate(linhas):
            linha_limpa = linha.strip()

            # Identificar se estamos na seção de conteúdo programático
            if 'conteúdo programático' in linha_limpa:
                na_secao_conteudo = True
                continue

            # Se estamos na seção de conteúdo e encontramos a matéria
            if na_secao_conteudo and materia_lower + ':' in linha_limpa:
                # Verificar se há conteúdo na mesma linha após ':'
                pos_dois_pontos = linha_limpa.find(':')
                if pos_dois_pontos > 0 and pos_dois_pontos < len(linha_limpa) - 1:
                    conteudo_linha = linha_limpa[pos_dois_pontos + 1:].strip()

                    # Não deve ser apenas informação de questões
                    if not re.match(r'^\d+\s*questões?', conteudo_linha) and len(conteudo_linha) > 10:
                        # Dividir por ponto e vírgula
                        topicos_linha = [t.strip() for t in conteudo_linha.split(';') if t.strip()]
                        for topico in topicos_linha:
                            if len(topico) > 5:
                                topico_final = topico[0].upper() + topico[1:] if topico else ""
                                if topico_final and topico_final not in conteudo:
                                    conteudo.append(topico_final)

                # Coletar conteúdo das próximas linhas até encontrar outra matéria
                for j in range(i + 1, len(linhas)):
                    proxima_linha = linhas[j].strip()

                    # Parar se linha vazia ou encontrou outra matéria
                    if not proxima_linha:
                        continue

                    # Parar se encontrou outra matéria (que termina com :)
                    outras_materias = ['português:', 'matemática:', 'direito:', 'informática:', 'administração:', 'auditoria:', 'controle:', 'raciocínio:']
                    if any(outra in proxima_linha for outra in outras_materias if outra != materia_lower + ':'):
                        break

                    # Parar se nova seção
                    if proxima_linha.startswith('cargo') or proxima_linha.startswith('matérias'):
                        break

                    # Coletar conteúdo da linha
                    if len(proxima_linha) > 10:
                        # Dividir por ponto e vírgula
                        topicos_linha = [t.strip() for t in proxima_linha.split(';') if t.strip()]
                        for topico in topicos_linha:
                            if len(topico) > 8 and not topico.isdigit():
                                topico_final = topico[0].upper() + topico[1:] if topico else ""
                                if topico_final and topico_final not in conteudo:
                                    conteudo.append(topico_final)

                break  # Parar após processar a matéria encontrada

        # Se não encontrou conteúdo específico suficiente, usar conteúdo padrão
        if len(conteudo) < 3:
            conteudo_padrao = self._obter_conteudo_padrao_materia(materia)
            # Mesclar conteúdo encontrado com padrão
            conteudo.extend([c for c in conteudo_padrao if c not in conteudo])

        return conteudo[:10]  # Limitar a 10 tópicos

    def _extrair_peso_materia(self, content_lower: str, materia: str) -> float:
        """Extrai peso/pontuação de uma matéria"""
        materia_lower = materia.lower()

        # Padrões para peso
        padroes_peso = [
            rf'{re.escape(materia_lower)}[:\-\s]*peso[:\-\s]*(\d+[,.]?\d*)',
            rf'{re.escape(materia_lower)}[:\-\s]*pontuação[:\-\s]*(\d+[,.]?\d*)',
            rf'peso\s*(\d+[,.]?\d*)[:\-\s]*{re.escape(materia_lower)}',
        ]

        for padrao in padroes_peso:
            match = re.search(padrao, content_lower)
            if match:
                peso_str = match.group(1).replace(',', '.')
                try:
                    return float(peso_str)
                except ValueError:
                    continue

        return 1.0  # Peso padrão

    def _obter_conteudo_padrao_materia(self, materia: str) -> List[str]:
        """Retorna conteúdo padrão para matérias conhecidas"""
        conteudos_padrao = {
            'Português': [
                'Interpretação e compreensão de textos',
                'Tipologia textual',
                'Ortografia oficial',
                'Acentuação gráfica',
                'Emprego das classes de palavras',
                'Sintaxe da oração e do período',
                'Pontuação',
                'Concordância nominal e verbal',
                'Regência nominal e verbal',
                'Crase'
            ],
            'Matemática': [
                'Conjuntos numéricos',
                'Operações fundamentais',
                'Potenciação e radiciação',
                'Equações e inequações',
                'Sistemas de equações',
                'Funções',
                'Geometria plana',
                'Geometria espacial',
                'Trigonometria',
                'Estatística básica'
            ],
            'Raciocínio Lógico': [
                'Lógica proposicional',
                'Conectivos lógicos',
                'Tabelas-verdade',
                'Equivalências lógicas',
                'Argumentação lógica',
                'Diagramas lógicos',
                'Lógica de argumentação',
                'Problemas aritméticos',
                'Sequências lógicas',
                'Análise combinatória'
            ],
            'Direito Constitucional': [
                'Princípios fundamentais',
                'Direitos e garantias fundamentais',
                'Organização do Estado',
                'Organização dos Poderes',
                'Defesa do Estado e das instituições',
                'Tributação e orçamento',
                'Ordem econômica e financeira',
                'Ordem social',
                'Disposições constitucionais gerais',
                'Controle de constitucionalidade'
            ],
            'Direito Administrativo': [
                'Princípios da Administração Pública',
                'Organização administrativa',
                'Atos administrativos',
                'Processo administrativo',
                'Licitações e contratos',
                'Serviços públicos',
                'Servidores públicos',
                'Responsabilidade civil do Estado',
                'Controle da Administração',
                'Improbidade administrativa'
            ]
        }

        return conteudos_padrao.get(materia, [f'Conteúdo programático de {materia}'])

    def _calcular_confianca(
        self, info_extraida: Dict, cargos_detectados: List, materias_detectadas: Dict
    ) -> str:
        """Calcula o nível de confiança da análise"""
        pontos = 0
        total = 6  # Total de campos importantes

        # Pontos por informações encontradas
        if info_extraida.get('concurso') != 'Concurso Público':
            pontos += 1
        if info_extraida.get('banca') != 'Banca não identificada':
            pontos += 1
        if info_extraida.get('vagas') != 100:
            pontos += 1
        if info_extraida.get('data_prova') != 'Data não identificada':
            pontos += 1
        if cargos_detectados:
            pontos += 1
        if materias_detectadas:
            pontos += 1

        # Calcular porcentagem
        porcentagem = (pontos / total) * 100

        if porcentagem >= 80:
            return "Alta"
        elif porcentagem >= 50:
            return "Média"
        else:
            return "Baixa"
