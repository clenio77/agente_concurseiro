'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/Button'
import { Menu, X, User, BookOpen, Target, Trophy, Brain, LogOut } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'

interface NavItem {
  label: string
  href: string
  icon?: React.ReactNode
}

const navItems: NavItem[] = [
  { label: 'Dashboard', href: '/dashboard', icon: <Target className="h-4 w-4" /> },
  { label: 'Estudos', href: '/study', icon: <BookOpen className="h-4 w-4" /> },
  { label: 'Conquistas', href: '/achievements', icon: <Trophy className="h-4 w-4" /> },
  { label: 'IA', href: '/ai', icon: <Brain className="h-4 w-4" /> },
]

export const Navbar: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const { user, isAuthenticated, logout } = useAuth()

  const handleLogout = async () => {
    await logout()
  }

  return (
    <nav className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-primary-600 to-primary-400 rounded-lg flex items-center justify-center">
                <Target className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                Agente Concurseiro
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          {isAuthenticated && (
            <div className="hidden md:flex items-center space-x-8">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                >
                  {item.icon}
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          )}

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary-100 dark:bg-primary-900/20 rounded-full flex items-center justify-center">
                    <User className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                  </div>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {user?.name || 'Usuário'}
                  </span>
                </div>
                <Button variant="ghost" size="sm" onClick={handleLogout}>
                  <LogOut className="h-4 w-4 mr-2" />
                  Sair
                </Button>
              </>
            ) : (
              <>
                <Link href="/login">
                  <Button variant="ghost" size="sm">
                    <User className="h-4 w-4 mr-2" />
                    Entrar
                  </Button>
                </Link>
                <Link href="/register">
                  <Button size="sm">
                    Cadastrar
                  </Button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMobileMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
            {isAuthenticated && navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center space-x-2 px-3 py-2 text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-md transition-colors"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                {item.icon}
                <span>{item.label}</span>
              </Link>
            ))}
            
            <div className="pt-4 space-y-2">
              {isAuthenticated ? (
                <>
                  <div className="px-3 py-2">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-primary-100 dark:bg-primary-900/20 rounded-full flex items-center justify-center">
                        <User className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                      </div>
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        {user?.name || 'Usuário'}
                      </span>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm" className="w-full justify-start" onClick={handleLogout}>
                    <LogOut className="h-4 w-4 mr-2" />
                    Sair
                  </Button>
                </>
              ) : (
                <>
                  <Link href="/login">
                    <Button variant="ghost" size="sm" className="w-full justify-start">
                      <User className="h-4 w-4 mr-2" />
                      Entrar
                    </Button>
                  </Link>
                  <Link href="/register">
                    <Button size="sm" className="w-full">
                      Cadastrar
                    </Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
