'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Progress } from '@/components/ui/Progress'
import { Brain, TrendingUp, Target, Clock, BarChart3, Lightbulb, Zap } from 'lucide-react'
import { cn } from '@/lib/utils/cn'
import { mockBehavioralPatterns, mockLearningInsights } from '@/data/mockData'

interface BehavioralPattern {
  id: string
  category: 'study_habits' | 'learning_style' | 'motivation' | 'performance' | 'social'
  pattern: string
  description: string
  confidence: number
  impact: 'positive' | 'negative' | 'neutral'
  recommendations: string[]
  lastUpdated: Date
}

interface LearningInsight {
  id: string
  type: 'strength' | 'improvement' | 'opportunity'
  title: string
  description: string
  actionItems: string[]
  priority: 'high' | 'medium' | 'low'
}

interface BehavioralAnalysisProps {
  className?: string
  userId?: string
}

export const BehavioralAnalysis: React.FC<BehavioralAnalysisProps> = ({
  className
}) => {
  const [patterns, setPatterns] = useState<BehavioralPattern[]>([])
  const [insights, setInsights] = useState<LearningInsight[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<string>('all')


  // Dados mock importados do arquivo centralizado

  useEffect(() => {
    setPatterns(mockBehavioralPatterns)
    setInsights(mockLearningInsights)
  }, [])

  const runAnalysis = async () => {
    setIsAnalyzing(true)
    
    // Simular análise em tempo real
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    // Atualizar padrões com novos insights
    const newPattern: BehavioralPattern = {
      id: Date.now().toString(),
      category: 'performance',
      pattern: 'Melhoria na Retenção',
      description: 'Sua retenção de conteúdo melhorou 23% nos últimos 7 dias',
      confidence: 0.82,
      impact: 'positive',
      recommendations: [
        'Continue com a técnica de repetição espaçada',
        'Aumente gradualmente a dificuldade',
        'Revise conceitos antigos regularmente'
      ],
      lastUpdated: new Date()
    }
    
    setPatterns(prev => [...prev, newPattern])
    setIsAnalyzing(false)
  }

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'study_habits': return 'Hábitos de Estudo'
      case 'learning_style': return 'Estilo de Aprendizagem'
      case 'motivation': return 'Motivação'
      case 'performance': return 'Performance'
      case 'social': return 'Social'
      default: return 'Geral'
    }
  }

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'study_habits': return <Clock className="h-4 w-4" />
      case 'learning_style': return <Brain className="h-4 w-4" />
      case 'motivation': return <Zap className="h-4 w-4" />
      case 'performance': return <TrendingUp className="h-4 w-4" />
      case 'social': return <Target className="h-4 w-4" />
      default: return <BarChart3 className="h-4 w-4" />
    }
  }

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'positive': return 'text-green-600 dark:text-green-400'
      case 'negative': return 'text-red-600 dark:text-red-400'
      case 'neutral': return 'text-gray-600 dark:text-gray-400'
      default: return 'text-gray-600 dark:text-gray-400'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'low': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const filteredPatterns = selectedCategory === 'all' 
    ? patterns 
    : patterns.filter(p => p.category === selectedCategory)

  const categories = [
    { value: 'all', label: 'Todas as Categorias' },
    { value: 'study_habits', label: 'Hábitos de Estudo' },
    { value: 'learning_style', label: 'Estilo de Aprendizagem' },
    { value: 'motivation', label: 'Motivação' },
    { value: 'performance', label: 'Performance' },
    { value: 'social', label: 'Social' }
  ]

  return (
    <div className={cn('space-y-6', className)}>
      {/* Header with Analysis Button */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Análise Comportamental Inteligente
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Insights personalizados sobre seus padrões de estudo e aprendizagem
          </p>
        </div>
        
        <Button
          onClick={runAnalysis}
          disabled={isAnalyzing}
          loading={isAnalyzing}
          className="flex items-center"
        >
          <Brain className="h-4 w-4 mr-2" />
          {isAnalyzing ? 'Analisando...' : 'Nova Análise'}
        </Button>
      </div>

      {/* Category Filter */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <Button
                key={category.value}
                variant={selectedCategory === category.value ? 'primary' : 'secondary'}
                size="sm"
                onClick={() => setSelectedCategory(category.value)}
                className="flex items-center"
              >
                {getCategoryIcon(category.value)}
                <span className="ml-2">{category.label}</span>
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Behavioral Patterns */}
      <div className="space-y-6">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
          Padrões Comportamentais Identificados
        </h3>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredPatterns.map((pattern) => (
            <Card key={pattern.id} className="relative overflow-hidden">
              <div className={cn(
                'absolute top-0 left-0 w-1 h-full',
                pattern.impact === 'positive' ? 'bg-green-500' : 
                pattern.impact === 'negative' ? 'bg-red-500' : 'bg-gray-500'
              )} />
              
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2">
                    {getCategoryIcon(pattern.category)}
                    <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      {getCategoryLabel(pattern.category)}
                    </span>
                  </div>
                  <span className={cn(
                    'text-xs px-2 py-1 rounded-full',
                    getImpactColor(pattern.impact)
                  )}>
                    {pattern.impact === 'positive' ? 'Positivo' : 
                     pattern.impact === 'negative' ? 'Negativo' : 'Neutro'}
                  </span>
                </div>
                <CardTitle className="text-lg">{pattern.pattern}</CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <p className="text-gray-600 dark:text-gray-400">
                  {pattern.description}
                </p>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Confiança da Análise</span>
                    <span>{Math.round(pattern.confidence * 100)}%</span>
                  </div>
                  <Progress value={pattern.confidence * 100} />
                </div>
                
                <div className="space-y-2">
                  <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Recomendações:
                  </h4>
                  <ul className="space-y-1">
                    {pattern.recommendations.map((rec, index) => (
                      <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                        <span className="text-primary-500 mr-2">•</span>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  Última atualização: {pattern.lastUpdated.toLocaleDateString('pt-BR')}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Learning Insights */}
      <div className="space-y-6">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
          Insights de Aprendizagem
        </h3>
        
        <div className="space-y-4">
          {insights.map((insight) => (
            <Card key={insight.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={cn(
                      'p-2 rounded-full',
                      insight.type === 'strength' ? 'bg-green-100 dark:bg-green-900/20' :
                      insight.type === 'improvement' ? 'bg-yellow-100 dark:bg-yellow-900/20' :
                      'bg-blue-100 dark:bg-blue-900/20'
                    )}>
                      {insight.type === 'strength' ? (
                        <TrendingUp className="h-5 w-5 text-green-600 dark:text-green-400" />
                      ) : insight.type === 'improvement' ? (
                        <Target className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
                      ) : (
                        <Lightbulb className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                      )}
                    </div>
                    <div>
                      <CardTitle className="text-lg">{insight.title}</CardTitle>
                      <span className={cn(
                        'inline-block px-2 py-1 rounded-full text-xs font-medium mt-2',
                        getPriorityColor(insight.priority)
                      )}>
                        Prioridade {insight.priority === 'high' ? 'Alta' : 
                                   insight.priority === 'medium' ? 'Média' : 'Baixa'}
                      </span>
                    </div>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <p className="text-gray-600 dark:text-gray-400">
                  {insight.description}
                </p>
                
                <div className="space-y-2">
                  <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Ações Recomendadas:
                  </h4>
                  <ul className="space-y-1">
                    {insight.actionItems.map((action, index) => (
                      <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                        <span className="text-primary-500 mr-2">•</span>
                        {action}
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Summary Stats */}
      <Card>
        <CardHeader>
          <CardTitle>Resumo da Análise</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {patterns.filter(p => p.impact === 'positive').length}
              </div>
              <p className="text-sm text-green-600 dark:text-green-400">Padrões Positivos</p>
            </div>
            
            <div className="text-center p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
              <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                {patterns.filter(p => p.impact === 'negative').length}
              </div>
              <p className="text-sm text-red-600 dark:text-red-400">Áreas de Melhoria</p>
            </div>
            
            <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {insights.length}
              </div>
              <p className="text-sm text-blue-600 dark:text-blue-400">Insights Gerados</p>
            </div>
            
            <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {Math.round(patterns.reduce((sum, p) => sum + p.confidence, 0) / patterns.length * 100)}%
              </div>
              <p className="text-sm text-purple-600 dark:text-purple-400">Confiança Média</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
