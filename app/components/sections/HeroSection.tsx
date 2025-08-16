'use client'

import React from 'react'
import { BookOpen, Target, Trophy, Users, Zap, Brain } from 'lucide-react'

export default function HeroSection() {
  return (
    <section className="relative bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
        <div className="text-center">
          {/* Main Title */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
            <span className="bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
              Agente Concurseiro
            </span>
            <br />
            <span className="text-2xl md:text-4xl lg:text-5xl text-gray-700 dark:text-gray-300">
              Sua IA para Aprovação
            </span>
          </h1>

          {/* Description */}
          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-3xl mx-auto leading-relaxed">
            Plataforma inteligente de preparação para concursos públicos com IA avançada, 
            gamificação personalizada e análise comportamental para maximizar seus resultados.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <button className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
              Começar Agora
            </button>
            <button className="border-2 border-primary-600 text-primary-600 hover:bg-primary-600 hover:text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-200">
              Ver Demonstração
            </button>
          </div>

          {/* Feature Highlights */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 max-w-4xl mx-auto">
            <div className="text-center group">
              <div className="w-16 h-16 mx-auto mb-3 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center group-hover:bg-primary-200 dark:group-hover:bg-primary-800 transition-colors duration-200">
                <Brain className="w-8 h-8 text-primary-600 dark:text-primary-400" />
              </div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">IA Inteligente</p>
            </div>

            <div className="text-center group">
              <div className="w-16 h-16 mx-auto mb-3 bg-secondary-100 dark:bg-secondary-900 rounded-full flex items-center justify-center group-hover:bg-secondary-200 dark:group-hover:bg-secondary-800 transition-colors duration-200">
                <Target className="w-8 h-8 text-secondary-600 dark:text-secondary-400" />
              </div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Foco Total</p>
            </div>

            <div className="text-center group">
              <div className="w-16 h-16 mx-auto mb-3 bg-success-100 dark:bg-success-900 rounded-full flex items-center justify-center group-hover:bg-success-200 dark:group-hover:bg-success-800 transition-colors duration-200">
                <Trophy className="w-8 h-8 text-success-600 dark:text-success-400" />
              </div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Gamificação</p>
            </div>

            <div className="text-center group">
              <div className="w-16 h-16 mx-auto mb-3 bg-warning-100 dark:bg-warning-900 rounded-full flex items-center justify-center group-hover:bg-warning-200 dark:group-hover:bg-warning-800 transition-colors duration-200">
                <BookOpen className="w-8 h-8 text-warning-600 dark:text-warning-400" />
              </div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Estudo Inteligente</p>
            </div>

            <div className="text-center group">
              <div className="w-16 h-16 mx-auto mb-3 bg-error-100 dark:bg-error-900 rounded-full flex items-center justify-center group-hover:bg-error-200 dark:group-hover:bg-error-800 transition-colors duration-200">
                <Zap className="w-8 h-8 text-error-600 dark:text-error-400" />
              </div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Performance</p>
            </div>

            <div className="text-center group">
              <div className="w-16 h-16 mx-auto mb-3 bg-gamification-100 dark:bg-gamification-900 rounded-full flex items-center justify-center group-hover:bg-gamification-200 dark:group-hover:bg-gamification-800 transition-colors duration-200">
                <Users className="w-8 h-8 text-gamification-600 dark:text-gamification-400" />
              </div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Comunidade</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-primary-600 dark:text-primary-400">10K+</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Usuários Ativos</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-secondary-600 dark:text-secondary-400">95%</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Taxa de Aprovação</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-success-600 dark:text-success-400">50+</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Concursos Cobertos</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-warning-600 dark:text-warning-400">24/7</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Suporte IA</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
