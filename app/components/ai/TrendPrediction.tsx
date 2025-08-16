'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Brain, TrendingUp, BarChart3 } from 'lucide-react'
import { cn } from '../../lib/utils/cn'
import { mockTrendPredictions, mockMarketTrends, mockLearningPredictions } from '../../data/mockData'

interface TrendPrediction {
  id: string
  category: 'subject' | 'career' | 'market' | 'learning' | 'technology'
  title: string
  description: string
  confidence: number
  timeframe: 'short_term' | 'medium_term' | 'long_term'
  impact: 'high' | 'medium' | 'low'
  probability: number
  recommendations: string[]
  lastUpdated: Date
}

interface MarketTrend {
  id: string
  subject: string
  trend: 'rising' | 'stable' | 'declining'
  demand: number
  salary_range: string
  opportunities: number
  growth_rate: number
}

interface LearningPrediction {
  id: string
  subject: string
  predicted_performance: number
  difficulty_trend: 'increasing' | 'stable' | 'decreasing'
  study_time_recommendation: number
  next_milestone: string
  estimated_completion: Date
}

interface TrendPredictionProps {
  className?: string
  userId?: string
}

export const TrendPrediction: React.FC<TrendPredictionProps> = ({
  className
}) => {
  const [predictions, setPredictions] = useState<TrendPrediction[]>([])
  const [marketTrends, setMarketTrends] = useState<MarketTrend[]>([])
  const [learningPredictions, setLearningPredictions] = useState<LearningPrediction[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('all')
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  

  useEffect(() => {
    setPredictions(mockTrendPredictions)
    setMarketTrends(mockMarketTrends)
    setLearningPredictions(mockLearningPredictions)
  }, [])

  const runPredictionAnalysis = async () => {
    setIsAnalyzing(true)
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    const newPrediction: TrendPrediction = {
      id: Date.now().toString(),
      category: 'technology',
      title: 'Blockchain em Concursos Públicos',
      description: 'Tecnologia blockchain será integrada em processos seletivos nos próximos 3 anos',
      confidence: 0.79,
      timeframe: 'medium_term',
      impact: 'medium',
      probability: 0.75,
      recommendations: [
        'Entenda os conceitos básicos de blockchain',
        'Monitore inovações em processos seletivos',
        'Prepare-se para mudanças tecnológicas'
      ],
      lastUpdated: new Date()
    }
    
    setPredictions(prev => [newPrediction, ...prev.slice(0, 9)])
    setIsAnalyzing(false)
  }

  const getTimeframeLabel = (timeframe: string) => {
    switch (timeframe) {
      case 'short_term': return 'Curto Prazo (6 meses)'
      case 'medium_term': return 'Médio Prazo (1-2 anos)'
      case 'long_term': return 'Longo Prazo (3-5 anos)'
      default: return 'Todos os Prazos'
    }
  }

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'subject': return 'Matérias'
      case 'career': return 'Carreira'
      case 'market': return 'Mercado'
      case 'learning': return 'Aprendizagem'
      case 'technology': return 'Tecnologia'
      default: return 'Todas as Categorias'
    }
  }

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'low': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'rising': return 'text-green-600 dark:text-green-400'
      case 'stable': return 'text-blue-600 dark:text-blue-400'
      case 'declining': return 'text-red-600 dark:text-red-400'
      default: return 'text-gray-600 dark:text-gray-400'
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'rising': return <TrendingUp className="h-4 w-4" />
      case 'stable': return <BarChart3 className="h-4 w-4" />
      case 'declining': return <TrendingUp className="h-4 w-4 transform rotate-180" />
      default: return <BarChart3 className="h-4 w-4" />
    }
  }

  const filteredPredictions = predictions.filter(prediction => {
    const timeframeMatch = selectedTimeframe === 'all' || prediction.timeframe === selectedTimeframe
    const categoryMatch = selectedCategory === 'all' || prediction.category === selectedCategory
    return timeframeMatch && categoryMatch
  })

  const timeframes = [
    { value: 'all', label: 'Todos os Prazos' },
    { value: 'short_term', label: 'Curto Prazo (6 meses)' },
    { value: 'medium_term', label: 'Médio Prazo (1-2 anos)' },
    { value: 'long_term', label: 'Longo Prazo (3-5 anos)' }
  ]

  const categories = [
    { value: 'all', label: 'Todas as Categorias' },
    { value: 'subject', label: 'Matérias' },
    { value: 'career', label: 'Carreira' },
    { value: 'market', label: 'Mercado' },
    { value: 'learning', label: 'Aprendizagem' },
    { value: 'technology', label: 'Tecnologia' }
  ]

  return (
    <div className={cn('space-y-6', className)}>
      {/* Header with Analysis Button */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Predição de Tendências Educacionais
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Análise preditiva de tendências em concursos públicos e mercado educacional
          </p>
        </div>
        
        <Button
          onClick={runPredictionAnalysis}
          disabled={isAnalyzing}
          loading={isAnalyzing}
          className="flex items-center"
        >
          <Brain className="h-4 w-4 mr-2" />
          {isAnalyzing ? 'Analisando...' : 'Nova Análise'}
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Prazo
              </label>
              <select 
                value={selectedTimeframe}
                onChange={(e) => setSelectedTimeframe(e.target.value)}
                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              >
                {timeframes.map((timeframe) => (
                  <option key={timeframe.value} value={timeframe.value}>
                    {timeframe.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Categoria
              </label>
              <select 
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              >
                {categories.map((category) => (
                  <option key={category.value} value={category.value}>
                    {category.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Trend Predictions */}
      <div className="space-y-6">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
          Predições de Tendências ({filteredPredictions.length})
        </h3>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredPredictions.map((prediction) => (
            <Card key={prediction.id} className="relative overflow-hidden">
              <div className={cn(
                'absolute top-0 left-0 w-1 h-full',
                prediction.impact === 'high' ? 'bg-red-500' : 
                prediction.impact === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
              )} />
              
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      {getCategoryLabel(prediction.category)}
                    </span>
                  </div>
                  <span className={cn(
                    'text-xs px-2 py-1 rounded-full',
                    getImpactColor(prediction.impact)
                  )}>
                    Impacto {prediction.impact === 'high' ? 'Alto' : 
                             prediction.impact === 'medium' ? 'Médio' : 'Baixo'}
                  </span>
                </div>
                <CardTitle className="text-lg">{prediction.title}</CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <p className="text-gray-600 dark:text-gray-400">
                  {prediction.description}
                </p>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Confiança</span>
                      <span>{Math.round(prediction.confidence * 100)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div 
                        className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${prediction.confidence * 100}%` }}
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Probabilidade</span>
                      <span>{Math.round(prediction.probability * 100)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div 
                        className="bg-green-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${prediction.probability * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Recomendações:
                  </h4>
                  <ul className="space-y-1">
                    {prediction.recommendations.map((rec, index) => (
                      <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                        <span className="text-primary-500 mr-2">•</span>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                  <span>{getTimeframeLabel(prediction.timeframe)}</span>
                  <span>{prediction.lastUpdated.toLocaleDateString('pt-BR')}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Market Trends */}
      <div className="space-y-6">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
          Tendências de Mercado
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {marketTrends.map((trend) => (
            <Card key={trend.id}>
              <CardContent className="p-4 text-center">
                <div className="flex items-center justify-center space-x-2 mb-3">
                  <span className={cn('text-sm font-medium', getTrendColor(trend.trend))}>
                    {trend.subject}
                  </span>
                  <div className={cn(getTrendColor(trend.trend))}>
                    {getTrendIcon(trend.trend)}
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">
                    {trend.demand}%
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Demanda</p>
                  
                  <div className="text-lg font-semibold text-primary-600 dark:text-primary-400">
                    {trend.salary_range}
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Faixa Salarial</p>
                  
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    {trend.opportunities} oportunidades
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Learning Predictions */}
      <div className="space-y-6">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
          Predições de Aprendizagem
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {learningPredictions.map((prediction) => (
            <Card key={prediction.id}>
              <CardHeader>
                <CardTitle className="text-lg">{prediction.subject}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Performance Prevista</span>
                    <span>{prediction.predicted_performance}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${prediction.predicted_performance}%` }}
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Tendência de Dificuldade</span>
                    <span className={cn(
                      'text-xs px-2 py-1 rounded-full',
                      prediction.difficulty_trend === 'increasing' ? 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400' :
                      prediction.difficulty_trend === 'decreasing' ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400' :
                      'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
                    )}>
                      {prediction.difficulty_trend === 'increasing' ? 'Aumentando' :
                       prediction.difficulty_trend === 'decreasing' ? 'Diminuindo' : 'Estável'}
                    </span>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Tempo de Estudo Recomendado</span>
                    <span className="font-medium">{prediction.study_time_recommendation}h/dia</span>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span>Próximo Milestone</span>
                    <span className="font-medium">{prediction.next_milestone}</span>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span>Conclusão Estimada</span>
                    <span className="font-medium">{prediction.estimated_completion.toLocaleDateString('pt-BR')}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Summary Stats */}
      <Card>
        <CardHeader>
          <CardTitle>Resumo das Predições</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {predictions.length}
              </div>
              <p className="text-sm text-blue-600 dark:text-blue-400">Predições Ativas</p>
            </div>
            
            <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {Math.round(predictions.reduce((sum, p) => sum + p.confidence, 0) / predictions.length * 100)}%
              </div>
              <p className="text-sm text-green-600 dark:text-green-400">Confiança Média</p>
            </div>
            
            <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {predictions.filter(p => p.impact === 'high').length}
              </div>
              <p className="text-sm text-purple-600 dark:text-purple-400">Alto Impacto</p>
            </div>
            
            <div className="text-center p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
              <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                {Math.round(predictions.reduce((sum, p) => sum + p.probability, 0) / predictions.length * 100)}%
              </div>
              <p className="text-sm text-orange-600 dark:text-orange-400">Probabilidade Média</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
