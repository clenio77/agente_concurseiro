import { createClient } from '@supabase/supabase-js'
import { Database } from '@/types/database'
import { getEnv } from '@/lib/env'

// Validar variáveis de ambiente
const env = getEnv()
const supabaseUrl = env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = env.NEXT_PUBLIC_SUPABASE_ANON_KEY

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  },
  realtime: {
    params: {
      eventsPerSecond: 10
    }
  },
  global: {
    headers: {
      'x-application-name': 'agente-concurseiro'
    }
  }
})

// Cliente para operações server-side
export const createServerSupabaseClient = () => {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
  const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!
  
  return createClient<Database>(supabaseUrl, supabaseServiceKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  })
}

// Hook para verificar se Supabase está configurado
export const useSupabaseClient = () => {
  if (!supabase) {
    throw new Error('Supabase client not initialized')
  }
  return supabase
}
