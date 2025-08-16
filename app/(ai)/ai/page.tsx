'use client'

import React, { useState } from 'react'
import { VoiceAssistant } from '@/components/ai/VoiceAssistant'
import { BehavioralAnalysis } from '@/components/ai/BehavioralAnalysis'
import { TrendPrediction } from '@/components/ai/TrendPrediction'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { AppLayout } from '@/components/layout/AppLayout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Brain, Mic, BarChart3, TrendingUp, Zap, Lightbulb } from 'lucide-react'

export const dynamic = 'force-dynamic'
export const revalidate = 0

export default function AIPage() {
  const [activeTab, setActiveTab] = useState<'voice' | 'behavioral' | 'trends'>('voice')
  const [lastCommand, setLastCommand] = useState('')
  const [lastResponse, setLastResponse] = useState('')

  const handleVoiceCommand = (command: string, response: string) => {
    setLastCommand(command)
    setLastResponse(response)
  }

  const tabs = [
    {
      id: 'voice',
      label: 'Assistente de Voz',
      icon: <Mic className="h-5 w-5" />,
      description: 'Controle por voz e comandos inteligentes'
    },
    {
      id: 'behavioral',
      label: 'Análise Comportamental',
      icon: <BarChart3 className="h-5 w-5" />,
      description: 'Insights sobre seus padrões de estudo'
    },
    {
      id: 'trends',
      label: 'Predição de Tendências',
      icon: <TrendingUp className="h-5 w-5" />,
      description: 'Análise preditiva do mercado educacional'
    }
  ]

  const renderActiveComponent = () => {
    switch (activeTab) {
      case 'voice':
        return <VoiceAssistant onCommandProcessed={handleVoiceCommand} />
      case 'behavioral':
        return <BehavioralAnalysis />
      case 'trends':
        return <TrendPrediction />
      default:
        return <VoiceAssistant onCommandProcessed={handleVoiceCommand} />
    }
  }

  return (
    <ProtectedRoute>
      <AppLayout>
        <div className="space-y-6">
          {/* Header */}
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center space-x-3">
              <div className="p-3 bg-primary-100 dark:bg-primary-900/20 rounded-full">
                <Brain className="h-8 w-8 text-primary-600 dark:text-primary-400" />
              </div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Inteligência Artificial
              </h1>
            </div>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Explore o poder da IA para revolucionar sua preparação para concursos públicos
            </p>
          </div>

          {/* AI Features Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Zap className="h-5 w-5 mr-2 text-yellow-500" />
                Recursos de IA Disponíveis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-lg border border-blue-200 dark:border-blue-800">
                  <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                    <Mic className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">
                    Assistente de Voz
                  </h3>
                  <p className="text-sm text-blue-700 dark:text-blue-300">
                    Controle por voz, comandos inteligentes e respostas em tempo real
                  </p>
                </div>

                <div className="text-center p-4 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-lg border border-green-200 dark:border-green-800">
                  <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-full w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                    <BarChart3 className="h-8 w-8 text-green-600 dark:text-green-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-green-900 dark:text-green-100 mb-2">
                    Análise Comportamental
                  </h3>
                  <p className="text-sm text-green-700 dark:text-green-300">
                    Insights personalizados sobre seus padrões de estudo e aprendizagem
                  </p>
                </div>

                <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 rounded-lg border border-purple-200 dark:border-purple-800">
                  <div className="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-full w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                    <TrendingUp className="h-8 w-8 text-purple-600 dark:text-purple-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-purple-900 dark:text-purple-100 mb-2">
                    Predição de Tendências
                  </h3>
                  <p className="text-sm text-purple-700 dark:text-purple-300">
                    Análise preditiva do mercado educacional e oportunidades futuras
                  </p>
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
                    onClick={() => setActiveTab(tab.id as 'voice' | 'behavioral' | 'trends')}
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

          {/* Last Voice Command Display */}
          {lastCommand && lastResponse && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Lightbulb className="h-5 w-5 mr-2 text-yellow-500" />
                  Último Comando de Voz Processado
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Mic className="h-4 w-4 text-gray-500" />
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Comando:
                    </span>
                  </div>
                  <p className="text-gray-900 dark:text-white font-medium">&ldquo;{lastCommand}&rdquo;</p>
                </div>

                <div className="p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Brain className="h-4 w-4 text-primary-500" />
                    <span className="text-sm font-medium text-primary-700 dark:text-primary-300">
                      Resposta da IA:
                    </span>
                  </div>
                  <p className="text-primary-900 dark:text-primary-100">{lastResponse}</p>
                </div>
              </CardContent>
            </Card>
          )}

          {/* AI Tips */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Lightbulb className="h-5 w-5 mr-2 text-yellow-500" />
                Dicas para Usar a IA
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    🎯 Assistente de Voz
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• Use comandos claros e diretos</li>
                    <li>• Fale em português brasileiro</li>
                    <li>• Aguarde o processamento antes de falar novamente</li>
                    <li>• Use os botões de comando rápido para testes</li>
                  </ul>
                </div>

                <div className="space-y-3">
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    🧠 Análise Comportamental
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• Execute análises regularmente</li>
                    <li>• Filtre por categorias específicas</li>
                    <li>• Siga as recomendações personalizadas</li>
                    <li>• Monitore seu progresso ao longo do tempo</li>
                  </ul>
                </div>

                <div className="space-y-3">
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    📈 Predição de Tendências
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• Filtre por prazo e categoria</li>
                    <li>• Foque em tendências de alto impacto</li>
                    <li>• Use as predições para planejar estudos</li>
                    <li>• Monitore mudanças no mercado</li>
                  </ul>
                </div>

                <div className="space-y-3">
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    🚀 Melhores Práticas
                  </h4>
                  <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                    <li>• Use a IA como complemento, não substituição</li>
                    <li>• Combine insights de diferentes ferramentas</li>
                    <li>• Ajuste suas estratégias baseado nas análises</li>
                    <li>• Mantenha-se atualizado com novas funcionalidades</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </AppLayout>
    </ProtectedRoute>
  )
}
