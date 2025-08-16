export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          email: string
          full_name: string
          avatar_url?: string
          study_level: 'iniciante' | 'intermediario' | 'avancado' | 'expert'
          target_exam: string
          points: number
          level: number
          experience: number
          created_at: string
          updated_at: string
          last_login: string
          is_premium: boolean
          preferences: Json
        }
        Insert: {
          id?: string
          email: string
          full_name: string
          avatar_url?: string
          study_level?: 'iniciante' | 'intermediario' | 'avancado' | 'expert'
          target_exam?: string
          points?: number
          level?: number
          experience?: number
          created_at?: string
          updated_at?: string
          last_login?: string
          is_premium?: boolean
          preferences?: Json
        }
        Update: {
          email?: string
          full_name?: string
          avatar_url?: string
          study_level?: 'iniciante' | 'intermediario' | 'avancado' | 'expert'
          target_exam?: string
          points?: number
          level?: number
          experience?: number
          updated_at?: string
          last_login?: string
          is_premium?: boolean
          preferences?: Json
        }
      }
      study_sessions: {
        Row: {
          id: string
          user_id: string
          subject: string
          duration_minutes: number
          score: number
          questions_answered: number
          correct_answers: number
          session_type: 'quiz' | 'flashcard' | 'reading' | 'video' | 'mixed'
          difficulty: 'easy' | 'medium' | 'hard'
          created_at: string
          ended_at?: string
          metadata: Json
        }
        Insert: {
          id?: string
          user_id: string
          subject: string
          duration_minutes: number
          score: number
          questions_answered: number
          correct_answers: number
          session_type: 'quiz' | 'flashcard' | 'reading' | 'video' | 'mixed'
          difficulty: 'easy' | 'medium' | 'hard'
          created_at?: string
          ended_at?: string
          metadata?: Json
        }
        Update: {
          subject?: string
          duration_minutes?: number
          score?: number
          questions_answered?: number
          correct_answers?: number
          session_type?: 'quiz' | 'flashcard' | 'reading' | 'video' | 'mixed'
          difficulty?: 'easy' | 'medium' | 'hard'
          ended_at?: string
          metadata?: Json
        }
      }
      flashcards: {
        Row: {
          id: string
          user_id: string
          question: string
          answer: string
          subject: string
          difficulty: 'easy' | 'medium' | 'hard'
          category: string
          tags: string[]
          next_review: string
          review_count: number
          success_rate: number
          created_at: string
          updated_at: string
          metadata: Json
        }
        Insert: {
          id?: string
          user_id: string
          question: string
          answer: string
          subject: string
          difficulty: 'easy' | 'medium' | 'hard'
          category: string
          tags?: string[]
          next_review?: string
          review_count?: number
          success_rate?: number
          created_at?: string
          updated_at?: string
          metadata?: Json
        }
        Update: {
          question?: string
          answer?: string
          subject?: string
          difficulty?: 'easy' | 'medium' | 'hard'
          category?: string
          tags?: string[]
          next_review?: string
          review_count?: number
          success_rate?: number
          updated_at?: string
          metadata?: Json
        }
      }
      quizzes: {
        Row: {
          id: string
          user_id: string
          title: string
          subject: string
          questions: Json
          total_questions: number
          time_limit_minutes: number
          difficulty: 'easy' | 'medium' | 'hard'
          created_at: string
          updated_at: string
          is_public: boolean
          tags: string[]
        }
        Insert: {
          id?: string
          user_id: string
          title: string
          subject: string
          questions: Json
          total_questions: number
          time_limit_minutes: number
          difficulty: 'easy' | 'medium' | 'hard'
          created_at?: string
          updated_at?: string
          is_public?: boolean
          tags?: string[]
        }
        Update: {
          title?: string
          subject?: string
          questions?: Json
          total_questions?: number
          time_limit_minutes?: number
          difficulty?: 'easy' | 'medium' | 'hard'
          updated_at?: string
          is_public?: boolean
          tags?: string[]
        }
      }
      quiz_results: {
        Row: {
          id: string
          quiz_id: string
          user_id: string
          score: number
          total_questions: number
          correct_answers: number
          time_taken_minutes: number
          answers: Json
          completed_at: string
          metadata: Json
        }
        Insert: {
          id?: string
          quiz_id: string
          user_id: string
          score: number
          total_questions: number
          correct_answers: number
          time_taken_minutes: number
          answers: Json
          completed_at?: string
          metadata?: Json
        }
        Update: {
          score?: number
          total_questions?: number
          correct_answers?: number
          time_taken_minutes?: number
          answers?: Json
          completed_at?: string
          metadata?: Json
        }
      }
      study_progress: {
        Row: {
          id: string
          user_id: string
          subject: string
          total_time_minutes: number
          total_sessions: number
          average_score: number
          last_studied: string
          streak_days: number
          level: number
          experience: number
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          subject: string
          total_time_minutes?: number
          total_sessions?: number
          average_score?: number
          last_studied?: string
          streak_days?: number
          level?: number
          experience?: number
          created_at?: string
          updated_at?: string
        }
        Update: {
          total_time_minutes?: number
          total_sessions?: number
          average_score?: number
          last_studied?: string
          streak_days?: number
          level?: number
          experience?: number
          updated_at?: string
        }
      }
      achievements: {
        Row: {
          id: string
          user_id: string
          achievement_type: string
          title: string
          description: string
          icon_url?: string
          points_earned: number
          unlocked_at: string
          metadata: Json
        }
        Insert: {
          id?: string
          user_id: string
          achievement_type: string
          title: string
          description: string
          icon_url?: string
          points_earned: number
          unlocked_at?: string
          metadata?: Json
        }
        Update: {
          achievement_type?: string
          title?: string
          description?: string
          icon_url?: string
          points_earned?: number
          unlocked_at?: string
          metadata?: Json
        }
      }
      notifications: {
        Row: {
          id: string
          user_id: string
          title: string
          message: string
          type: 'info' | 'success' | 'warning' | 'error' | 'achievement'
          is_read: boolean
          action_url?: string
          created_at: string
          read_at?: string
          metadata: Json
        }
        Insert: {
          id?: string
          user_id: string
          title: string
          message: string
          type: 'info' | 'success' | 'warning' | 'error' | 'achievement'
          is_read?: boolean
          action_url?: string
          created_at?: string
          read_at?: string
          metadata?: Json
        }
        Update: {
          title?: string
          message?: string
          type?: 'info' | 'success' | 'warning' | 'error' | 'achievement'
          is_read?: boolean
          action_url?: string
          read_at?: string
          metadata?: Json
        }
      }
      voice_assistant_sessions: {
        Row: {
          id: string
          user_id: string
          session_type: 'command' | 'question' | 'dictation'
          input_text?: string
          output_text: string
          duration_seconds: number
          language: string
          created_at: string
          metadata: Json
        }
        Insert: {
          id?: string
          user_id: string
          session_type: 'command' | 'question' | 'dictation'
          input_text?: string
          output_text: string
          duration_seconds: number
          language: string
          created_at?: string
          metadata?: Json
        }
        Update: {
          session_type?: 'command' | 'question' | 'dictation'
          input_text?: string
          output_text?: string
          duration_seconds?: number
          language?: string
          metadata?: Json
        }
      }
      behavioral_analysis: {
        Row: {
          id: string
          user_id: string
          session_id: string
          focus_score: number
          attention_span_minutes: number
          breaks_taken: number
          study_pattern: 'consistent' | 'sporadic' | 'intensive' | 'relaxed'
          created_at: string
          metadata: Json
        }
        Insert: {
          id?: string
          user_id: string
          session_id: string
          focus_score: number
          attention_span_minutes: number
          breaks_taken: number
          study_pattern: 'consistent' | 'sporadic' | 'intensive' | 'relaxed'
          created_at?: string
          metadata?: Json
        }
        Update: {
          focus_score?: number
          attention_span_minutes?: number
          breaks_taken?: number
          study_pattern?: 'consistent' | 'sporadic' | 'intensive' | 'relaxed'
          metadata?: Json
        }
      }
      trend_predictions: {
        Row: {
          id: string
          subject: string
          prediction_type: 'exam_trend' | 'topic_frequency' | 'difficulty_shift'
          prediction_data: Json
          confidence_score: number
          valid_until: string
          created_at: string
          metadata: Json
        }
        Insert: {
          id?: string
          subject: string
          prediction_type: 'exam_trend' | 'topic_frequency' | 'difficulty_shift'
          prediction_data: Json
          confidence_score: number
          valid_until: string
          created_at?: string
          metadata?: Json
        }
        Update: {
          subject?: string
          prediction_type?: 'exam_trend' | 'topic_frequency' | 'difficulty_shift'
          prediction_data?: Json
          confidence_score?: number
          valid_until?: string
          metadata?: Json
        }
      }
      ar_sessions: {
        Row: {
          id: string
          user_id: string
          model_type: '3d_model' | 'virtual_environment' | 'interactive_element'
          model_url: string
          session_duration_minutes: number
          interactions_count: number
          created_at: string
          ended_at?: string
          metadata: Json
        }
        Insert: {
          id?: string
          user_id: string
          model_type: '3d_model' | 'virtual_environment' | 'interactive_element'
          model_url: string
          session_duration_minutes: number
          interactions_count?: number
          created_at?: string
          ended_at?: string
          metadata?: Json
        }
        Update: {
          model_type?: '3d_model' | 'virtual_environment' | 'interactive_element'
          model_url?: string
          session_duration_minutes?: number
          interactions_count?: number
          ended_at?: string
          metadata?: Json
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

// Tipos auxiliares
export type Json = string | number | boolean | null | { [key: string]: Json | undefined } | Json[]

export type Tables<T extends keyof Database['public']['Tables']> = Database['public']['Tables'][T]['Row']
export type Inserts<T extends keyof Database['public']['Tables']> = Database['public']['Tables'][T]['Insert']
export type Updates<T extends keyof Database['public']['Tables']> = Database['public']['Tables'][T]['Update']

// Tipos específicos
export type User = Tables<'users'>
export type StudySession = Tables<'study_sessions'>
export type Flashcard = Tables<'flashcards'>
export type Quiz = Tables<'quizzes'>
export type QuizResult = Tables<'quiz_results'>
export type StudyProgress = Tables<'study_progress'>
export type Achievement = Tables<'achievements'>
export type Notification = Tables<'notifications'>
export type VoiceAssistantSession = Tables<'voice_assistant_sessions'>
export type BehavioralAnalysis = Tables<'behavioral_analysis'>
export type TrendPrediction = Tables<'trend_predictions'>
export type ARSession = Tables<'ar_sessions'>

// Tipos para inserção
export type CreateUser = Inserts<'users'>
export type CreateStudySession = Inserts<'study_sessions'>
export type CreateFlashcard = Inserts<'flashcards'>
export type CreateQuiz = Inserts<'quizzes'>
export type CreateQuizResult = Inserts<'quiz_results'>
export type CreateStudyProgress = Inserts<'study_progress'>
export type CreateAchievement = Inserts<'achievements'>
export type CreateNotification = Inserts<'notifications'>
export type CreateVoiceAssistantSession = Inserts<'voice_assistant_sessions'>
export type CreateBehavioralAnalysis = Inserts<'behavioral_analysis'>
export type CreateTrendPrediction = Inserts<'trend_predictions'>
export type CreateARSession = Inserts<'ar_sessions'>

// Tipos para atualização
export type UpdateUser = Updates<'users'>
export type UpdateStudySession = Updates<'study_sessions'>
export type UpdateFlashcard = Updates<'flashcards'>
export type UpdateQuiz = Updates<'quizzes'>
export type UpdateQuizResult = Updates<'quiz_results'>
export type UpdateStudyProgress = Updates<'study_progress'>
export type UpdateAchievement = Updates<'achievements'>
export type UpdateNotification = Updates<'notifications'>
export type UpdateVoiceAssistantSession = Updates<'voice_assistant_sessions'>
export type UpdateBehavioralAnalysis = Updates<'behavioral_analysis'>
export type UpdateTrendPrediction = Updates<'trend_predictions'>
export type UpdateARSession = Updates<'ar_sessions'>
