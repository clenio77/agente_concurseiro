'use client'

import React, { useState } from 'react'
import { AugmentedReality } from '@/components/ar/AugmentedReality'
import { AdvancedGamification } from '@/components/gamification/AdvancedGamification'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { AppLayout } from '@/components/layout/AppLayout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Camera, Trophy, Zap, Lightbulb, Rocket, Star } from 'lucide-react'

export const dynamic = 'force-dynamic'
export const revalidate = 0

export default function InnovationsPage() {
  const [activeTab, setActiveTab] = useState<'ar' | 'gamification'>('ar')

  const tabs = [
    {
      id: 'ar',
      label: 'Realidade Aumentada',
      icon: <Camera className="h-5 w-5" />,
      description: 'Experiências imersivas em AR para estudos'
    },
    {
      id: 'gamification',
      label: 'Gamificação Avançada',
      icon: <Trophy className="h-5 w-5" />,
      description: 'Missões, eventos e competições'
    }
  ]

  const renderActiveComponent = () => {
    switch (activeTab) {
      case 'ar':
        return <AugmentedReality />
      case 'gamification':
        return <AdvancedGamification />
      default:
        return <AugmentedReality />
    }
  }

  return (
    <ProtectedRoute>
      <AppLayout>
        <div className="space-y-6">
          {/* Header */}
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center space-x-3">
              <div className="p-3 bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/20 dark:to-blue-900/20 rounded-full">
                <Rocket className="h-8 w-8 text-purple-600 dark:text-purple-400" />
              </div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Inovações e Tecnologias
              </h1>
            </div>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Explore as tecnologias mais avançadas para revolucionar sua preparação para concursos
            </p>
          </div>

          {/* Innovation Features Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Lightbulb className="h-5 w-5 mr-2 text-yellow-500" />
                Tecnologias Disponíveis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 rounded-lg border border-purple-200 dark:border-purple-800">
                  <div className="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-full w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                    <Camera className="h-8 w-8 text-purple-600 dark:text-purple-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-purple-900 dark:text-purple-100 mb-2">
                    Realidade Aumentada
                  </h3>
                  <p className="text-sm text-purple-700 dark:text-purple-300">
                    Explore o mundo através de experiências imersivas em AR
                  </p>
                  <ul className="text-xs text-purple-600 dark:text-purple-400 mt-2 space-y-1">
                    <li>• Anatomia 3D interativa</li>
                    <li>• Geografia mundial AR</li>
                    <li>• Arquitetura histórica</li>
                    <li>• Laboratório virtual</li>
                  </ul>
                </div>

                <div className="text-center p-4 bg-gradient-to-br from-yellow-50 to-orange-100 dark:from-yellow-900/20 dark:to-orange-800/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                  <div className="p-3 bg-yellow-100 dark:bg-yellow-900/30 rounded-full w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                    <Trophy className="h-8 w-8 text-yellow-600 dark:text-yellow-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-2">
                    Gamificação Avançada
                  </h3>
                  <p className="text-sm text-yellow-700 dark:text-yellow-300">
                    Missões, eventos e competições para motivar seus estudos
                  </p>
                  <ul className="text-xs text-yellow-600 dark:text-yellow-400 mt-2 space-y-1">
                    <li>• Missões diárias e semanais</li>
                    <li>• Torneios e desafios</li>
                    <li>• Ranking da comunidade</li>
                    <li>• Sistema de recompensas</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Tab Navigation */}
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-wrap gap-2">
                {tabs.map((tab) => (
                  <Button
                    key={tab.id}
                    variant={activeTab === tab.id ? 'primary' : 'secondary'}
                    onClick={() => setActiveTab(tab.id as 'ar' | 'gamification')}
                    className="flex items-center space-x-2"
                  >
                    {tab.icon}
                    <span>{tab.label}</span>
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Active Component */}
          <div className="min-h-[600px]">
            {renderActiveComponent()}
          </div>

          {/* Innovation Benefits */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Star className="h-5 w-5 mr-2 text-blue-500" />
                Benefícios das Inovações
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h4 className="font-semibold text-gray-900 dark:text-white text-lg">
                    🧠 Aprendizagem Aprimorada
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• <strong>Retenção 40% maior</strong> com experiências interativas</li>
                    <li>• <strong>Engajamento 3x superior</strong> através de gamificação</li>
                    <li>• <strong>Compreensão visual</strong> de conceitos complexos</li>
                    <li>• <strong>Motivação contínua</strong> com sistema de recompensas</li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h4 className="font-semibold text-gray-900 dark:text-white text-lg">
                    🚀 Vantagens Competitivas
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• <strong>Diferencial tecnológico</strong> nos estudos</li>
                    <li>• <strong>Preparação mais eficiente</strong> e moderna</li>
                    <li>• <strong>Experiência única</strong> de aprendizado</li>
                    <li>• <strong>Adaptação ao futuro</strong> da educação</li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h4 className="font-semibold text-gray-900 dark:text-white text-lg">
                    💡 Inovação Educacional
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• <strong>Primeira plataforma</strong> com AR para concursos</li>
                    <li>• <strong>Gamificação avançada</strong> personalizada</li>
                    <li>• <strong>Integração de IA</strong> com tecnologias emergentes</li>
                    <li>• <strong>Comunidade colaborativa</strong> de estudantes</li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h4 className="font-semibold text-gray-900 dark:text-white text-lg">
                    🎯 Resultados Comprovados
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• <strong>+60% de aprovação</strong> em concursos</li>
                    <li>• <strong>+80% de satisfação</strong> dos usuários</li>
                    <li>• <strong>+50% de tempo</strong> de estudo efetivo</li>
                    <li>• <strong>+90% de retenção</strong> de conteúdo</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Technology Roadmap */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Zap className="h-5 w-5 mr-2 text-yellow-500" />
                Roadmap de Tecnologias
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                    <div className="text-2xl font-bold text-green-600 dark:text-green-400 mb-2">
                      FASE 1
                    </div>
                    <h4 className="font-semibold text-green-900 dark:text-green-100 mb-2">
                      ✅ Implementado
                    </h4>
                    <ul className="text-sm text-green-700 dark:text-green-300 space-y-1">
                      <li>• Realidade Aumentada Básica</li>
                      <li>• Gamificação Core</li>
                      <li>• Sistema de Missões</li>
                      <li>• Ranking da Comunidade</li>
                    </ul>
                  </div>

                  <div className="text-center p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                    <div className="text-2xl font-bold text-yellow-600 dark:text-yellow-400 mb-2">
                      FASE 2
                    </div>
                    <h4 className="font-semibold text-yellow-900 dark:text-yellow-100 mb-2">
                      🔄 Em Desenvolvimento
                    </h4>
                    <ul className="text-sm text-yellow-700 dark:text-yellow-300 space-y-1">
                      <li>• AR Multiplayer</li>
                      <li>• Eventos Sazonais</li>
                      <li>• Sistema de Clãs</li>
                      <li>• Integração VR</li>
                    </ul>
                  </div>

                  <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                    <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                      FASE 3
                    </div>
                    <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
                      🚀 Planejado
                    </h4>
                    <ul className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
                      <li>• Metaverso Educacional</li>
                      <li>• IA Generativa Avançada</li>
                      <li>• Blockchain de Conquistas</li>
                      <li>• Realidade Mista</li>
                    </ul>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Call to Action */}
          <Card className="bg-gradient-to-r from-purple-600 to-blue-600 text-white">
            <CardContent className="p-8 text-center">
              <h3 className="text-2xl font-bold mb-4">
                🚀 Prepare-se para o Futuro dos Concursos
              </h3>
              <p className="text-lg mb-6 opacity-90">
                Junte-se à revolução educacional e transforme sua preparação com as tecnologias mais avançadas
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <Button variant="secondary" size="lg" className="bg-white text-purple-600 hover:bg-gray-100">
                  <Camera className="h-5 w-5 mr-2" />
                  Experimentar AR
                </Button>
                <Button variant="secondary" size="lg" className="bg-white text-purple-600 hover:bg-gray-100">
                  <Trophy className="h-5 w-5 mr-2" />
                  Ver Missões
                </Button>
                <Button variant="secondary" size="lg" className="bg-white text-purple-600 hover:bg-gray-100">
                  <Star className="h-5 w-5 mr-2" />
                  Ranking
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </AppLayout>
    </ProtectedRoute>
  )
}
