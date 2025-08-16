'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils/cn'
import { 
  Home, 
  BookOpen, 
  Target, 
  Trophy, 
  Brain, 
  Settings, 
  BarChart3,
  Calendar,
  FileText,
  Users,
  Rocket
} from 'lucide-react'

interface SidebarItem {
  label: string
  href: string
  icon: React.ReactNode
  badge?: string | number
}

const sidebarItems: SidebarItem[] = [
  { label: 'Início', href: '/dashboard', icon: <Home className="h-5 w-5" /> },
  { label: 'Estudos', href: '/study', icon: <BookOpen className="h-5 w-5" /> },
  { label: 'Metas', href: '/goals', icon: <Target className="h-5 w-5" /> },
  { label: 'Conquistas', href: '/achievements', icon: <Trophy className="h-5 w-5" /> },
  { label: 'IA Assistant', href: '/ai', icon: <Brain className="h-5 w-5" /> },
  { label: 'Inovações', href: '/innovations', icon: <Rocket className="h-5 w-5" /> },
  { label: 'Analytics', href: '/analytics', icon: <BarChart3 className="h-5 w-5" /> },
  { label: 'Calendário', href: '/calendar', icon: <Calendar className="h-5 w-5" /> },
  { label: 'Documentos', href: '/documents', icon: <FileText className="h-5 w-5" /> },
  { label: 'Comunidade', href: '/community', icon: <Users className="h-5 w-5" /> },
  { label: 'Configurações', href: '/settings', icon: <Settings className="h-5 w-5" /> },
]

export const Sidebar: React.FC = () => {
  const pathname = usePathname()

  return (
    <div className="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 h-screen overflow-y-auto">
      <div className="p-6">
        {/* Logo */}
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-10 h-10 bg-gradient-to-r from-primary-600 to-primary-400 rounded-xl flex items-center justify-center">
            <Target className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900 dark:text-white">
              Agente
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Concurseiro
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="space-y-2">
          {sidebarItems.map((item) => {
            const isActive = pathname === item.href
            const isActiveParent = pathname.startsWith(item.href)
            
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                  'hover:bg-gray-100 dark:hover:bg-gray-800',
                  isActive && 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300',
                  isActiveParent && !isActive && 'bg-gray-50 dark:bg-gray-800 text-gray-700 dark:text-gray-300',
                  !isActive && !isActiveParent && 'text-gray-600 dark:text-gray-400'
                )}
              >
                <div className="flex items-center space-x-3">
                  <div className={cn(
                    'flex items-center justify-center',
                    isActive ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400 dark:text-gray-500'
                  )}>
                    {item.icon}
                  </div>
                  <span>{item.label}</span>
                </div>
                
                {item.badge && (
                  <span className={cn(
                    'inline-flex items-center px-2 py-1 text-xs font-medium rounded-full',
                    isActive 
                      ? 'bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200'
                      : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                  )}>
                    {item.badge}
                  </span>
                )}
              </Link>
            )
          })}
        </nav>

        {/* User Profile */}
        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gray-300 dark:bg-gray-600 rounded-full flex items-center justify-center">
              <Users className="h-4 w-4 text-gray-600 dark:text-gray-400" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                Usuário
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                Nível 1
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
