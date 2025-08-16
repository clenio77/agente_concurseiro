import { z } from 'zod'

// Schema de validação para variáveis de ambiente
const envSchema = z.object({
  // Supabase
  NEXT_PUBLIC_SUPABASE_URL: z.string().url('Supabase URL deve ser uma URL válida'),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(100, 'Chave anônima muito curta'),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(100, 'Chave service role muito curta'),
  
  // NextAuth
  NEXTAUTH_SECRET: z.string().min(32, 'Secret deve ter pelo menos 32 caracteres'),
  NEXTAUTH_URL: z.string().url('NextAuth URL deve ser uma URL válida'),
  
  // OpenAI (opcional)
  NEXT_PUBLIC_OPENAI_API_KEY: z.string().optional(),
  
  // Ambiente
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  NEXT_PUBLIC_ENVIRONMENT: z.enum(['development', 'staging', 'production']).default('development'),
  
  // Google (opcional)
  NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION: z.string().optional(),
  
  // App
  NEXT_PUBLIC_APP_URL: z.string().url('App URL deve ser uma URL válida').default('http://localhost:3000'),
})

// Função para validar e retornar variáveis de ambiente
export function validateEnv() {
  try {
    const env = envSchema.parse(process.env)
    return { success: true, env }
  } catch (error) {
    if (error instanceof z.ZodError) {
      const missingVars = error.errors.map(err => `${err.path.join('.')}: ${err.message}`)
      console.error('❌ Variáveis de ambiente inválidas:')
      missingVars.forEach(msg => console.error(`   ${msg}`))
      
      throw new Error(`Variáveis de ambiente inválidas:\n${missingVars.join('\n')}`)
    }
    throw error
  }
}

// Função para obter variáveis de ambiente validadas
export function getEnv() {
  const result = validateEnv()
  if (!result.success) {
    throw new Error('Falha na validação de ambiente')
  }
  return result.env
}

// Função para verificar se estamos em produção
export function isProduction() {
  return process.env.NODE_ENV === 'production'
}

// Função para verificar se estamos em desenvolvimento
export function isDevelopment() {
  return process.env.NODE_ENV === 'development'
}

// Função para verificar se estamos em teste
export function isTest() {
  return process.env.NODE_ENV === 'test'
}
