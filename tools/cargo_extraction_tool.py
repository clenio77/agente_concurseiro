import re
from typing import List

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

# Lista de cargos conhecidos para comparação
CARGOS_CONHECIDOS = [
    'analista em controle interno', 'arquiteto', 'assistente social',
    'auditor fiscal tributário', 'bibliotecário', 'biólogo',
    'conservador-restaurador', 'contador', 'engenheiro agrônomo',
    'engenheiro ambiental', 'engenheiro civil', 'engenheiro elétrico',
    'engenheiro de segurança do trabalho', 'farmacêutico-bioquímico',
    'fonoaudiólogo', 'geógrafo', 'médico do trabalho',
    'médico veterinário', 'nutricionista', 'profissional de educação física',
    'programador visual', 'psicólogo', 'zootecnista', 'procurador municipal',
    'analista pedagógico', 'inspetor escolar', 'intérprete educacional',
    'professor de arte', 'professor de história', 'professor de inglês',
    'professor de libras', 'professor de língua portuguesa', 'professor de matemática',
    'fiscal de abastecimento', 'fiscal de obras', 'fiscal sanitário/alimentos',
    'fiscal sanitário/enfermagem', 'fiscal sanitário/farmácia',
    'profissional de apoio escolar', 'técnico em agropecuária',
    'técnico em alimentos', 'técnico em enfermagem', 'agente da autoridade de trânsito',
    'assistente técnico de som', 'desenhista', 'fiscal de defesa do consumidor',
    'fiscal de transportes', 'oficial administrativo', 'agente de apoio operacional',
    'agente de segurança patrimonial', 'operador de teleatendimento'
]

# Regex para extrair possíveis cargos
PADROES_CARGOS = [
    r'cargo\s+(?:de\s+)?([A-ZÁÉÍÓÚÂÊÔÃÕÇa-záéíóúâêôãõç ]{3,50})',
    r'([A-ZÁÉÍÓÚÂÊÔÃÕÇa-záéíóúâêôãõç ]{3,50})\s+(?:federal|estadual|municipal)',
    r'([A-ZÁÉÍÓÚÂÊÔÃÕÇa-záéíóúâêôãõç ]{3,50})\s+(?:de\s+)?polícia',
    r'([A-ZÁÉÍÓÚÂÊÔÃÕÇa-záéíóúâêôãõç ]{3,50})\s+(?:agente|escrivão|delegado|perito|papiloscopista)',
    r'cargo\s+de\s+([A-ZÁÉÍÓÚÂÊÔÃÕÇa-záéíóúâêôãõç ]{3,50})',
]

def extract_cargos_from_pdf(file_path: str) -> List[str]:
    """
    Extrai nomes de cargos de um arquivo PDF usando pdfplumber e regex.
    Retorna lista de cargos únicos encontrados.
    """
    if pdfplumber is None:
        raise ImportError("pdfplumber não está instalado. Instale com 'pip install pdfplumber'.")
    cargos_encontrados = set()
    try:
        with pdfplumber.open(file_path) as pdf:
            texto = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        return [f"Erro ao extrair texto do PDF: {str(e)}"]
    texto_lower = texto.lower()
    # Busca por cargos conhecidos
    for cargo in CARGOS_CONHECIDOS:
        if cargo in texto_lower:
            cargos_encontrados.add(cargo.title())
    # Busca por padrões regex
    for padrao in PADROES_CARGOS:
        for match in re.findall(padrao, texto, re.IGNORECASE):
            if isinstance(match, tuple):
                match = match[0]
            cargo = match.strip().title()
            if len(cargo) > 2 and cargo not in cargos_encontrados:
                cargos_encontrados.add(cargo)
    return sorted(cargos_encontrados)
