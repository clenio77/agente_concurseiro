import streamlit as st
import json
import time
from datetime import datetime, timedelta
from tools.question_api_tool import QuestionAPITool
from utils.config import load_config

def render_simulado_page():
    st.title("Simulado Interativo")
    
    # Carregar configuração
    config = load_config()
    
    # Inicializar ferramenta de questões
    question_tool = QuestionAPITool()
    
    # Verificar se há um simulado em andamento
    if "current_quiz" not in st.session_state:
        st.session_state.current_quiz = None
        st.session_state.quiz_answers = {}
        st.session_state.quiz_start_time = None
        st.session_state.quiz_submitted = False
        st.session_state.quiz_results = None
    
    # Sidebar para configurações do simulado
    with st.sidebar:
        st.header("Configurações do Simulado")
        
        # Opções de matérias
        all_subjects = ["Português", "Matemática", "Direito Constitucional", 
                       "Direito Administrativo", "Raciocínio Lógico", 
                       "Informática", "Conhecimentos Específicos"]
        
        selected_subjects = st.multiselect(
            "Selecione as matérias",
            options=all_subjects,
            default=["Português", "Matemática", "Conhecimentos Específicos"]
        )
        
        # Opções de dificuldade
        difficulty = st.select_slider(
            "Dificuldade",
            options=["Fácil", "Média", "Difícil"],
            value="Média"
        )
        
        # Mapeamento de dificuldade
        difficulty_map = {
            "Fácil": "easy",
            "Média": "medium",
            "Difícil": "hard"
        }
        
        # Número de questões
        num_questions = st.slider(
            "Número de questões",
            min_value=5,
            max_value=30,
            value=10,
            step=5
        )
        
        # Banca examinadora
        banca = st.selectbox(
            "Banca examinadora",
            options=["CESPE", "FGV", "VUNESP", "CEBRASPE", "IBFC"],
            index=0
        )
        
        # Botão para iniciar simulado
        start_button = st.button("Iniciar Simulado")
        
        if start_button:
            with st.spinner("Gerando simulado..."):
                # Converter dificuldade
                diff_param = difficulty_map.get(difficulty, "medium")
                
                # Buscar questões
                params = {
                    "subjects": selected_subjects,
                    "difficulty": diff_param,
                    "count": num_questions,
                    "banca": banca
                }
                
                # Gerar simulado
                result = question_tool._run("fetch_questions", json.dumps(params))
                questions = json.loads(result)
                
                # Criar quiz
                quiz = {
                    "id": f"quiz_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "title": f"Simulado {difficulty} - {banca}",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "questions": questions,
                    "settings": {
                        "subjects": selected_subjects,
                        "difficulty": difficulty,
                        "banca": banca,
                        "num_questions": num_questions
                    }
                }
                
                # Armazenar quiz na sessão
                st.session_state.current_quiz = quiz
                st.session_state.quiz_answers = {}
                st.session_state.quiz_start_time = datetime.now()
                st.session_state.quiz_submitted = False
                st.session_state.quiz_results = None
                
                # Recarregar página
                st.experimental_rerun()
    
    # Exibir simulado em andamento
    if st.session_state.current_quiz and not st.session_state.quiz_submitted:
        quiz = st.session_state.current_quiz
        
        # Calcular tempo decorrido
        elapsed_time = datetime.now() - st.session_state.quiz_start_time
        elapsed_minutes = int(elapsed_time.total_seconds() // 60)
        elapsed_seconds = int(elapsed_time.total_seconds() % 60)
        
        # Exibir informações do simulado
        st.subheader(quiz["title"])
        st.write(f"Data: {quiz['date']}")
        st.write(f"Matérias: {', '.join(quiz['settings']['subjects'])}")
        st.write(f"Dificuldade: {quiz['settings']['difficulty']}")
        st.write(f"Banca: {quiz['settings']['banca']}")
        
        # Exibir tempo decorrido
        st.info(f"Tempo decorrido: {elapsed_minutes:02d}:{elapsed_seconds:02d}")
        
        # Formulário para respostas
        with st.form("quiz_form"):
            # Exibir cada questão
            for i, question in enumerate(quiz["questions"]):
                st.markdown(f"### Questão {i+1}")
                st.markdown(f"**{question['text']}**")
                st.markdown(f"*{question['subject']} - {question['banca']} ({question['year']})*")
                
                # Opções de resposta
                options = {opt["id"]: opt["text"] for opt in question["options"]}
                
                # ID da questão
                question_id = question["id"]
                
                # Obter resposta atual (se existir)
                current_answer = st.session_state.quiz_answers.get(question_id, "")
                
                # Exibir opções
                selected_option = st.radio(
                    f"Selecione uma opção (Questão {i+1}):",
                    options=list(options.keys()),
                    format_func=lambda x: f"{x}) {options[x]}",
                    key=f"q_{question_id}",
                    index=None if not current_answer else list(options.keys()).index(current_answer)
                )
                
                # Armazenar resposta
                if selected_option:
                    st.session_state.quiz_answers[question_id] = selected_option
                
                st.markdown("---")
            
            # Botões de ação
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Finalizar Simulado")
            with col2:
                save_button = st.form_submit_button("Salvar Progresso")
            
            if submit_button:
                # Verificar se todas as questões foram respondidas
                if len(st.session_state.quiz_answers) < len(quiz["questions"]):
                    st.warning(f"Atenção: Você respondeu apenas {len(st.session_state.quiz_answers)} de {len(quiz['questions'])} questões. Tem certeza que deseja finalizar?")
                    confirm = st.button("Confirmar Finalização")
                    if confirm:
                        st.session_state.quiz_submitted = True
                else:
                    st.session_state.quiz_submitted = True
            
            if save_button:
                st.success("Progresso salvo com sucesso!")
        
        # Se o quiz foi finalizado, processar resultados
        if st.session_state.quiz_submitted:
            with st.spinner("Processando resultados..."):
                # Preparar parâmetros
                params = {
                    "quiz_id": quiz["id"],
                    "answers": st.session_state.quiz_answers
                }
                
                # Submeter respostas
                result = question_tool._run("submit_answers", json.dumps(params))
                st.session_state.quiz_results = json.loads(result)
                
                # Recarregar página
                st.experimental_rerun()
    
    # Exibir resultados do simulado
    elif st.session_state.quiz_submitted and st.session_state.quiz_results:
        quiz = st.session_state.current_quiz
        results = st.session_state.quiz_results
        
        # Calcular tempo total
        total_time = datetime.now() - st.session_state.quiz_start_time
        total_minutes = int(total_time.total_seconds() // 60)
        total_seconds = int(total_time.total_seconds() % 60)
        
        # Exibir resumo dos resultados
        st.subheader("Resultados do Simulado")
        
        # Métricas principais
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pontuação", f"{results['score']}%")
        with col2:
            st.metric("Acertos", f"{results['correct_count']}/{len(quiz['questions'])}")
        with col3:
            st.metric("Tempo Total", f"{total_minutes}min {total_seconds}s")
        
        # Gráfico de desempenho por matéria
        if "subject_scores" in results and results["subject_scores"]:
            st.subheader("Desempenho por Matéria")
            
            import pandas as pd
            import altair as alt
            
            # Preparar dados
            subjects = []
            scores = []
            
            for subject, score in results["subject_scores"].items():
                subjects.append(subject)
                scores.append(score)
            
            # Criar DataFrame
            df = pd.DataFrame({
                "Matéria": subjects,
                "Pontuação": scores
            })
            
            # Criar gráfico
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Pontuação:Q', scale=alt.Scale(domain=[0, 100])),
                y=alt.Y('Matéria:N', sort='-x'),
                color=alt.Color('Pontuação:Q', scale=alt.Scale(scheme='blues')),
                tooltip=['Matéria', 'Pontuação']
            ).properties(
                height=30 * len(subjects)
            )
            
            st.altair_chart(chart, use_container_width=True)
        
        # Detalhes das questões
        st.subheader("Detalhes das Questões")
        
        # Exibir cada questão com resultado
        for i, question_result in enumerate(results["question_results"]):
            # Encontrar questão original
            question = next((q for q in quiz["questions"] if q["id"] == question_result["question_id"]), None)
            
            if not question:
                continue
            
            # Determinar cor com base no resultado
            result_color = "green" if question_result["is_correct"] else "red"
            result_icon = "✓" if question_result["is_correct"] else "✗"
            
            # Criar expansor para cada questão
            with st.expander(f"Questão {i+1}: {result_icon} {question['text'][:50]}..."):
                st.markdown(f"**{question['text']}**")
                st.markdown(f"*{question['subject']} - {question['banca']} ({question['year']})*")
                
                # Exibir opções
                for opt in question["options"]:
                    # Determinar estilo para cada opção
                    if opt["id"] == question_result["correct_answer"]:
                        st.markdown(f"**{opt['id']}) {opt['text']} ✓**")
                    elif opt["id"] == question_result["submitted_answer"] and not question_result["is_correct"]:
                        st.markdown(f"**{opt['id']}) {opt['text']} ✗**")
                    else:
                        st.markdown(f"{opt['id']}) {opt['text']}")
                
                # Exibir explicação
                if "explanation" in question:
                    st.markdown("**Explicação:**")
                    st.markdown(question["explanation"])
        
        # Botões de ação
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Novo Simulado"):
                # Limpar estado
                st.session_state.current_quiz = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_start_time = None
                st.session_state.quiz_submitted = False
                st.session_state.quiz_results = None
                
                # Recarregar página
                st.experimental_rerun()
        
        with col2:
            if st.button("Salvar Resultados"):
                # Aqui poderia salvar os resultados em um banco de dados
                st.success("Resultados salvos com sucesso!")
    
    # Exibir página inicial
    elif not st.session_state.current_quiz:
        st.info("Configure e inicie um simulado usando as opções no menu lateral.")
        
        # Exibir estatísticas de simulados anteriores (simulado)
        st.subheader("Estatísticas de Simulados Anteriores")
        
        # Dados simulados
        import pandas as pd
        import altair as alt
        import numpy as np
        
        # Gerar dados simulados
        dates = [datetime.now() - timedelta(days=x*7) for x in range(5)]
        scores = [random.randint(60, 95) for _ in range(5)]
        
        # Criar DataFrame
        df = pd.DataFrame({
            "Data": dates,
            "Pontuação": scores
        })
        
        # Criar gráfico
        chart = alt.Chart(df).mark_line(point=True).encode(
            x='Data:T',
            y=alt.Y('Pontuação:Q', scale=alt.Scale(domain=[0, 100])),
            tooltip=['Data', 'Pontuação']
        ).properties(
            height=300
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # Dicas para o simulado
        st.subheader("Dicas para o Simulado")
        
        tips = [
            "Leia atentamente cada questão antes de responder.",
            "Administre bem o tempo, não gaste muito tempo em uma única questão.",
            "Responda primeiro as questões que você tem mais confiança.",
            "Elimine as alternativas claramente incorretas para aumentar suas chances.",
            "Revise suas respostas antes de finalizar, se houver tempo."
        ]
        
        for tip in tips:
            st.markdown(f"- {tip}")

if __name__ == "__main__":
    render_simulado_page()