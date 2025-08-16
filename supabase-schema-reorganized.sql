-- =====================================================
-- SCHEMA COMPLETO PARA AGENTE CONCURSEIRO V3.0
-- VERSÃO REORGANIZADA - ORDEM CORRETA
-- =====================================================

-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- 1. TABELAS PRINCIPAIS (CRIAR PRIMEIRO)
-- =====================================================

-- Tabela de usuários (estende auth.users)
CREATE TABLE public.users (
    id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    avatar_url TEXT,
    study_level TEXT DEFAULT 'iniciante' CHECK (study_level IN ('iniciante', 'intermediario', 'avancado', 'expert')),
    target_exam TEXT DEFAULT 'geral',
    points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    experience INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_premium BOOLEAN DEFAULT FALSE,
    preferences JSONB DEFAULT '{}'::jsonb,
    timezone TEXT DEFAULT 'America/Sao_Paulo',
    language TEXT DEFAULT 'pt-BR'
);

-- Tabela de sessões de estudo
CREATE TABLE public.study_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    focus_score INTEGER CHECK (focus_score >= 0 AND focus_score <= 100),
    comprehension_score INTEGER CHECK (comprehension_score >= 0 AND comprehension_score <= 100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de flashcards
CREATE TABLE public.flashcards (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    front_content TEXT NOT NULL,
    back_content TEXT NOT NULL,
    difficulty INTEGER DEFAULT 1 CHECK (difficulty >= 1 AND difficulty <= 5),
    last_reviewed TIMESTAMP WITH TIME ZONE,
    next_review TIMESTAMP WITH TIME ZONE,
    review_count INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de quizzes
CREATE TABLE public.quizzes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    total_questions INTEGER NOT NULL,
    time_limit_minutes INTEGER,
    difficulty TEXT DEFAULT 'medio' CHECK (difficulty IN ('facil', 'medio', 'dificil')),
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de questões dos quizzes
CREATE TABLE public.quiz_questions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    quiz_id UUID REFERENCES public.quizzes(id) ON DELETE CASCADE NOT NULL,
    question_text TEXT NOT NULL,
    question_type TEXT DEFAULT 'multiple_choice' CHECK (question_type IN ('multiple_choice', 'true_false', 'essay')),
    options JSONB,
    correct_answer TEXT NOT NULL,
    explanation TEXT,
    difficulty INTEGER DEFAULT 1 CHECK (difficulty >= 1 AND difficulty <= 5),
    points INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de resultados de quizzes
CREATE TABLE public.quiz_results (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    quiz_id UUID REFERENCES public.quizzes(id) ON DELETE CASCADE NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    time_taken_minutes INTEGER,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    answers JSONB
);

-- Tabela de progresso de estudo
CREATE TABLE public.study_progress (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    mastery_level INTEGER DEFAULT 0 CHECK (mastery_level >= 0 AND mastery_level <= 100),
    study_time_minutes INTEGER DEFAULT 0,
    last_studied TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, subject, topic)
);

-- Tabela de conquistas
CREATE TABLE public.achievements (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    achievement_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    icon_url TEXT,
    points_awarded INTEGER DEFAULT 0,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de notificações
CREATE TABLE public.notifications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info' CHECK (type IN ('info', 'success', 'warning', 'error')),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    read_at TIMESTAMP WITH TIME ZONE
);

-- =====================================================
-- 2. TABELAS DE IA E RECURSOS AVANÇADOS
-- =====================================================

-- Tabela de sessões do Voice Assistant
CREATE TABLE public.voice_assistant_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    session_start TIMESTAMP WITH TIME ZONE NOT NULL,
    session_end TIMESTAMP WITH TIME ZONE,
    commands_processed INTEGER DEFAULT 0,
    total_duration_minutes INTEGER,
    language TEXT DEFAULT 'pt-BR',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de comandos de voz
CREATE TABLE public.voice_commands (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID REFERENCES public.voice_assistant_sessions(id) ON DELETE CASCADE NOT NULL,
    command_text TEXT NOT NULL,
    recognized_text TEXT,
    action_taken TEXT,
    success BOOLEAN DEFAULT FALSE,
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de análise comportamental
CREATE TABLE public.behavioral_analysis (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    session_id UUID REFERENCES public.study_sessions(id) ON DELETE CASCADE NOT NULL,
    focus_metrics JSONB,
    attention_span_minutes INTEGER,
    break_patterns JSONB,
    productivity_score DECIMAL(5,2),
    recommendations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de predições de tendências
CREATE TABLE public.trend_predictions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    exam_type TEXT NOT NULL,
    predicted_topics JSONB,
    confidence_score DECIMAL(5,2),
    study_recommendations JSONB,
    predicted_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de sessões de Realidade Aumentada
CREATE TABLE public.ar_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    ar_type TEXT NOT NULL,
    content_url TEXT,
    duration_minutes INTEGER,
    interaction_data JSONB,
    performance_metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 3. TABELAS DE GAMIFICAÇÃO
-- =====================================================

-- Tabela de níveis e experiência
CREATE TABLE public.user_levels (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    current_level INTEGER DEFAULT 1,
    current_experience INTEGER DEFAULT 0,
    experience_to_next_level INTEGER DEFAULT 100,
    total_experience_earned INTEGER DEFAULT 0,
    level_up_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de missões diárias
CREATE TABLE public.daily_missions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    mission_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    target_value INTEGER NOT NULL,
    current_value INTEGER DEFAULT 0,
    reward_points INTEGER DEFAULT 0,
    is_completed BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de streak de estudos
CREATE TABLE public.study_streaks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_study_date DATE,
    streak_start_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 4. TABELAS DE TEMPLATES (CRIAR ANTES DAS FUNÇÕES)
-- =====================================================

-- Tabela de conquistas padrão (sem user_id para reutilização)
CREATE TABLE public.achievement_templates (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    achievement_type TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    icon_url TEXT,
    points_awarded INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 5. ÍNDICES PARA PERFORMANCE
-- =====================================================

-- Índices para consultas frequentes
CREATE INDEX idx_users_email ON public.users(email);
CREATE INDEX idx_users_study_level ON public.users(study_level);
CREATE INDEX idx_study_sessions_user_id ON public.study_sessions(user_id);
CREATE INDEX idx_study_sessions_subject ON public.study_sessions(subject);
CREATE INDEX idx_study_sessions_start_time ON public.study_sessions(start_time);
CREATE INDEX idx_flashcards_user_id ON public.flashcards(user_id);
CREATE INDEX idx_flashcards_subject ON public.flashcards(subject);
CREATE INDEX idx_flashcards_next_review ON public.flashcards(next_review);
CREATE INDEX idx_quizzes_user_id ON public.quizzes(user_id);
CREATE INDEX idx_quizzes_subject ON public.quizzes(subject);
CREATE INDEX idx_quiz_results_user_id ON public.quiz_results(user_id);
CREATE INDEX idx_study_progress_user_id ON public.study_progress(user_id);
CREATE INDEX idx_notifications_user_id ON public.notifications(user_id);
CREATE INDEX idx_notifications_is_read ON public.notifications(is_read);

-- Índices compostos para consultas complexas
CREATE INDEX idx_study_sessions_user_subject ON public.study_sessions(user_id, subject);
CREATE INDEX idx_flashcards_user_subject ON public.flashcards(user_id, subject);
CREATE INDEX idx_quiz_results_user_quiz ON public.quiz_results(user_id, quiz_id);

-- =====================================================
-- 6. DADOS INICIAIS (INSERIR APÓS CRIAR TABELAS)
-- =====================================================

-- Inserir templates de conquistas padrão
INSERT INTO public.achievement_templates (achievement_type, title, description, points_awarded) VALUES
('first_login', 'Primeiro Acesso', 'Bem-vindo ao Agente Concurseiro!', 10),
('first_session', 'Primeira Sessão', 'Completou sua primeira sessão de estudo', 25),
('streak_3', 'Consistente', 'Manteve 3 dias seguidos de estudo', 50),
('streak_7', 'Dedicado', 'Manteve 7 dias seguidos de estudo', 100),
('streak_30', 'Viciado em Estudos', 'Manteve 30 dias seguidos de estudo', 500),
('first_quiz', 'Primeiro Quiz', 'Completou seu primeiro quiz', 30),
('perfect_score', 'Perfeição', 'Acertou 100% em um quiz', 100),
('flashcard_master', 'Mestre dos Flashcards', 'Criou 50 flashcards', 75),
('subject_expert', 'Especialista', 'Dominou um assunto completamente', 200);

-- =====================================================
-- 7. FUNÇÕES E TRIGGERS (CRIAR APÓS TODAS AS TABELAS)
-- =====================================================

-- Função para atualizar timestamp de atualização
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Função para calcular experiência e nível
CREATE OR REPLACE FUNCTION calculate_user_level()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualizar experiência total
    UPDATE public.user_levels 
    SET current_experience = current_experience + NEW.points,
        total_experience_earned = total_experience_earned + NEW.points
    WHERE user_id = NEW.user_id;
    
    -- Verificar se subiu de nível
    UPDATE public.user_levels 
    SET current_level = current_level + 1,
        experience_to_next_level = experience_to_next_level * 1.5,
        level_up_date = NOW()
    WHERE user_id = NEW.user_id 
    AND current_experience >= experience_to_next_level;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Função para criar perfil completo de usuário
CREATE OR REPLACE FUNCTION create_user_profile(
    user_uuid UUID,
    user_email TEXT,
    user_full_name TEXT
)
RETURNS VOID AS $$
BEGIN
    -- Inserir usuário na tabela users
    INSERT INTO public.users (id, email, full_name)
    VALUES (user_uuid, user_email, user_full_name);
    
    -- Inserir nível inicial
    INSERT INTO public.user_levels (user_id, current_level, current_experience, experience_to_next_level)
    VALUES (user_uuid, 1, 0, 100);
    
    -- Inserir streak inicial
    INSERT INTO public.study_streaks (user_id, current_streak, longest_streak)
    VALUES (user_uuid, 0, 0);
    
    -- Inserir conquista de primeiro acesso
    INSERT INTO public.achievements (user_id, achievement_type, title, description, points_awarded)
    SELECT user_uuid, achievement_type, title, description, points_awarded
    FROM public.achievement_templates
    WHERE achievement_type = 'first_login';
    
    -- Atualizar pontos do usuário
    UPDATE public.users 
    SET points = points + (
        SELECT points_awarded 
        FROM public.achievement_templates 
        WHERE achievement_type = 'first_login'
    )
    WHERE id = user_uuid;
    
    -- Inserir progresso inicial para matérias básicas
    INSERT INTO public.study_progress (user_id, subject, topic, mastery_level)
    VALUES 
        (user_uuid, 'Português', 'Gramática', 0),
        (user_uuid, 'Matemática', 'Aritmética', 0),
        (user_uuid, 'Direito', 'Constitucional', 0),
        (user_uuid, 'Informática', 'Conceitos Básicos', 0);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para obter estatísticas do usuário
CREATE OR REPLACE FUNCTION get_user_stats(user_uuid UUID)
RETURNS TABLE (
    total_study_time INTEGER,
    total_sessions INTEGER,
    total_flashcards INTEGER,
    total_quizzes INTEGER,
    average_score DECIMAL(5,2),
    current_streak INTEGER,
    longest_streak INTEGER,
    total_points INTEGER,
    current_level INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COALESCE(SUM(ss.duration_minutes), 0)::INTEGER as total_study_time,
        COUNT(ss.id)::INTEGER as total_sessions,
        COUNT(f.id)::INTEGER as total_flashcards,
        COUNT(q.id)::INTEGER as total_quizzes,
        COALESCE(AVG(qr.score), 0.0)::DECIMAL(5,2) as average_score,
        COALESCE(ss_streak.current_streak, 0)::INTEGER as current_streak,
        COALESCE(ss_streak.longest_streak, 0)::INTEGER as longest_streak,
        COALESCE(u.points, 0)::INTEGER as total_points,
        COALESCE(ul.current_level, 1)::INTEGER as current_level
    FROM public.users u
    LEFT JOIN public.study_sessions ss ON u.id = ss.user_id
    LEFT JOIN public.flashcards f ON u.id = f.user_id
    LEFT JOIN public.quizzes q ON u.id = q.user_id
    LEFT JOIN public.quiz_results qr ON q.id = qr.quiz_id
    LEFT JOIN public.study_streaks ss_streak ON u.id = ss_streak.user_id
    LEFT JOIN public.user_levels ul ON u.id = ul.user_id
    WHERE u.id = user_uuid
    GROUP BY u.id, u.points, ss_streak.current_streak, ss_streak.longest_streak, ul.current_level;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Função para obter recomendações de estudo
CREATE OR REPLACE FUNCTION get_study_recommendations(user_uuid UUID)
RETURNS TABLE (
    subject TEXT,
    topic TEXT,
    priority_score DECIMAL(5,2),
    last_studied TIMESTAMP WITH TIME ZONE,
    mastery_level INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        sp.subject,
        sp.topic,
        (100 - sp.mastery_level + 
         EXTRACT(EPOCH FROM (NOW() - sp.last_studied)) / 86400)::DECIMAL(5,2) as priority_score,
        sp.last_studied,
        sp.mastery_level
    FROM public.study_progress sp
    WHERE sp.user_id = user_uuid
    ORDER BY priority_score DESC
    LIMIT 10;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para criar perfil completo quando usuário se registra
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    -- Chamar função para criar perfil completo
    PERFORM create_user_profile(
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1))
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- 8. TRIGGERS (CRIAR APÓS AS FUNÇÕES)
-- =====================================================

-- Triggers para atualizar timestamps
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_flashcards_updated_at BEFORE UPDATE ON public.flashcards
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quizzes_updated_at BEFORE UPDATE ON public.quizzes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_study_progress_updated_at BEFORE UPDATE ON public.study_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_levels_updated_at BEFORE UPDATE ON public.user_levels
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_study_streaks_updated_at BEFORE UPDATE ON public.study_streaks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger para atualizar nível quando ganhar pontos
CREATE TRIGGER update_user_level_after_points 
    AFTER INSERT ON public.achievements
    FOR EACH ROW EXECUTE FUNCTION calculate_user_level();

-- Trigger para criar perfil completo quando usuário se registra
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- =====================================================
-- 9. POLÍTICAS RLS (ROW LEVEL SECURITY)
-- =====================================================

-- Habilitar RLS em todas as tabelas
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.study_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.flashcards ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quizzes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quiz_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.study_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.voice_assistant_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.voice_commands ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.behavioral_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.trend_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ar_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_levels ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.daily_missions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.study_streaks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.achievement_templates ENABLE ROW LEVEL SECURITY;

-- Políticas para usuários
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- Políticas para sessões de estudo
CREATE POLICY "Users can manage own study sessions" ON public.study_sessions
    FOR ALL USING (auth.uid() = user_id);

-- Políticas para flashcards
CREATE POLICY "Users can manage own flashcards" ON public.flashcards
    FOR ALL USING (auth.uid() = user_id);

-- Políticas para quizzes
CREATE POLICY "Users can manage own quizzes" ON public.quizzes
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view public quizzes" ON public.quizzes
    FOR SELECT USING (is_public = true);

-- Políticas para questões de quiz
CREATE POLICY "Users can manage own quiz questions" ON public.quiz_questions
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.quizzes 
            WHERE id = quiz_id AND user_id = auth.uid()
        )
    );

-- Políticas para resultados de quiz
CREATE POLICY "Users can manage own quiz results" ON public.quiz_results
    FOR ALL USING (auth.uid() = user_id);

-- Políticas para progresso de estudo
CREATE POLICY "Users can manage own study progress" ON public.study_progress
    FOR ALL USING (auth.uid() = user_id);

-- Políticas para conquistas
CREATE POLICY "Users can view own achievements" ON public.achievements
    FOR SELECT USING (auth.uid() = user_id);

-- Políticas para notificações
CREATE POLICY "Users can manage own notifications" ON public.notifications
    FOR ALL USING (auth.uid() = user_id);

-- Políticas para Voice Assistant
CREATE POLICY "Users can manage own voice sessions" ON public.voice_assistant_sessions
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own voice commands" ON public.voice_commands
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.voice_assistant_sessions 
            WHERE id = session_id AND user_id = auth.uid()
        )
    );

-- Políticas para análise comportamental
CREATE POLICY "Users can manage own behavioral data" ON public.behavioral_analysis
    FOR ALL USING (auth.uid() = user_id);

-- Políticas para predições de tendências
CREATE POLICY "Users can manage own trend predictions" ON public.trend_predictions
    FOR ALL USING (auth.uid() = user_id);

-- Políticas para sessões de AR
CREATE POLICY "Users can manage own AR sessions" ON public.ar_sessions
    FOR ALL USING (auth.uid() = user_id);

-- Políticas para gamificação
CREATE POLICY "Users can manage own level data" ON public.user_levels
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own missions" ON public.daily_missions
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own streaks" ON public.study_streaks
    FOR ALL USING (auth.uid() = user_id);

-- Políticas para templates de conquistas (leitura pública)
CREATE POLICY "Anyone can view achievement templates" ON public.achievement_templates
    FOR SELECT USING (true);

-- =====================================================
-- 10. COMENTÁRIOS FINAIS
-- =====================================================

COMMENT ON TABLE public.users IS 'Tabela principal de usuários do sistema';
COMMENT ON TABLE public.study_sessions IS 'Sessões de estudo dos usuários';
COMMENT ON TABLE public.flashcards IS 'Flashcards para estudo';
COMMENT ON TABLE public.quizzes IS 'Quizzes de estudo';
COMMENT ON TABLE public.achievement_templates IS 'Templates de conquistas padrão do sistema';
COMMENT ON TABLE public.achievements IS 'Conquistas e gamificação';
COMMENT ON TABLE public.voice_assistant_sessions IS 'Sessões do assistente de voz';
COMMENT ON TABLE public.behavioral_analysis IS 'Análise comportamental dos usuários';
COMMENT ON TABLE public.trend_predictions IS 'Predições de tendências de concursos';

-- =====================================================
-- FIM DO SCHEMA REORGANIZADO
-- =====================================================
