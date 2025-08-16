"""
Sistema de Simulados Reais - Agente Concurseiro v2.0
Simulados por banca, cargo e correção automática com estatísticas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Optional
import json
import time

class SimuladosSystem:
    """Sistema completo de simulados para concursos"""
    
    def __init__(self):
        self.bancas_questoes = {
            "CESPE/CEBRASPE": {
                "tipo": "Certo/Errado",
                "caracteristicas": ["Textos longos", "Interpretação", "Pegadinhas sutis"],
                "tempo_medio": 3,  # minutos por questão
                "dificuldade": "Alta"
            },
            "FCC": {
                "tipo": "Múltipla Escolha",
                "caracteristicas": ["Objetivas", "Técnicas", "5 alternativas"],
                "tempo_medio": 2.5,
                "dificuldade": "Média-Alta"
            },
            "FGV": {
                "tipo": "Múltipla Escolha",
                "caracteristicas": ["Analíticas", "Contextualizadas", "5 alternativas"],
                "tempo_medio": 3.5,
                "dificuldade": "Alta"
            },
            "VUNESP": {
                "tipo": "Múltipla Escolha",
                "caracteristicas": ["Práticas", "Diretas", "5 alternativas"],
                "tempo_medio": 2,
                "dificuldade": "Média"
            }
        }
        
        self.cargos_areas = {
            "Analista Judiciário": {
                "areas": ["Direito", "Administração", "Português", "Informática"],
                "nivel": "Superior",
                "materias_peso": {
                    "Português": 25,
                    "Direito Constitucional": 20,
                    "Direito Administrativo": 20,
                    "Conhecimentos Específicos": 20,
                    "Informática": 15
                }
            },
            "Técnico Judiciário": {
                "areas": ["Direito Básico", "Administração", "Português", "Informática"],
                "nivel": "Médio",
                "materias_peso": {
                    "Português": 30,
                    "Direito Constitucional": 15,
                    "Direito Administrativo": 15,
                    "Conhecimentos Específicos": 25,
                    "Informática": 15
                }
            },
            "Auditor Fiscal": {
                "areas": ["Contabilidade", "Direito Tributário", "Administração", "Português"],
                "nivel": "Superior",
                "materias_peso": {
                    "Português": 15,
                    "Contabilidade": 30,
                    "Direito Tributário": 25,
                    "Direito Constitucional": 15,
                    "Conhecimentos Específicos": 15
                }
            },
            "Professor": {
                "areas": ["Educação", "Português", "Conhecimentos Específicos"],
                "nivel": "Superior",
                "materias_peso": {
                    "Português": 25,
                    "Conhecimentos Pedagógicos": 35,
                    "Conhecimentos Específicos": 40
                }
            }
        }
        
        # Banco de questões por matéria e banca
        self.questoes_banco = self._inicializar_banco_questoes()
        
        # Histórico de simulados (simulado em memória)
        if 'historico_simulados' not in st.session_state:
            st.session_state.historico_simulados = []

    def _inicializar_banco_questoes(self) -> Dict:
        """Inicializa banco de questões por matéria e banca"""
        return {
            "Português": {
                "CESPE/CEBRASPE": [
                    {
                        "id": 1,
                        "enunciado": "A concordância verbal está correta na frase: 'Fazem dois anos que não o vejo.'",
                        "tipo": "Certo/Errado",
                        "resposta_correta": "Errado",
                        "explicacao": "O verbo 'fazer' no sentido de tempo decorrido é impessoal, devendo ficar no singular: 'Faz dois anos'.",
                        "dificuldade": "Média",
                        "assunto": "Concordância Verbal"
                    },
                    {
                        "id": 2,
                        "enunciado": "No texto, o uso da vírgula em 'O candidato, que estudou muito, foi aprovado' é obrigatório.",
                        "tipo": "Certo/Errado",
                        "resposta_correta": "Certo",
                        "explicacao": "A vírgula é obrigatória para isolar a oração subordinada adjetiva explicativa.",
                        "dificuldade": "Fácil",
                        "assunto": "Pontuação"
                    }
                ],
                "FCC": [
                    {
                        "id": 3,
                        "enunciado": "Assinale a alternativa em que a regência verbal está INCORRETA:",
                        "tipo": "Múltipla Escolha",
                        "alternativas": [
                            "Aspirou ao cargo de diretor.",
                            "Assistiu o filme ontem.",
                            "Obedeceu às normas da empresa.",
                            "Procedeu à leitura do documento.",
                            "Visou ao alvo com precisão."
                        ],
                        "resposta_correta": "B",
                        "explicacao": "O verbo 'assistir' no sentido de 'ver' exige preposição 'a': 'Assistiu ao filme'.",
                        "dificuldade": "Média",
                        "assunto": "Regência Verbal"
                    }
                ]
            },
            "Direito Constitucional": {
                "CESPE/CEBRASPE": [
                    {
                        "id": 4,
                        "enunciado": "Segundo a Constituição Federal, todos são iguais perante a lei, sem distinção de qualquer natureza.",
                        "tipo": "Certo/Errado",
                        "resposta_correta": "Certo",
                        "explicacao": "Art. 5º, caput da CF/88 estabelece o princípio da igualdade formal.",
                        "dificuldade": "Fácil",
                        "assunto": "Direitos Fundamentais"
                    }
                ],
                "FCC": [
                    {
                        "id": 5,
                        "enunciado": "São direitos sociais previstos na Constituição Federal:",
                        "tipo": "Múltipla Escolha",
                        "alternativas": [
                            "Educação, saúde, alimentação e trabalho.",
                            "Vida, liberdade, igualdade e segurança.",
                            "Propriedade, herança, sucessão e moradia.",
                            "Voto, elegibilidade, petição e associação.",
                            "Intimidade, honra, imagem e domicílio."
                        ],
                        "resposta_correta": "A",
                        "explicacao": "Art. 6º da CF/88 lista os direitos sociais, incluindo educação, saúde, alimentação e trabalho.",
                        "dificuldade": "Fácil",
                        "assunto": "Direitos Sociais"
                    }
                ]
            },
            "Informática": {
                "FCC": [
                    {
                        "id": 6,
                        "enunciado": "No Microsoft Word, a combinação de teclas Ctrl+Z tem a função de:",
                        "tipo": "Múltipla Escolha",
                        "alternativas": [
                            "Salvar o documento.",
                            "Desfazer a última ação.",
                            "Copiar o texto selecionado.",
                            "Fechar o documento.",
                            "Imprimir o documento."
                        ],
                        "resposta_correta": "B",
                        "explicacao": "Ctrl+Z é o atalho padrão para desfazer a última ação realizada.",
                        "dificuldade": "Fácil",
                        "assunto": "Microsoft Office"
                    }
                ]
            }
        }

    def gerar_simulado(self, banca: str, cargo: str, num_questoes: int = 20) -> Dict:
        """Gera simulado personalizado baseado na banca e cargo"""
        if cargo not in self.cargos_areas:
            return {"erro": "Cargo não encontrado"}
        
        info_cargo = self.cargos_areas[cargo]
        materias_peso = info_cargo["materias_peso"]
        
        # Calcula número de questões por matéria baseado no peso
        questoes_por_materia = {}
        questoes_restantes = num_questoes
        
        for materia, peso in materias_peso.items():
            num_questoes_materia = max(1, int((peso / 100) * num_questoes))
            questoes_por_materia[materia] = min(num_questoes_materia, questoes_restantes)
            questoes_restantes -= questoes_por_materia[materia]
        
        # Gera questões
        questoes_simulado = []
        questao_id = 1
        
        for materia, num_questoes_mat in questoes_por_materia.items():
            if materia in self.questoes_banco and banca in self.questoes_banco[materia]:
                questoes_disponiveis = self.questoes_banco[materia][banca]
                
                # Seleciona questões aleatoriamente
                questoes_selecionadas = random.sample(
                    questoes_disponiveis,
                    min(num_questoes_mat, len(questoes_disponiveis))
                )
                
                for questao in questoes_selecionadas:
                    questao_simulado = questao.copy()
                    questao_simulado["numero"] = questao_id
                    questao_simulado["materia"] = materia
                    questoes_simulado.append(questao_simulado)
                    questao_id += 1
            
            # Se não há questões suficientes, gera questões genéricas
            while len([q for q in questoes_simulado if q["materia"] == materia]) < num_questoes_mat:
                questao_generica = self._gerar_questao_generica(materia, banca, questao_id)
                questao_generica["materia"] = materia
                questoes_simulado.append(questao_generica)
                questao_id += 1
        
        # Embaralha questões
        random.shuffle(questoes_simulado)
        
        # Calcula tempo total
        tempo_total = len(questoes_simulado) * self.bancas_questoes[banca]["tempo_medio"]
        
        simulado = {
            "id": f"SIM_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "banca": banca,
            "cargo": cargo,
            "questoes": questoes_simulado,
            "tempo_total": tempo_total,
            "data_criacao": datetime.now(),
            "materias_peso": materias_peso
        }
        
        return simulado

    def _gerar_questao_generica(self, materia: str, banca: str, numero: int) -> Dict:
        """Gera questão genérica quando não há questões específicas"""
        tipo_questao = self.bancas_questoes[banca]["tipo"]
        
        questoes_genericas = {
            "Português": {
                "enunciado": f"Questão {numero} de Português - {materia}",
                "assunto": "Gramática"
            },
            "Direito Constitucional": {
                "enunciado": f"Questão {numero} sobre princípios constitucionais",
                "assunto": "Princípios"
            },
            "Direito Administrativo": {
                "enunciado": f"Questão {numero} sobre atos administrativos",
                "assunto": "Atos Administrativos"
            },
            "Informática": {
                "enunciado": f"Questão {numero} sobre conceitos de informática",
                "assunto": "Conceitos Básicos"
            },
            "Conhecimentos Específicos": {
                "enunciado": f"Questão {numero} de conhecimentos específicos do cargo",
                "assunto": "Específicos"
            }
        }
        
        info_questao = questoes_genericas.get(materia, {
            "enunciado": f"Questão {numero} de {materia}",
            "assunto": "Geral"
        })
        
        if tipo_questao == "Certo/Errado":
            return {
                "id": f"GEN_{numero}",
                "numero": numero,
                "enunciado": info_questao["enunciado"],
                "tipo": "Certo/Errado",
                "resposta_correta": random.choice(["Certo", "Errado"]),
                "explicacao": "Esta é uma questão de exemplo para demonstração.",
                "dificuldade": "Média",
                "assunto": info_questao["assunto"]
            }
        else:
            return {
                "id": f"GEN_{numero}",
                "numero": numero,
                "enunciado": info_questao["enunciado"],
                "tipo": "Múltipla Escolha",
                "alternativas": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D", "Alternativa E"],
                "resposta_correta": random.choice(["A", "B", "C", "D", "E"]),
                "explicacao": "Esta é uma questão de exemplo para demonstração.",
                "dificuldade": "Média",
                "assunto": info_questao["assunto"]
            }

    def executar_simulado(self, simulado: Dict) -> Dict:
        """Executa simulado interativo"""
        if 'simulado_atual' not in st.session_state:
            st.session_state.simulado_atual = simulado
            st.session_state.respostas_simulado = {}
            st.session_state.tempo_inicio = datetime.now()
            st.session_state.questao_atual = 0
        
        return st.session_state.simulado_atual

    def corrigir_simulado(self, simulado: Dict, respostas: Dict) -> Dict:
        """Corrige simulado e gera estatísticas"""
        questoes = simulado["questoes"]
        total_questoes = len(questoes)
        acertos = 0
        acertos_por_materia = {}
        tempo_total = (datetime.now() - st.session_state.get('tempo_inicio', datetime.now())).total_seconds() / 60
        
        # Inicializa contadores por matéria
        for questao in questoes:
            materia = questao["materia"]
            if materia not in acertos_por_materia:
                acertos_por_materia[materia] = {"acertos": 0, "total": 0}
            acertos_por_materia[materia]["total"] += 1
        
        # Corrige questões
        questoes_corrigidas = []
        for questao in questoes:
            numero = questao["numero"]
            resposta_usuario = respostas.get(numero, "")
            resposta_correta = questao["resposta_correta"]
            
            acertou = resposta_usuario == resposta_correta
            if acertou:
                acertos += 1
                acertos_por_materia[questao["materia"]]["acertos"] += 1
            
            questao_corrigida = questao.copy()
            questao_corrigida["resposta_usuario"] = resposta_usuario
            questao_corrigida["acertou"] = acertou
            questoes_corrigidas.append(questao_corrigida)
        
        # Calcula estatísticas
        percentual_acerto = (acertos / total_questoes) * 100
        
        # Desempenho por matéria
        desempenho_materias = {}
        for materia, dados in acertos_por_materia.items():
            if dados["total"] > 0:
                percentual = (dados["acertos"] / dados["total"]) * 100
                desempenho_materias[materia] = {
                    "acertos": dados["acertos"],
                    "total": dados["total"],
                    "percentual": percentual
                }
        
        resultado = {
            "simulado_id": simulado["id"],
            "data_realizacao": datetime.now(),
            "banca": simulado["banca"],
            "cargo": simulado["cargo"],
            "total_questoes": total_questoes,
            "acertos": acertos,
            "erros": total_questoes - acertos,
            "percentual_acerto": percentual_acerto,
            "tempo_realizado": tempo_total,
            "tempo_previsto": simulado["tempo_total"],
            "desempenho_materias": desempenho_materias,
            "questoes_corrigidas": questoes_corrigidas,
            "aprovado": percentual_acerto >= 60  # Critério básico de aprovação
        }
        
        # Salva no histórico
        st.session_state.historico_simulados.append(resultado)
        
        return resultado

    def gerar_relatorio_desempenho(self, historico: List[Dict]) -> Dict:
        """Gera relatório de desempenho baseado no histórico"""
        if not historico:
            return {"erro": "Nenhum simulado realizado"}
        
        # Estatísticas gerais
        total_simulados = len(historico)
        media_acertos = sum(s["percentual_acerto"] for s in historico) / total_simulados
        melhor_desempenho = max(historico, key=lambda x: x["percentual_acerto"])
        pior_desempenho = min(historico, key=lambda x: x["percentual_acerto"])
        
        # Evolução temporal
        historico_ordenado = sorted(historico, key=lambda x: x["data_realizacao"])
        evolucao = [s["percentual_acerto"] for s in historico_ordenado]
        
        # Desempenho por matéria (média)
        materias_desempenho = {}
        for simulado in historico:
            for materia, dados in simulado["desempenho_materias"].items():
                if materia not in materias_desempenho:
                    materias_desempenho[materia] = []
                materias_desempenho[materia].append(dados["percentual"])
        
        media_por_materia = {
            materia: sum(percentuais) / len(percentuais)
            for materia, percentuais in materias_desempenho.items()
        }
        
        # Bancas mais realizadas
        bancas_count = {}
        for simulado in historico:
            banca = simulado["banca"]
            bancas_count[banca] = bancas_count.get(banca, 0) + 1
        
        relatorio = {
            "total_simulados": total_simulados,
            "media_acertos": media_acertos,
            "melhor_desempenho": melhor_desempenho,
            "pior_desempenho": pior_desempenho,
            "evolucao_temporal": evolucao,
            "media_por_materia": media_por_materia,
            "bancas_realizadas": bancas_count,
            "aprovacoes": sum(1 for s in historico if s["aprovado"]),
            "taxa_aprovacao": (sum(1 for s in historico if s["aprovado"]) / total_simulados) * 100
        }
        
        return relatorio

def render_simulados_system():
    """Renderiza o sistema completo de simulados"""
    st.header("🎯 Sistema de Simulados Reais")
    
    sistema = SimuladosSystem()
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "🆕 Novo Simulado",
        "📊 Realizar Simulado",
        "📈 Histórico e Estatísticas",
        "🎯 Análise de Desempenho"
    ])
    
    with tab1:
        st.subheader("🆕 Criar Novo Simulado")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            banca_selecionada = st.selectbox(
                "🏛️ Selecione a banca:",
                options=list(sistema.bancas_questoes.keys())
            )
        
        with col2:
            cargo_selecionado = st.selectbox(
                "💼 Selecione o cargo:",
                options=list(sistema.cargos_areas.keys())
            )
        
        with col3:
            num_questoes = st.slider(
                "📝 Número de questões:",
                min_value=10,
                max_value=50,
                value=20,
                step=5
            )
        
        # Informações da banca e cargo
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.info(f"**🏛️ {banca_selecionada}**")
            info_banca = sistema.bancas_questoes[banca_selecionada]
            st.write(f"• **Tipo:** {info_banca['tipo']}")
            st.write(f"• **Tempo médio:** {info_banca['tempo_medio']} min/questão")
            st.write(f"• **Dificuldade:** {info_banca['dificuldade']}")
        
        with col_info2:
            st.info(f"**💼 {cargo_selecionado}**")
            info_cargo = sistema.cargos_areas[cargo_selecionado]
            st.write(f"• **Nível:** {info_cargo['nivel']}")
            st.write("• **Matérias principais:**")
            for materia, peso in list(info_cargo['materias_peso'].items())[:3]:
                st.write(f"  - {materia}: {peso}%")
        
        if st.button("🎯 Gerar Simulado", type="primary"):
            with st.spinner("🔄 Gerando simulado personalizado..."):
                simulado = sistema.gerar_simulado(banca_selecionada, cargo_selecionado, num_questoes)
                
                if "erro" not in simulado:
                    st.session_state.simulado_gerado = simulado
                    st.success("✅ Simulado gerado com sucesso!")
                    
                    # Resumo do simulado
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("📝 Questões", len(simulado["questoes"]))
                    
                    with col2:
                        st.metric("⏰ Tempo Total", f"{simulado['tempo_total']:.0f} min")
                    
                    with col3:
                        st.metric("🏛️ Banca", simulado["banca"])
                    
                    with col4:
                        st.metric("💼 Cargo", simulado["cargo"])
                    
                    # Distribuição por matéria
                    materias_count = {}
                    for questao in simulado["questoes"]:
                        materia = questao["materia"]
                        materias_count[materia] = materias_count.get(materia, 0) + 1
                    
                    fig_distribuicao = px.pie(
                        values=list(materias_count.values()),
                        names=list(materias_count.keys()),
                        title="📊 Distribuição de Questões por Matéria"
                    )
                    st.plotly_chart(fig_distribuicao, use_container_width=True)
                    
                    st.info("💡 Vá para a aba 'Realizar Simulado' para começar!")
                
                else:
                    st.error(f"❌ {simulado['erro']}")
    
    with tab2:
        st.subheader("📊 Realizar Simulado")
        
        if 'simulado_gerado' not in st.session_state:
            st.warning("⚠️ Primeiro gere um simulado na aba 'Novo Simulado'")
        else:
            simulado = st.session_state.simulado_gerado
            
            # Inicializa simulado se necessário
            if 'simulado_iniciado' not in st.session_state:
                st.session_state.simulado_iniciado = False
                st.session_state.respostas_simulado = {}
                st.session_state.questao_atual = 0
            
            if not st.session_state.simulado_iniciado:
                # Tela de início
                st.info(f"**🎯 Simulado: {simulado['banca']} - {simulado['cargo']}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📝 Questões", len(simulado["questoes"]))
                with col2:
                    st.metric("⏰ Tempo", f"{simulado['tempo_total']:.0f} min")
                with col3:
                    st.metric("🎯 Tipo", sistema.bancas_questoes[simulado['banca']]['tipo'])
                
                st.write("### 📋 Instruções:")
                st.write("• Leia cada questão com atenção")
                st.write("• Marque apenas uma alternativa por questão")
                st.write("• Você pode navegar entre as questões")
                st.write("• Ao final, clique em 'Finalizar Simulado'")
                
                if st.button("🚀 Iniciar Simulado", type="primary"):
                    st.session_state.simulado_iniciado = True
                    st.session_state.tempo_inicio = datetime.now()
                    st.rerun()
            
            else:
                # Simulado em andamento
                questoes = simulado["questoes"]
                questao_atual = st.session_state.questao_atual
                
                # Barra de progresso
                progresso = (questao_atual + 1) / len(questoes)
                st.progress(progresso)
                st.write(f"Questão {questao_atual + 1} de {len(questoes)}")
                
                # Tempo decorrido
                tempo_decorrido = (datetime.now() - st.session_state.tempo_inicio).total_seconds() / 60
                col_tempo1, col_tempo2 = st.columns(2)
                with col_tempo1:
                    st.metric("⏰ Tempo Decorrido", f"{tempo_decorrido:.1f} min")
                with col_tempo2:
                    st.metric("⏰ Tempo Restante", f"{simulado['tempo_total'] - tempo_decorrido:.1f} min")
                
                # Questão atual
                questao = questoes[questao_atual]
                
                st.write(f"### 📚 {questao['materia']} - {questao['assunto']}")
                st.write(f"**Questão {questao['numero']}:** {questao['enunciado']}")
                
                # Opções de resposta
                if questao["tipo"] == "Certo/Errado":
                    resposta = st.radio(
                        "Selecione sua resposta:",
                        options=["Certo", "Errado"],
                        key=f"questao_{questao['numero']}",
                        index=None
                    )
                else:
                    resposta = st.radio(
                        "Selecione sua resposta:",
                        options=["A", "B", "C", "D", "E"],
                        format_func=lambda x: f"{x}) {questao['alternativas'][ord(x) - ord('A')]}",
                        key=f"questao_{questao['numero']}",
                        index=None
                    )
                
                # Salva resposta
                if resposta:
                    st.session_state.respostas_simulado[questao['numero']] = resposta
                
                # Navegação
                col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
                
                with col_nav1:
                    if questao_atual > 0:
                        if st.button("⬅️ Anterior"):
                            st.session_state.questao_atual -= 1
                            st.rerun()
                
                with col_nav3:
                    if questao_atual < len(questoes) - 1:
                        if st.button("➡️ Próxima"):
                            st.session_state.questao_atual += 1
                            st.rerun()
                    else:
                        if st.button("✅ Finalizar Simulado", type="primary"):
                            # Corrige simulado
                            resultado = sistema.corrigir_simulado(
                                simulado,
                                st.session_state.respostas_simulado
                            )
                            
                            st.session_state.resultado_simulado = resultado
                            st.session_state.simulado_finalizado = True
                            st.rerun()
                
                # Mapa de questões
                with st.expander("🗺️ Mapa de Questões"):
                    cols = st.columns(10)
                    for i, q in enumerate(questoes):
                        col_idx = i % 10
                        with cols[col_idx]:
                            status = "✅" if q['numero'] in st.session_state.respostas_simulado else "⭕"
                            if st.button(f"{status} {q['numero']}", key=f"nav_{i}"):
                                st.session_state.questao_atual = i
                                st.rerun()
            
            # Resultado do simulado
            if st.session_state.get('simulado_finalizado', False):
                resultado = st.session_state.resultado_simulado
                
                st.success("🎉 Simulado Finalizado!")
                
                # Métricas principais
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📊 Nota Final", f"{resultado['percentual_acerto']:.1f}%")
                
                with col2:
                    st.metric("✅ Acertos", f"{resultado['acertos']}/{resultado['total_questoes']}")
                
                with col3:
                    st.metric("⏰ Tempo", f"{resultado['tempo_realizado']:.1f} min")
                
                with col4:
                    status = "✅ Aprovado" if resultado['aprovado'] else "❌ Reprovado"
                    st.metric("🎯 Status", status)
                
                # Desempenho por matéria
                st.subheader("📚 Desempenho por Matéria")
                
                df_materias = pd.DataFrame([
                    {
                        "Matéria": materia,
                        "Acertos": dados["acertos"],
                        "Total": dados["total"],
                        "Percentual": dados["percentual"]
                    }
                    for materia, dados in resultado["desempenho_materias"].items()
                ])
                
                fig_materias = px.bar(
                    df_materias,
                    x="Matéria",
                    y="Percentual",
                    title="📊 Desempenho por Matéria (%)",
                    color="Percentual",
                    color_continuous_scale="RdYlGn"
                )
                st.plotly_chart(fig_materias, use_container_width=True)
                
                # Gabarito detalhado
                with st.expander("📋 Ver Gabarito Detalhado"):
                    for questao in resultado["questoes_corrigidas"]:
                        status_icon = "✅" if questao["acertou"] else "❌"
                        
                        st.write(f"**{status_icon} Questão {questao['numero']} - {questao['materia']}**")
                        st.write(f"**Enunciado:** {questao['enunciado']}")
                        
                        if questao["tipo"] == "Múltipla Escolha":
                            st.write("**Alternativas:**")
                            for i, alt in enumerate(questao["alternativas"]):
                                letra = chr(ord('A') + i)
                                st.write(f"{letra}) {alt}")
                        
                        col_resp1, col_resp2 = st.columns(2)
                        with col_resp1:
                            st.write(f"**Sua resposta:** {questao.get('resposta_usuario', 'Não respondida')}")
                        with col_resp2:
                            st.write(f"**Resposta correta:** {questao['resposta_correta']}")
                        
                        st.write(f"**Explicação:** {questao['explicacao']}")
                        st.divider()
                
                # Botão para novo simulado
                if st.button("🔄 Fazer Novo Simulado"):
                    # Limpa session state
                    keys_to_clear = [
                        'simulado_iniciado', 'respostas_simulado', 'questao_atual',
                        'tempo_inicio', 'resultado_simulado', 'simulado_finalizado'
                    ]
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
    
    with tab3:
        st.subheader("📈 Histórico de Simulados")
        
        historico = st.session_state.get('historico_simulados', [])
        
        if not historico:
            st.info("📊 Nenhum simulado realizado ainda. Faça seu primeiro simulado!")
        else:
            # Tabela de histórico
            df_historico = pd.DataFrame([
                {
                    "Data": s["data_realizacao"].strftime("%d/%m/%Y %H:%M"),
                    "Banca": s["banca"],
                    "Cargo": s["cargo"],
                    "Questões": s["total_questoes"],
                    "Acertos": s["acertos"],
                    "Nota (%)": f"{s['percentual_acerto']:.1f}%",
                    "Tempo (min)": f"{s['tempo_realizado']:.1f}",
                    "Status": "✅ Aprovado" if s["aprovado"] else "❌ Reprovado"
                }
                for s in historico
            ])
            
            st.dataframe(df_historico, use_container_width=True)
            
            # Gráfico de evolução
            if len(historico) > 1:
                fig_evolucao = px.line(
                    x=range(1, len(historico) + 1),
                    y=[s["percentual_acerto"] for s in historico],
                    title="📈 Evolução do Desempenho",
                    labels={"x": "Simulado", "y": "Nota (%)"}
                )
                fig_evolucao.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="Linha de Aprovação (60%)")
                st.plotly_chart(fig_evolucao, use_container_width=True)
    
    with tab4:
        st.subheader("🎯 Análise de Desempenho")
        
        historico = st.session_state.get('historico_simulados', [])
        
        if not historico:
            st.info("📊 Realize alguns simulados para ver sua análise de desempenho!")
        else:
            relatorio = sistema.gerar_relatorio_desempenho(historico)
            
            # Métricas gerais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Simulados Realizados", relatorio["total_simulados"])
            
            with col2:
                st.metric("📈 Média Geral", f"{relatorio['media_acertos']:.1f}%")
            
            with col3:
                st.metric("✅ Aprovações", relatorio["aprovacoes"])
            
            with col4:
                st.metric("🎯 Taxa de Aprovação", f"{relatorio['taxa_aprovacao']:.1f}%")
            
            # Melhor e pior desempenho
            col_best, col_worst = st.columns(2)
            
            with col_best:
                st.success("🏆 **Melhor Desempenho**")
                melhor = relatorio["melhor_desempenho"]
                st.write(f"• **Nota:** {melhor['percentual_acerto']:.1f}%")
                st.write(f"• **Banca:** {melhor['banca']}")
                st.write(f"• **Cargo:** {melhor['cargo']}")
                st.write(f"• **Data:** {melhor['data_realizacao'].strftime('%d/%m/%Y')}")
            
            with col_worst:
                st.error("📉 **Pior Desempenho**")
                pior = relatorio["pior_desempenho"]
                st.write(f"• **Nota:** {pior['percentual_acerto']:.1f}%")
                st.write(f"• **Banca:** {pior['banca']}")
                st.write(f"• **Cargo:** {pior['cargo']}")
                st.write(f"• **Data:** {pior['data_realizacao'].strftime('%d/%m/%Y')}")
            
            # Desempenho por matéria
            st.subheader("📚 Desempenho Médio por Matéria")
            
            if relatorio["media_por_materia"]:
                df_materias_media = pd.DataFrame([
                    {"Matéria": materia, "Média (%)": media}
                    for materia, media in relatorio["media_por_materia"].items()
                ])
                
                fig_materias_media = px.bar(
                    df_materias_media,
                    x="Matéria",
                    y="Média (%)",
                    title="📊 Desempenho Médio por Matéria",
                    color="Média (%)",
                    color_continuous_scale="RdYlGn"
                )
                st.plotly_chart(fig_materias_media, use_container_width=True)
            
            # Bancas mais realizadas
            st.subheader("🏛️ Bancas Mais Realizadas")
            
            if relatorio["bancas_realizadas"]:
                fig_bancas = px.pie(
                    values=list(relatorio["bancas_realizadas"].values()),
                    names=list(relatorio["bancas_realizadas"].keys()),
                    title="📊 Distribuição de Simulados por Banca"
                )
                st.plotly_chart(fig_bancas, use_container_width=True)
            
            # Recomendações
            st.subheader("💡 Recomendações de Estudo")
            
            # Identifica matérias com menor desempenho
            if relatorio["media_por_materia"]:
                materias_ordenadas = sorted(
                    relatorio["media_por_materia"].items(),
                    key=lambda x: x[1]
                )
                
                st.write("**🎯 Priorize o estudo das seguintes matérias:**")
                for materia, media in materias_ordenadas[:3]:
                    if media < 60:
                        st.error(f"• **{materia}**: {media:.1f}% - Precisa de atenção especial")
                    elif media < 70:
                        st.warning(f"• **{materia}**: {media:.1f}% - Pode melhorar")
                    else:
                        st.success(f"• **{materia}**: {media:.1f}% - Bom desempenho")
            
            # Dicas baseadas no desempenho
            if relatorio["taxa_aprovacao"] < 50:
                st.info("💡 **Dica:** Sua taxa de aprovação está baixa. Foque em revisar os conceitos básicos e pratique mais simulados.")
            elif relatorio["taxa_aprovacao"] < 80:
                st.info("💡 **Dica:** Você está no caminho certo! Continue praticando e foque nas matérias com menor desempenho.")
            else:
                st.success("💡 **Parabéns!** Excelente desempenho! Continue mantendo a consistência nos estudos.")