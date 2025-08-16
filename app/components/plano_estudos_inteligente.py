"""
Plano de Estudos Inteligente - Agente Concurseiro v2.0
Sistema avançado de planejamento personalizado baseado em IA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
from typing import Dict, List, Tuple, Optional
import json

class PlanoEstudosInteligente:
    """Sistema inteligente de planejamento de estudos"""
    
    def __init__(self):
        self.perfis_estudo = {
            "Iniciante": {
                "horas_dia": 3,
                "dias_semana": 5,
                "intensidade": "Baixa",
                "foco_teoria": 70,
                "foco_pratica": 30,
                "revisoes_semana": 2
            },
            "Intermediário": {
                "horas_dia": 5,
                "dias_semana": 6,
                "intensidade": "Média",
                "foco_teoria": 60,
                "foco_pratica": 40,
                "revisoes_semana": 3
            },
            "Avançado": {
                "horas_dia": 7,
                "dias_semana": 6,
                "intensidade": "Alta",
                "foco_teoria": 50,
                "foco_pratica": 50,
                "revisoes_semana": 4
            },
            "Intensivo": {
                "horas_dia": 9,
                "dias_semana": 7,
                "intensidade": "Muito Alta",
                "foco_teoria": 40,
                "foco_pratica": 60,
                "revisoes_semana": 5
            }
        }
        
        self.metodologias = {
            "Pomodoro": {
                "descricao": "25 min estudo + 5 min pausa",
                "ciclos_hora": 2,
                "eficiencia": 85,
                "melhor_para": ["Concentração", "Disciplina"]
            },
            "Feynman": {
                "descricao": "Ensinar para aprender",
                "ciclos_hora": 1,
                "eficiencia": 90,
                "melhor_para": ["Compreensão", "Memorização"]
            },
            "Active Recall": {
                "descricao": "Recuperação ativa da memória",
                "ciclos_hora": 3,
                "eficiencia": 88,
                "melhor_para": ["Memorização", "Revisão"]
            },
            "Spaced Repetition": {
                "descricao": "Revisão espaçada no tempo",
                "ciclos_hora": 2,
                "eficiencia": 92,
                "melhor_para": ["Retenção", "Longo prazo"]
            }
        }
        
        self.tipos_atividade = {
            "Teoria": {
                "cor": "#3498db",
                "icon": "📚",
                "descricao": "Leitura e compreensão de conceitos"
            },
            "Exercícios": {
                "cor": "#e74c3c",
                "icon": "✏️",
                "descricao": "Resolução de questões práticas"
            },
            "Revisão": {
                "cor": "#f39c12",
                "icon": "🔄",
                "descricao": "Revisão de conteúdo estudado"
            },
            "Simulado": {
                "cor": "#9b59b6",
                "icon": "🎯",
                "descricao": "Simulados e provas práticas"
            },
            "Redação": {
                "cor": "#1abc9c",
                "icon": "✍️",
                "descricao": "Prática de redação e escrita"
            }
        }

    def analisar_perfil_usuario(self, dados_usuario: Dict) -> Dict:
        """Analisa perfil do usuário para personalizar plano"""
        # Dados básicos
        tempo_disponivel = dados_usuario.get('tempo_disponivel', 4)
        experiencia = dados_usuario.get('experiencia', 'Intermediário')
        data_prova = dados_usuario.get('data_prova')
        materias_dificuldade = dados_usuario.get('materias_dificuldade', {})
        
        # Calcula dias até a prova
        if data_prova:
            dias_restantes = (data_prova - datetime.now().date()).days
        else:
            dias_restantes = 90  # Padrão 3 meses
        
        # Determina perfil baseado no tempo disponível e experiência
        if tempo_disponivel <= 3:
            perfil_sugerido = "Iniciante"
        elif tempo_disponivel <= 5:
            perfil_sugerido = "Intermediário"
        elif tempo_disponivel <= 7:
            perfil_sugerido = "Avançado"
        else:
            perfil_sugerido = "Intensivo"
        
        # Ajusta baseado na experiência
        if experiencia == "Primeira vez" and perfil_sugerido != "Iniciante":
            perfil_sugerido = "Iniciante"
        elif experiencia == "Muito experiente" and perfil_sugerido == "Iniciante":
            perfil_sugerido = "Intermediário"
        
        analise = {
            "perfil_sugerido": perfil_sugerido,
            "dias_restantes": dias_restantes,
            "horas_totais": dias_restantes * tempo_disponivel,
            "urgencia": self._calcular_urgencia(dias_restantes),
            "materias_prioritarias": self._identificar_prioridades(materias_dificuldade),
            "metodologia_recomendada": self._recomendar_metodologia(experiencia, tempo_disponivel)
        }
        
        return analise

    def _calcular_urgencia(self, dias_restantes: int) -> str:
        """Calcula nível de urgência baseado nos dias restantes"""
        if dias_restantes <= 30:
            return "Crítica"
        elif dias_restantes <= 60:
            return "Alta"
        elif dias_restantes <= 120:
            return "Média"
        else:
            return "Baixa"

    def _identificar_prioridades(self, materias_dificuldade: Dict) -> List[str]:
        """Identifica matérias prioritárias baseado na dificuldade"""
        if not materias_dificuldade:
            return ["Português", "Direito Constitucional", "Conhecimentos Específicos"]
        
        # Ordena por dificuldade (maior dificuldade = maior prioridade)
        materias_ordenadas = sorted(
            materias_dificuldade.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [materia for materia, _ in materias_ordenadas[:5]]

    def _recomendar_metodologia(self, experiencia: str, tempo_disponivel: int) -> str:
        """Recomenda metodologia baseada no perfil"""
        if experiencia == "Primeira vez":
            return "Pomodoro"
        elif tempo_disponivel <= 3:
            return "Pomodoro"
        elif experiencia == "Muito experiente":
            return "Spaced Repetition"
        else:
            return "Active Recall"

    def gerar_plano_personalizado(self, analise_perfil: Dict, materias_edital: Dict) -> Dict:
        """Gera plano de estudos personalizado"""
        perfil = self.perfis_estudo[analise_perfil["perfil_sugerido"]]
        dias_restantes = analise_perfil["dias_restantes"]
        
        # Calcula distribuição de horas por matéria
        distribuicao_materias = self._calcular_distribuicao_materias(
            materias_edital,
            analise_perfil["materias_prioritarias"]
        )
        
        # Gera cronograma semanal
        cronograma_semanal = self._gerar_cronograma_semanal(
            perfil,
            distribuicao_materias,
            analise_perfil["metodologia_recomendada"]
        )
        
        # Gera cronograma mensal
        cronograma_mensal = self._gerar_cronograma_mensal(
            cronograma_semanal,
            dias_restantes
        )
        
        # Calcula metas e marcos
        metas = self._definir_metas(materias_edital, dias_restantes)
        
        plano = {
            "id": f"PLANO_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "data_criacao": datetime.now(),
            "perfil_usuario": analise_perfil,
            "configuracao": perfil,
            "distribuicao_materias": distribuicao_materias,
            "cronograma_semanal": cronograma_semanal,
            "cronograma_mensal": cronograma_mensal,
            "metas": metas,
            "metodologia": analise_perfil["metodologia_recomendada"]
        }
        
        return plano

    def _calcular_distribuicao_materias(self, materias_edital: Dict, prioritarias: List[str]) -> Dict:
        """Calcula distribuição de tempo por matéria"""
        distribuicao = {}
        
        # Se há informações do edital, usa os pesos
        if materias_edital:
            total_peso = sum(materias_edital.values())
            for materia, peso in materias_edital.items():
                # Aumenta peso das matérias prioritárias
                if materia in prioritarias:
                    peso_ajustado = peso * 1.3
                else:
                    peso_ajustado = peso
                
                distribuicao[materia] = (peso_ajustado / total_peso) * 100
        else:
            # Distribuição padrão
            materias_padrao = {
                "Português": 25,
                "Direito Constitucional": 20,
                "Direito Administrativo": 20,
                "Conhecimentos Específicos": 20,
                "Informática": 10,
                "Atualidades": 5
            }
            distribuicao = materias_padrao
        
        return distribuicao

    def _gerar_cronograma_semanal(self, perfil: Dict, distribuicao: Dict, metodologia: str) -> Dict:
        """Gera cronograma semanal detalhado"""
        dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        horas_dia = perfil["horas_dia"]
        dias_estudo = perfil["dias_semana"]
        
        cronograma = {}
        
        # Distribui matérias pelos dias
        materias_lista = list(distribuicao.keys())
        
        for i, dia in enumerate(dias_semana[:dias_estudo]):
            atividades = []
            horas_restantes = horas_dia
            
            # Manhã (40% do tempo) - Matérias mais difíceis
            horas_manha = int(horas_dia * 0.4)
            if i < len(materias_lista):
                materia_principal = materias_lista[i % len(materias_lista)]
                atividades.append({
                    "periodo": "Manhã",
                    "horario": "08:00-12:00",
                    "materia": materia_principal,
                    "tipo": "Teoria",
                    "horas": horas_manha,
                    "metodologia": metodologia
                })
                horas_restantes -= horas_manha
            
            # Tarde (40% do tempo) - Exercícios
            horas_tarde = int(horas_dia * 0.4)
            if horas_restantes >= horas_tarde:
                materia_exercicios = materias_lista[(i + 1) % len(materias_lista)]
                atividades.append({
                    "periodo": "Tarde",
                    "horario": "14:00-18:00",
                    "materia": materia_exercicios,
                    "tipo": "Exercícios",
                    "horas": horas_tarde,
                    "metodologia": metodologia
                })
                horas_restantes -= horas_tarde
            
            # Noite (20% do tempo) - Revisão
            if horas_restantes > 0:
                atividades.append({
                    "periodo": "Noite",
                    "horario": "19:00-21:00",
                    "materia": "Revisão Geral",
                    "tipo": "Revisão",
                    "horas": horas_restantes,
                    "metodologia": "Spaced Repetition"
                })
            
            cronograma[dia] = atividades
        
        # Dias de descanso/revisão
        for dia in dias_semana[dias_estudo:]:
            if dia == "Domingo":
                cronograma[dia] = [{
                    "periodo": "Livre",
                    "horario": "Flexível",
                    "materia": "Descanso",
                    "tipo": "Descanso",
                    "horas": 0,
                    "metodologia": "Relaxamento"
                }]
            else:
                cronograma[dia] = [{
                    "periodo": "Manhã",
                    "horario": "09:00-11:00",
                    "materia": "Revisão Livre",
                    "tipo": "Revisão",
                    "horas": 2,
                    "metodologia": "Active Recall"
                }]
        
        return cronograma

    def _gerar_cronograma_mensal(self, cronograma_semanal: Dict, dias_restantes: int) -> Dict:
        """Gera cronograma mensal baseado no semanal"""
        cronograma_mensal = {}
        
        # Calcula número de semanas
        semanas = min(dias_restantes // 7, 16)  # Máximo 4 meses
        
        for semana in range(1, semanas + 1):
            # Ajusta intensidade baseado na proximidade da prova
            if semana <= semanas * 0.3:  # Primeiras 30%
                fase = "Fundamentação"
                foco = "Teoria"
            elif semana <= semanas * 0.7:  # 30-70%
                fase = "Aprofundamento"
                foco = "Exercícios"
            else:  # Últimas 30%
                fase = "Revisão Final"
                foco = "Simulados"
            
            cronograma_mensal[f"Semana {semana}"] = {
                "fase": fase,
                "foco_principal": foco,
                "cronograma": cronograma_semanal.copy(),
                "objetivos": self._definir_objetivos_semana(fase, semana)
            }
        
        return cronograma_mensal

    def _definir_objetivos_semana(self, fase: str, semana: int) -> List[str]:
        """Define objetivos específicos para cada semana"""
        objetivos = {
            "Fundamentação": [
                f"Completar leitura básica de todas as matérias",
                f"Fazer resumos dos principais conceitos",
                f"Resolver 50 questões por matéria"
            ],
            "Aprofundamento": [
                f"Resolver 100+ questões por matéria",
                f"Fazer 2 simulados completos",
                f"Revisar pontos de maior dificuldade"
            ],
            "Revisão Final": [
                f"Fazer 1 simulado por dia",
                f"Revisar todos os resumos",
                f"Focar nas matérias com menor desempenho"
            ]
        }
        
        return objetivos.get(fase, ["Manter ritmo de estudos"])

    def _definir_metas(self, materias_edital: Dict, dias_restantes: int) -> Dict:
        """Define metas específicas e mensuráveis"""
        metas = {
            "curto_prazo": [],  # 1-2 semanas
            "medio_prazo": [],  # 1 mês
            "longo_prazo": []   # Até a prova
        }
        
        # Metas de curto prazo
        metas["curto_prazo"] = [
            "Estabelecer rotina diária de estudos",
            "Completar primeiro ciclo de todas as matérias",
            "Resolver 200 questões no total"
        ]
        
        # Metas de médio prazo
        metas["medio_prazo"] = [
            "Atingir 70% de acerto em simulados",
            "Completar revisão de todas as matérias",
            "Fazer 10 redações completas"
        ]
        
        # Metas de longo prazo
        if dias_restantes <= 60:
            metas["longo_prazo"] = [
                "Atingir 80% de acerto em simulados",
                "Dominar pontos mais cobrados",
                "Estar preparado para a prova"
            ]
        else:
            metas["longo_prazo"] = [
                "Atingir 85% de acerto em simulados",
                "Dominar todas as matérias",
                "Ter segurança total para a prova"
            ]
        
        return metas

    def acompanhar_progresso(self, plano: Dict, atividades_realizadas: List[Dict]) -> Dict:
        """Acompanha progresso do plano de estudos"""
        # Calcula estatísticas de cumprimento
        total_atividades = self._contar_atividades_planejadas(plano)
        atividades_concluidas = len(atividades_realizadas)
        
        # Calcula progresso por matéria
        progresso_materias = {}
        for atividade in atividades_realizadas:
            materia = atividade.get("materia", "Desconhecida")
            if materia not in progresso_materias:
                progresso_materias[materia] = {"horas": 0, "atividades": 0}
            
            progresso_materias[materia]["horas"] += atividade.get("horas", 0)
            progresso_materias[materia]["atividades"] += 1
        
        # Calcula aderência ao cronograma
        aderencia = (atividades_concluidas / total_atividades) * 100 if total_atividades > 0 else 0
        
        # Identifica tendências
        tendencias = self._analisar_tendencias(atividades_realizadas)
        
        acompanhamento = {
            "data_analise": datetime.now(),
            "progresso_geral": aderencia,
            "atividades_concluidas": atividades_concluidas,
            "atividades_planejadas": total_atividades,
            "progresso_materias": progresso_materias,
            "tendencias": tendencias,
            "recomendacoes": self._gerar_recomendacoes(aderencia, progresso_materias)
        }
        
        return acompanhamento

    def _contar_atividades_planejadas(self, plano: Dict) -> int:
        """Conta total de atividades planejadas"""
        total = 0
        cronograma_semanal = plano.get("cronograma_semanal", {})
        
        for dia, atividades in cronograma_semanal.items():
            total += len([a for a in atividades if a["tipo"] != "Descanso"])
        
        return total * 4  # Aproximadamente 4 semanas por mês

    def _analisar_tendencias(self, atividades: List[Dict]) -> Dict:
        """Analisa tendências no comportamento de estudo"""
        if len(atividades) < 7:
            return {"erro": "Dados insuficientes para análise"}
        
        # Analisa últimos 7 dias
        atividades_recentes = atividades[-7:]
        
        # Calcula médias
        horas_por_dia = sum(a.get("horas", 0) for a in atividades_recentes) / 7
        
        # Identifica padrões
        dias_semana_ativo = {}
        for atividade in atividades_recentes:
            dia = atividade.get("dia_semana", "Desconhecido")
            dias_semana_ativo[dia] = dias_semana_ativo.get(dia, 0) + 1
        
        melhor_dia = max(dias_semana_ativo.items(), key=lambda x: x[1])[0] if dias_semana_ativo else "N/A"
        
        return {
            "horas_media_dia": horas_por_dia,
            "melhor_dia_semana": melhor_dia,
            "consistencia": len(atividades_recentes) / 7,
            "tendencia": "Crescente" if len(atividades_recentes) >= 5 else "Irregular"
        }

    def _gerar_recomendacoes(self, aderencia: float, progresso_materias: Dict) -> List[str]:
        """Gera recomendações baseadas no progresso"""
        recomendacoes = []
        
        if aderencia < 50:
            recomendacoes.append("🚨 Aderência baixa! Revise seu cronograma e reduza a carga se necessário.")
        elif aderencia < 70:
            recomendacoes.append("⚠️ Tente manter mais consistência no cronograma.")
        else:
            recomendacoes.append("✅ Excelente aderência! Continue assim!")
        
        # Analisa progresso por matéria
        if progresso_materias:
            materias_atrasadas = [
                materia for materia, dados in progresso_materias.items()
                if dados["horas"] < 10  # Menos de 10 horas estudadas
            ]
            
            if materias_atrasadas:
                recomendacoes.append(f"📚 Foque mais em: {', '.join(materias_atrasadas[:3])}")
        
        return recomendacoes

def render_plano_estudos_inteligente():
    """Renderiza o sistema de plano de estudos inteligente"""
    st.header("🧠 Plano de Estudos Inteligente")
    
    sistema = PlanoEstudosInteligente()
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Criar Plano",
        "📅 Meu Cronograma",
        "📊 Acompanhamento",
        "⚙️ Configurações"
    ])
    
    with tab1:
        st.subheader("🎯 Criar Plano Personalizado")
        
        # Formulário de perfil
        with st.form("perfil_usuario"):
            st.write("### 👤 Seu Perfil de Estudos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                tempo_disponivel = st.slider(
                    "⏰ Horas disponíveis por dia:",
                    min_value=1,
                    max_value=12,
                    value=4,
                    help="Quantas horas você pode dedicar aos estudos por dia?"
                )
                
                experiencia = st.selectbox(
                    "📚 Sua experiência com concursos:",
                    options=["Primeira vez", "Já fiz alguns", "Experiente", "Muito experiente"]
                )
                
                data_prova = st.date_input(
                    "📅 Data da prova:",
                    value=datetime.now().date() + timedelta(days=90),
                    min_value=datetime.now().date()
                )
            
            with col2:
                st.write("**🎯 Dificuldade por matéria (1-5):**")
                
                materias_dificuldade = {}
                materias_principais = [
                    "Português", "Direito Constitucional", "Direito Administrativo",
                    "Conhecimentos Específicos", "Informática", "Atualidades"
                ]
                
                for materia in materias_principais:
                    dificuldade = st.slider(
                        f"{materia}:",
                        min_value=1,
                        max_value=5,
                        value=3,
                        key=f"dif_{materia}"
                    )
                    materias_dificuldade[materia] = dificuldade
            
            # Preferências adicionais
            st.write("### ⚙️ Preferências de Estudo")
            
            col_pref1, col_pref2 = st.columns(2)
            
            with col_pref1:
                periodo_preferido = st.selectbox(
                    "🌅 Período preferido:",
                    options=["Manhã", "Tarde", "Noite", "Flexível"]
                )
                
                tipo_conteudo = st.selectbox(
                    "📖 Preferência de conteúdo:",
                    options=["Mais teoria", "Equilibrado", "Mais prática"]
                )
            
            with col_pref2:
                dias_descanso = st.multiselect(
                    "🛌 Dias de descanso:",
                    options=["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
                    default=["Domingo"]
                )
                
                incluir_redacao = st.checkbox("✍️ Incluir prática de redação", value=True)
            
            submitted = st.form_submit_button("🚀 Gerar Plano Inteligente", type="primary")
            
            if submitted:
                with st.spinner("🤖 Analisando seu perfil e gerando plano personalizado..."):
                    # Dados do usuário
                    dados_usuario = {
                        "tempo_disponivel": tempo_disponivel,
                        "experiencia": experiencia,
                        "data_prova": data_prova,
                        "materias_dificuldade": materias_dificuldade,
                        "periodo_preferido": periodo_preferido,
                        "tipo_conteudo": tipo_conteudo,
                        "dias_descanso": dias_descanso,
                        "incluir_redacao": incluir_redacao
                    }
                    
                    # Analisa perfil
                    analise_perfil = sistema.analisar_perfil_usuario(dados_usuario)
                    
                    # Gera plano
                    materias_edital = {materia: 5 - dif for materia, dif in materias_dificuldade.items()}
                    plano = sistema.gerar_plano_personalizado(analise_perfil, materias_edital)
                    
                    # Salva no session state
                    st.session_state.plano_atual = plano
                    st.session_state.dados_usuario = dados_usuario
                    
                    st.success("✅ Plano gerado com sucesso!")
                    
                    # Resumo do plano
                    st.subheader("📋 Resumo do Seu Plano")
                    
                    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
                    
                    with col_res1:
                        st.metric("👤 Perfil", analise_perfil["perfil_sugerido"])
                    
                    with col_res2:
                        st.metric("📅 Dias Restantes", analise_perfil["dias_restantes"])
                    
                    with col_res3:
                        st.metric("⏰ Horas Totais", f"{analise_perfil['horas_totais']}h")
                    
                    with col_res4:
                        urgencia_color = {
                            "Crítica": "🔴",
                            "Alta": "🟠", 
                            "Média": "🟡",
                            "Baixa": "🟢"
                        }
                        st.metric("⚡ Urgência", f"{urgencia_color.get(analise_perfil['urgencia'], '⚪')} {analise_perfil['urgência']}")
                    
                    # Distribuição por matéria
                    fig_distribuicao = px.pie(
                        values=list(plano["distribuicao_materias"].values()),
                        names=list(plano["distribuicao_materias"].keys()),
                        title="📊 Distribuição de Tempo por Matéria"
                    )
                    st.plotly_chart(fig_distribuicao, use_container_width=True)
                    
                    # Metodologia recomendada
                    metodologia = sistema.metodologias[plano["metodologia"]]
                    st.info(f"**🎯 Metodologia Recomendada:** {plano['metodologia']}")
                    st.write(f"• **Descrição:** {metodologia['descricao']}")
                    st.write(f"• **Eficiência:** {metodologia['eficiencia']}%")
                    st.write(f"• **Melhor para:** {', '.join(metodologia['melhor_para'])}")
                    
                    st.info("💡 Vá para a aba 'Meu Cronograma' para ver o planejamento detalhado!")
    
    with tab2:
        st.subheader("📅 Meu Cronograma de Estudos")
        
        if 'plano_atual' not in st.session_state:
            st.warning("⚠️ Primeiro crie seu plano na aba 'Criar Plano'")
        else:
            plano = st.session_state.plano_atual
            
            # Seletor de visualização
            tipo_visualizacao = st.selectbox(
                "📊 Tipo de visualização:",
                options=["Cronograma Semanal", "Cronograma Mensal", "Metas e Objetivos"]
            )
            
            if tipo_visualizacao == "Cronograma Semanal":
                st.subheader("📅 Cronograma Semanal Detalhado")
                
                cronograma = plano["cronograma_semanal"]
                
                for dia, atividades in cronograma.items():
                    with st.expander(f"📅 {dia}", expanded=True):
                        if atividades[0]["tipo"] == "Descanso":
                            st.info("🛌 Dia de descanso - Aproveite para relaxar!")
                        else:
                            for atividade in atividades:
                                tipo_info = sistema.tipos_atividade.get(atividade["tipo"], {})
                                
                                col_ativ1, col_ativ2, col_ativ3 = st.columns([2, 1, 1])
                                
                                with col_ativ1:
                                    st.write(f"**{tipo_info.get('icon', '📚')} {atividade['materia']}**")
                                    st.write(f"_{tipo_info.get('descricao', 'Atividade de estudo')}_")
                                
                                with col_ativ2:
                                    st.write(f"**⏰ {atividade['horario']}**")
                                    st.write(f"**🕐 {atividade['horas']}h**")
                                
                                with col_ativ3:
                                    st.write(f"**🎯 {atividade['tipo']}**")
                                    st.write(f"**📖 {atividade['metodologia']}**")
                                
                                # Botão para marcar como concluído
                                if st.button(f"✅ Concluir", key=f"concluir_{dia}_{atividade['materia']}"):
                                    # Adiciona atividade ao histórico
                                    if 'atividades_realizadas' not in st.session_state:
                                        st.session_state.atividades_realizadas = []
                                    
                                    atividade_realizada = atividade.copy()
                                    atividade_realizada["data_conclusao"] = datetime.now()
                                    atividade_realizada["dia_semana"] = dia
                                    
                                    st.session_state.atividades_realizadas.append(atividade_realizada)
                                    st.success(f"✅ Atividade '{atividade['materia']}' marcada como concluída!")
                                    st.rerun()
            
            elif tipo_visualizacao == "Cronograma Mensal":
                st.subheader("📅 Cronograma Mensal")
                
                cronograma_mensal = plano["cronograma_mensal"]
                
                for semana, info in cronograma_mensal.items():
                    with st.expander(f"📅 {semana} - {info['fase']}", expanded=False):
                        col_sem1, col_sem2 = st.columns(2)
                        
                        with col_sem1:
                            st.write(f"**🎯 Foco Principal:** {info['foco_principal']}")
                            st.write(f"**📋 Fase:** {info['fase']}")
                        
                        with col_sem2:
                            st.write("**🎯 Objetivos da Semana:**")
                            for objetivo in info['objetivos']:
                                st.write(f"• {objetivo}")
            
            else:  # Metas e Objetivos
                st.subheader("🎯 Metas e Objetivos")
                
                metas = plano["metas"]
                
                col_meta1, col_meta2, col_meta3 = st.columns(3)
                
                with col_meta1:
                    st.success("**🎯 Curto Prazo (1-2 semanas)**")
                    for meta in metas["curto_prazo"]:
                        st.write(f"• {meta}")
                
                with col_meta2:
                    st.info("**🎯 Médio Prazo (1 mês)**")
                    for meta in metas["medio_prazo"]:
                        st.write(f"• {meta}")
                
                with col_meta3:
                    st.warning("**🎯 Longo Prazo (Até a prova)**")
                    for meta in metas["longo_prazo"]:
                        st.write(f"• {meta}")
    
    with tab3:
        st.subheader("📊 Acompanhamento de Progresso")
        
        if 'plano_atual' not in st.session_state:
            st.warning("⚠️ Primeiro crie seu plano na aba 'Criar Plano'")
        elif 'atividades_realizadas' not in st.session_state or not st.session_state.atividades_realizadas:
            st.info("📊 Comece a marcar atividades como concluídas para ver seu progresso!")
        else:
            plano = st.session_state.plano_atual
            atividades_realizadas = st.session_state.atividades_realizadas
            
            # Gera acompanhamento
            acompanhamento = sistema.acompanhar_progresso(plano, atividades_realizadas)
            
            # Métricas principais
            col_prog1, col_prog2, col_prog3, col_prog4 = st.columns(4)
            
            with col_prog1:
                st.metric("📊 Progresso Geral", f"{acompanhamento['progresso_geral']:.1f}%")
            
            with col_prog2:
                st.metric("✅ Atividades Concluídas", acompanhamento['atividades_concluidas'])
            
            with col_prog3:
                st.metric("📋 Atividades Planejadas", acompanhamento['atividades_planejadas'])
            
            with col_prog4:
                tendencia = acompanhamento['tendencias'].get('tendencia', 'N/A')
                st.metric("📈 Tendência", tendencia)
            
            # Progresso por matéria
            if acompanhamento['progresso_materias']:
                st.subheader("📚 Progresso por Matéria")
                
                df_progresso = pd.DataFrame([
                    {
                        "Matéria": materia,
                        "Horas Estudadas": dados["horas"],
                        "Atividades Concluídas": dados["atividades"]
                    }
                    for materia, dados in acompanhamento['progresso_materias'].items()
                ])
                
                fig_progresso = px.bar(
                    df_progresso,
                    x="Matéria",
                    y="Horas Estudadas",
                    title="📊 Horas de Estudo por Matéria",
                    color="Horas Estudadas",
                    color_continuous_scale="viridis"
                )
                st.plotly_chart(fig_progresso, use_container_width=True)
                
                st.dataframe(df_progresso, use_container_width=True)
            
            # Tendências e análises
            st.subheader("📈 Análise de Tendências")
            
            tendencias = acompanhamento['tendencias']
            if 'erro' not in tendencias:
                col_tend1, col_tend2 = st.columns(2)
                
                with col_tend1:
                    st.metric("⏰ Média Horas/Dia", f"{tendencias['horas_media_dia']:.1f}h")
                    st.metric("📅 Melhor Dia", tendencias['melhor_dia_semana'])
                
                with col_tend2:
                    st.metric("🎯 Consistência", f"{tendencias['consistencia']:.1%}")
                    st.metric("📊 Tendência", tendencias['tendencia'])
            
            # Recomendações
            st.subheader("💡 Recomendações Personalizadas")
            
            for recomendacao in acompanhamento['recomendacoes']:
                if "🚨" in recomendacao:
                    st.error(recomendacao)
                elif "⚠️" in recomendacao:
                    st.warning(recomendacao)
                else:
                    st.success(recomendacao)
    
    with tab4:
        st.subheader("⚙️ Configurações do Plano")
        
        if 'plano_atual' not in st.session_state:
            st.warning("⚠️ Primeiro crie seu plano na aba 'Criar Plano'")
        else:
            # Informações do plano atual
            plano = st.session_state.plano_atual
            
            st.write("### 📋 Informações do Plano Atual")
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.info(f"**📅 Criado em:** {plano['data_criacao'].strftime('%d/%m/%Y %H:%M')}")
                st.info(f"**👤 Perfil:** {plano['perfil_usuario']['perfil_sugerido']}")
                st.info(f"**🎯 Metodologia:** {plano['metodologia']}")
            
            with col_info2:
                st.info(f"**📅 Dias Restantes:** {plano['perfil_usuario']['dias_restantes']}")
                st.info(f"**⏰ Horas Totais:** {plano['perfil_usuario']['horas_totais']}h")
                st.info(f"**⚡ Urgência:** {plano['perfil_usuario']['urgencia']}")
            
            # Configurações avançadas
            st.write("### ⚙️ Configurações Avançadas")
            
            with st.expander("🔧 Ajustar Configurações"):
                # Permite ajustar algumas configurações
                novo_tempo = st.slider(
                    "⏰ Ajustar horas por dia:",
                    min_value=1,
                    max_value=12,
                    value=plano['configuracao']['horas_dia']
                )
                
                nova_metodologia = st.selectbox(
                    "📖 Alterar metodologia:",
                    options=list(sistema.metodologias.keys()),
                    index=list(sistema.metodologias.keys()).index(plano['metodologia'])
                )
                
                if st.button("💾 Salvar Alterações"):
                    # Atualiza configurações
                    plano['configuracao']['horas_dia'] = novo_tempo
                    plano['metodologia'] = nova_metodologia
                    st.session_state.plano_atual = plano
                    
                    st.success("✅ Configurações atualizadas!")
                    st.rerun()
            
            # Exportar/Importar plano
            st.write("### 📤 Exportar/Importar Plano")
            
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                if st.button("📤 Exportar Plano (JSON)"):
                    plano_json = json.dumps(plano, default=str, indent=2)
                    st.download_button(
                        label="💾 Baixar Plano",
                        data=plano_json,
                        file_name=f"plano_estudos_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
            
            with col_exp2:
                uploaded_plano = st.file_uploader(
                    "📥 Importar Plano",
                    type=['json'],
                    help="Importe um plano exportado anteriormente"
                )
                
                if uploaded_plano is not None:
                    try:
                        plano_importado = json.loads(uploaded_plano.getvalue())
                        st.session_state.plano_atual = plano_importado
                        st.success("✅ Plano importado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao importar plano: {str(e)}")
            
            # Reset do plano
            st.write("### 🔄 Reset do Plano")
            
            if st.button("🗑️ Limpar Todos os Dados", type="secondary"):
                # Confirma reset
                if st.button("⚠️ Confirmar Reset (IRREVERSÍVEL)", type="secondary"):
                    # Limpa session state
                    keys_to_clear = ['plano_atual', 'dados_usuario', 'atividades_realizadas']
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                    
                    st.success("✅ Dados limpos! Crie um novo plano na primeira aba.")
                    st.rerun()