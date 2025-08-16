'use client'

import React from 'react'
import { Navbar } from '@/components/navigation/Navbar'
import { Sidebar } from '@/components/navigation/Sidebar'

interface AppLayoutProps {
  children: React.ReactNode
  showSidebar?: boolean
}

export const AppLayout: React.FC<AppLayoutProps> = ({ 
  children, 
  showSidebar = true 
}) => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      
      <div className="flex">
        {showSidebar && <Sidebar />}
        
        <main className={cn(
          "flex-1 p-6",
          showSidebar ? "ml-0" : "ml-0"
        )}>
          {children}
        </main>
      </div>
    </div>
  )
}

function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ')
}
