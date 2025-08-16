'use client'

import React from 'react'
import { useAuth } from '@/hooks/useAuth'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

interface ProtectedRouteProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  fallback 
}) => {
  const { isAuthenticated, isLoading } = useAuth()

  // Durante o build estático, renderizar um placeholder
  if (typeof window === 'undefined') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-pulse text-lg text-gray-600 dark:text-gray-400">
            Carregando...
          </div>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return fallback || (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-gray-600 dark:text-gray-400">
            Carregando...
          </p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null // O hook useAuth já redireciona para /login
  }

  return <>{children}</>
}
