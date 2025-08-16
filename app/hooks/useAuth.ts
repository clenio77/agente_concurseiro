'use client'

import { useSession, signIn, signOut } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export const useAuth = () => {
  const { data: session, status, update } = useSession()
  const router = useRouter()

  const isAuthenticated = status === 'authenticated'
  const isLoading = status === 'loading'
  const isUnauthenticated = status === 'unauthenticated'

  const login = async (email: string, password: string) => {
    try {
      const result = await signIn('credentials', {
        email,
        password,
        redirect: false,
      })

      if (result?.error) {
        throw new Error(result.error)
      }

      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Erro ao fazer login' 
      }
    }
  }

  const logout = async () => {
    try {
      await signOut({ redirect: false })
      router.push('/login')
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Erro ao fazer logout' 
      }
    }
  }

  const refreshSession = async () => {
    try {
      await update()
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Erro ao atualizar sessão' 
      }
    }
  }

  // Proteger rotas autenticadas
  useEffect(() => {
    if (isUnauthenticated && typeof window !== 'undefined') {
      router.push('/login')
    }
  }, [isUnauthenticated, router])

  // Durante o build estático, retornar valores padrão
  if (typeof window === 'undefined') {
    return {
      session: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      isUnauthenticated: true,
      login: () => Promise.resolve({ success: false, error: 'Build estático' }),
      logout: () => Promise.resolve({ success: false, error: 'Build estático' }),
      refreshSession: () => Promise.resolve({ success: false, error: 'Build estático' }),
    }
  }

  return {
    session,
    user: session?.user,
    isAuthenticated,
    isLoading,
    isUnauthenticated,
    login,
    logout,
    refreshSession,
  }
}
