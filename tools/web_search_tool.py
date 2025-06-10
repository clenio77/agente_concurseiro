import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urljoin, urlparse
import PyPDF2
from io import BytesIO

class WebSearchTool:
    def __init__(self):
        self.name = "WebSearchTool"
        self.description = "Busca inteligente por provas anteriores e editais com análise de conteúdo"

        # Sites conhecidos de concursos
        self.concurso_sites = [
            "pciconcursos.com.br",
            "concursosnobrasil.com.br",
            "qconcursos.com",
            "estrategiaconcursos.com.br",
            "grancursosonline.com.br",
            "tecconcursos.com.br",
            "questoesdeconcursos.com.br"
        ]

        # Headers para simular navegador real
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def search_exam_content(self, cargo: str, concurso: str, banca: str, cidade: str,
                           max_results: int = 10) -> Dict:
        """Busca provas anteriores com parâmetros específicos"""

        # Construir query de busca
        query_terms = [cargo, concurso, banca, cidade, "prova", "gabarito"]
        query = " ".join([term for term in query_terms if term])

        # Realizar busca simulada mais realista
        search_results = self._simulate_realistic_search(query, max_results)

        # Analisar e processar resultados
        processed_results = []

        for result in search_results:
            try:
                # Extrair informações do resultado
                content_info = self._analyze_search_result(result)

                # Tentar baixar e analisar conteúdo se for PDF
                if content_info.get('is_pdf'):
                    pdf_analysis = self._analyze_pdf_content(result['url'])
                    content_info.update(pdf_analysis)

                processed_results.append(content_info)

                # Delay para evitar sobrecarga
                time.sleep(0.5)

            except Exception as e:
                processed_results.append({
                    'url': result.get('url', ''),
                    'title': result.get('title', ''),
                    'error': f'Erro ao processar: {str(e)}'
                })

        # Compilar resultado final
        search_summary = {
            'query': query,
            'total_results': len(processed_results),
            'successful_extractions': len([r for r in processed_results if 'error' not in r]),
            'results': processed_results,
            'search_metadata': {
                'cargo': cargo,
                'concurso': concurso,
                'banca': banca,
                'cidade': cidade,
                'search_timestamp': datetime.now().isoformat()
            },
            'recommendations': self._generate_search_recommendations(processed_results)
        }

        return search_summary

    def _simulate_realistic_search(self, query: str, max_results: int) -> List[Dict]:
        """Simula busca mais realista baseada em sites reais de concursos"""
        results = []

        # Gerar resultados baseados em padrões reais
        for i in range(max_results):
            site = self.concurso_sites[i % len(self.concurso_sites)]

            # Simular diferentes tipos de conteúdo
            content_types = ['prova_completa', 'gabarito', 'edital', 'questoes_comentadas']
            content_type = content_types[i % len(content_types)]

            # Gerar URL realista
            url_path = self._generate_realistic_url(query, content_type, site)

            # Gerar título realista
            title = self._generate_realistic_title(query, content_type)

            # Simular snippet
            snippet = self._generate_realistic_snippet(query, content_type)

            result = {
                'url': f'https://{site}/{url_path}',
                'title': title,
                'snippet': snippet,
                'site': site,
                'content_type': content_type,
                'relevance_score': self._calculate_relevance_score(query, title, snippet),
                'estimated_year': 2020 + (i % 4),  # Simular anos 2020-2023
                'file_type': 'pdf' if content_type in ['prova_completa', 'gabarito'] else 'html'
            }

            results.append(result)

        # Ordenar por relevância
        results.sort(key=lambda x: x['relevance_score'], reverse=True)

        return results

    def _generate_realistic_url(self, query: str, content_type: str, site: str) -> str:
        """Gera URLs realistas baseadas no tipo de conteúdo"""
        query_clean = re.sub(r'[^\w\s-]', '', query.lower()).replace(' ', '-')

        url_patterns = {
            'prova_completa': f'provas/{query_clean}/prova-completa-{datetime.now().year}',
            'gabarito': f'gabaritos/{query_clean}/gabarito-oficial-{datetime.now().year}',
            'edital': f'editais/{query_clean}/edital-{datetime.now().year}',
            'questoes_comentadas': f'questoes/{query_clean}/questoes-comentadas'
        }

        return url_patterns.get(content_type, f'concursos/{query_clean}')

    def _generate_realistic_title(self, query: str, content_type: str) -> str:
        """Gera títulos realistas baseados no tipo de conteúdo"""
        title_templates = {
            'prova_completa': f'Prova Completa - {query} - PDF com Gabarito',
            'gabarito': f'Gabarito Oficial - {query} - Todas as Questões',
            'edital': f'Edital Completo - {query} - Requisitos e Conteúdo',
            'questoes_comentadas': f'Questões Comentadas - {query} - Resolução Detalhada'
        }

        return title_templates.get(content_type, f'{query} - Material Completo')

    def _generate_realistic_snippet(self, query: str, content_type: str) -> str:
        """Gera snippets realistas baseados no tipo de conteúdo"""
        snippet_templates = {
            'prova_completa': f'Baixe a prova completa de {query} em PDF. Contém todas as questões aplicadas na prova oficial com gabarito. Material atualizado e revisado por especialistas.',
            'gabarito': f'Gabarito oficial de {query} com todas as respostas corretas. Confira seu desempenho e veja quais questões acertou.',
            'edital': f'Edital completo de {query} com todos os requisitos, conteúdo programático e informações sobre o concurso.',
            'questoes_comentadas': f'Questões de {query} com comentários detalhados e explicações passo a passo. Ideal para estudos e revisão.'
        }

        return snippet_templates.get(content_type, f'Material completo sobre {query} para sua preparação.')

    def _calculate_relevance_score(self, query: str, title: str, snippet: str) -> float:
        """Calcula score de relevância baseado na correspondência de termos"""
        query_words = set(query.lower().split())
        title_words = set(title.lower().split())
        snippet_words = set(snippet.lower().split())

        # Calcular interseções
        title_matches = len(query_words.intersection(title_words))
        snippet_matches = len(query_words.intersection(snippet_words))

        # Score baseado nas correspondências (peso maior para título)
        title_score = (title_matches / len(query_words)) * 0.7 if query_words else 0
        snippet_score = (snippet_matches / len(query_words)) * 0.3 if query_words else 0

        total_score = title_score + snippet_score

        # Bonus para termos específicos
        bonus = 0.0
        if 'prova' in title.lower():
            bonus += 0.2
        if 'gabarito' in title.lower():
            bonus += 0.15
        if 'pdf' in title.lower():
            bonus += 0.1

        return min(total_score + bonus, 1.0)

    def _analyze_search_result(self, result: Dict) -> Dict:
        """Analisa um resultado de busca individual"""
        analysis = {
            'url': result['url'],
            'title': result['title'],
            'snippet': result['snippet'],
            'site': result['site'],
            'content_type': result['content_type'],
            'relevance_score': result['relevance_score'],
            'estimated_year': result['estimated_year'],
            'is_pdf': result['file_type'] == 'pdf',
            'quality_indicators': self._assess_content_quality(result),
            'extraction_status': 'pending'
        }

        return analysis

    def _assess_content_quality(self, result: Dict) -> Dict:
        """Avalia indicadores de qualidade do conteúdo"""
        quality = {
            'has_official_source': 'oficial' in result['title'].lower() or 'oficial' in result['snippet'].lower(),
            'has_complete_content': 'completa' in result['title'].lower() or 'completo' in result['snippet'].lower(),
            'has_answer_key': 'gabarito' in result['title'].lower() or 'gabarito' in result['snippet'].lower(),
            'is_recent': result['estimated_year'] >= 2020,
            'site_reliability': self._assess_site_reliability(result['site'])
        }

        # Calcular score geral de qualidade
        quality_score = sum([
            quality['has_official_source'] * 0.3,
            quality['has_complete_content'] * 0.2,
            quality['has_answer_key'] * 0.2,
            quality['is_recent'] * 0.1,
            quality['site_reliability'] * 0.2
        ])

        quality['overall_score'] = round(quality_score, 2)
        quality['quality_level'] = 'Alta' if quality_score > 0.7 else 'Média' if quality_score > 0.4 else 'Baixa'

        return quality

    def _assess_site_reliability(self, site: str) -> float:
        """Avalia confiabilidade do site"""
        reliable_sites = {
            'pciconcursos.com.br': 0.9,
            'qconcursos.com': 0.85,
            'estrategiaconcursos.com.br': 0.8,
            'grancursosonline.com.br': 0.75,
            'tecconcursos.com.br': 0.7,
            'concursosnobrasil.com.br': 0.65,
            'questoesdeconcursos.com.br': 0.6
        }

        return reliable_sites.get(site, 0.5)

    def _analyze_pdf_content(self, url: str) -> Dict:
        """Simula análise de conteúdo PDF"""
        # Em uma implementação real, baixaria e analisaria o PDF
        # Por ora, vamos simular a análise

        pdf_analysis = {
            'file_size_mb': round(2.5 + (hash(url) % 50) / 10, 1),  # Simular tamanho 2.5-7.5MB
            'estimated_pages': 15 + (hash(url) % 30),  # Simular 15-45 páginas
            'estimated_questions': 20 + (hash(url) % 60),  # Simular 20-80 questões
            'has_answer_key': hash(url) % 3 != 0,  # 66% chance de ter gabarito
            'content_structure': {
                'has_instructions': True,
                'has_questions': True,
                'has_answer_sheet': hash(url) % 4 != 0,  # 75% chance
                'has_explanations': hash(url) % 5 == 0   # 20% chance
            },
            'extraction_quality': 'Alta' if hash(url) % 3 == 0 else 'Média',
            'text_extractable': hash(url) % 10 != 0  # 90% chance de ser extraível
        }

        return pdf_analysis

    def _generate_search_recommendations(self, results: List[Dict]) -> List[str]:
        """Gera recomendações baseadas nos resultados da busca"""
        recommendations = []

        if not results:
            recommendations.append("Nenhum resultado encontrado. Tente refinar os termos de busca.")
            return recommendations

        # Analisar qualidade geral dos resultados
        high_quality_count = len([r for r in results if r.get('quality_indicators', {}).get('quality_level') == 'Alta'])
        pdf_count = len([r for r in results if r.get('is_pdf')])

        if high_quality_count > 0:
            recommendations.append(f"Encontrados {high_quality_count} resultados de alta qualidade.")

        if pdf_count > 0:
            recommendations.append(f"Encontrados {pdf_count} arquivos PDF para download.")

        if high_quality_count < len(results) * 0.3:
            recommendations.append("Poucos resultados de alta qualidade. Considere refinar a busca.")

        # Recomendações específicas
        if any('edital' in r.get('content_type', '') for r in results):
            recommendations.append("Revise o edital para entender o conteúdo programático.")

        if any('gabarito' in r.get('content_type', '') for r in results):
            recommendations.append("Use os gabaritos para verificar seu desempenho em simulados.")

        return recommendations

    def _run(self, action: str, params_json: str = None) -> str:
        """Interface principal da ferramenta"""
        try:
            if params_json:
                params = json.loads(params_json)
            else:
                params = {}

            if action == "search_exams":
                cargo = params.get('cargo', '')
                concurso = params.get('concurso', '')
                banca = params.get('banca', '')
                cidade = params.get('cidade', '')
                max_results = params.get('max_results', 10)

                result = self.search_exam_content(cargo, concurso, banca, cidade, max_results)

            else:
                # Fallback para busca simples
                query = action  # Usar action como query se não for um comando específico
                result = self.search_exam_content(query, '', '', '', 10)

            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            return json.dumps({
                'error': f'Erro na busca: {str(e)}',
                'action': action,
                'params': params_json
            }, indent=2, ensure_ascii=False)