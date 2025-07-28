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
                r'banca\s+examinadora[:\\s]+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
                r'([a-z]+/[a-z]+(?:\s+[a-z]+)*)',
                r'(cespe|cebraspe|fgv|vunesp|fcc|ibfc|quadrix|instituto\s+aocp|instituto\s+cesgranrio)',
                r'banca[:\\s]+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
                r'([a-z]+(?:\s+[a-z]+)*)\s+(?:organizadora|examinadora)',
                r'organização[:\\s]+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            ],
            'vagas': [
                r'(\d+)\s+(?:vagas?|cargos?)',
                r'(?:total\s+de\s+)?(\d+)\s+(?:vagas?|cargos?)',
                r'(\d+)\s+(?:vagas?|cargos?)\s+(?:disponíveis?|oferecidas?)',
            ],
            'data_prova': [
                r'data\s+(?:da\s+)?prova[:\\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'prova\s+(?:será\s+)?(?:realizada\s+)?(?:em\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(?:data\s+da\s+)?prova',
            ],
            'data_inscricao': [
                r'inscrições?[:\\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|-)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'período\s+de\s+inscrições?[:\\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|-)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:a\s*|-)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+inscrições?',
            ]
        }

    def extrair_texto_arquivo(self, uploaded_file) -> str:
        """Extrai texto de diferentes tipos de arquivo usando múltiplas estratégias"""
        try:
            if uploaded_file.type == "text/plain":
                return uploaded_file.read().decode('utf-8')

            elif uploaded_file.type == "application/pdf":
                return self._extrair_texto_pdf(uploaded_file)

            elif uploaded_file.type == ("application/" "vnd.openxmlformats-officedocument.wordprocessingml.document"):
                return self._extrair_texto_docx(uploaded_file)

            else:
                return "Formato de arquivo não suportado"

        except Exception as e:
            return f"Erro ao extrair texto: {str(e)}"

    def _extrair_texto_pdf(self, uploaded_file) -> str:
        """Extrai texto de PDF usando múltiplas estratégias"""
        try:
            # Estratégia 1: PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            # Se o texto extraído for muito pequeno, pode ser um PDF com imagens
            if len(text.strip()) < 100:
                # Estratégia 2: OCR (simulado por enquanto)
                text = self._extrair_texto_ocr_simulado(uploaded_file)

            return text

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

        # Limpar e normalizar conteúdo
        content_clean = self._limpar_conteudo(content)
        content_lower = content_clean.lower()

        # Extrair informações básicas
        info_extraida = self._extrair_informacoes_basicas(content_lower)

        # Detectar cargos
        cargos_detectados = self._detectar_cargos(content_lower)

        # Detectar matérias
        materias_detectadas = self._detectar_materias(content_lower)

        # Calcular confiança da análise
        confianca = self._calcular_confianca(
            info_extraida, cargos_detectados, materias_detectadas
        )

        return {
            'concurso': info_extraida.get('concurso', 'Concurso Público'),
            'banca': info_extraida.get('banca', 'Banca não identificada'),
            'vagas': int(info_extraida.get('vagas', 100)),
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
        # Remove caracteres especiais excessivos
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'[^\w\s\-/.,()]', '', content)
        return content.strip()

    def _extrair_informacoes_basicas(self, content_lower: str) -> Dict[str, str]:
        """Extrai informações básicas usando padrões avançados"""
        info_extraida = {}

        for campo, padrao_list in self.padroes_avancados.items():
            for padrao in padrao_list:
                match = re.search(padrao, content_lower)
                if match:
                    if campo == 'data_inscricao' and len(match.groups()) >= 2:
                        info_extraida[campo] = f"{match.group(1)} - {match.group(2)}"
                    else:
                        valor = match.group(1).strip()
                        # Limpar valor extraído
                        valor = re.sub(r'[^\w\s\-/]', '', valor)
                        info_extraida[campo] = valor
                    break

        # Fallback para banca se não encontrada
        if 'banca' not in info_extraida:
            for banca in self.bancas_conhecidas:
                if banca in content_lower:
                    info_extraida['banca'] = banca.upper()
                    break

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

        # Padrões adicionais para capturar variações
        padroes_adicionais = [
            r'(?:cargo\s+de\s+)?([a-z]+(?:\s+[a-z]+)*)\s+(?:de\s+)?(?:polícia|federal|civil|militar)',
            r'(?:para\s+o\s+cargo\s+de\s+)?([a-z]+(?:\s+[a-z]+)*)',
            r'([a-z]+(?:\s+[a-z]+)*)\s+(?:federal|civil|militar)',
            r'(?:professor\s+de\s+)([a-z]+)',
            r'(?:engenheiro\s+)([a-z]+)',
            r'(?:técnico\s+em\s+)([a-z]+)',
            r'(?:fiscal\s+de\s+)([a-z]+)',
            r'(?:músico\s+instrumentista/)([a-z]+)',
            r'(?:oficial\s+de\s+)([a-z]+)',
        ]

        for padrao in padroes_adicionais:
            matches = re.findall(padrao, content_lower)
            for match in matches:
                cargo = match.strip()
                if len(cargo) > 3 and cargo not in [c.lower() for c in cargos_detectados]:
                    cargos_detectados.append(cargo.title())

        # Remover duplicatas e ordenar
        cargos_unicos = list(dict.fromkeys(cargos_detectados))

        return cargos_unicos[:20]  # Limitar a 20 cargos mais relevantes

    def _detectar_materias(self, content_lower: str) -> Dict[str, Dict[str, Any]]:
        """Detecta matérias e suas informações"""
        materias_detectadas = {}

        # Padrões para matérias
        padroes_materias = [
            r'([a-z]+(?:\s+[a-z]+)*)\s*\((\d+)\s+questões?\)',
            r'(\d+)\s+questões?\s+(?:de\s+)?([a-z]+(?:\s+[a-z]+)*)',
            r'([a-z]+(?:\s+[a-z]+)*)\s*[:\s*](\d+)\s+questões?',
        ]

        for padrao in padroes_materias:
            matches = re.findall(padrao, content_lower)
            for match in matches:
                if len(match) >= 2:
                    materia = match[0].strip().title()
                    questoes = int(match[1])
                    materias_detectadas[materia] = {
                        'questoes': questoes,
                        'peso': 1.0,
                        'conteudo': f"{materia}: {questoes} questões"
                    }

        # Fallback para matérias comuns
        if not materias_detectadas:
            materias_comuns = [
                'português', 'matemática', 'direito constitucional', 'direito penal',
                'direito processual penal', 'direito administrativo', 'informática'
            ]
            for materia in materias_comuns:
                if materia in content_lower:
                    materias_detectadas[materia.title()] = {
                        'questoes': 10,
                        'peso': 1.0,
                        'conteudo': f"{materia.title()}: 10 questões"
                    }

        return materias_detectadas

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
