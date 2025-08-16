'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Progress } from '@/components/ui/Progress'
import { Trophy, Star, Target, Clock, Gift, Users, Calendar } from 'lucide-react'
import { cn } from '@/lib/utils/cn'
import { mockMissions, mockEvents, mockLeaderboard } from '@/data/mockData'

interface Mission {
  id: string
  title: string
  description: string
  type: 'daily' | 'weekly' | 'special' | 'seasonal'
  category: 'study' | 'social' | 'achievement' | 'exploration'
  difficulty: 'easy' | 'medium' | 'hard' | 'epic'
  points: number
  progress: number
  maxProgress: number
  reward: string
  expiresAt?: Date
  isCompleted: boolean
  isActive: boolean
}

interface Event {
  id: string
  name: string
  description: string
  type: 'tournament' | 'challenge' | 'collaboration' | 'celebration'
  startDate: Date
  endDate: Date
  participants: number
  maxParticipants: number
  rewards: string[]
  isActive: boolean
  isJoined: boolean
}

interface LeaderboardEntry {
  id: string
  username: string
  avatar: string
  points: number
  level: number
  rank: number
  streak: number
  achievements: number
}

interface AdvancedGamificationProps {
  className?: string
  userId?: string
}

export const AdvancedGamification: React.FC<AdvancedGamificationProps> = ({
  className
}) => {
  const [missions, setMissions] = useState<Mission[]>([])
  const [events, setEvents] = useState<Event[]>([])
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [selectedTab, setSelectedTab] = useState<'missions' | 'events' | 'leaderboard'>('missions')
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  

  useEffect(() => {
    setMissions(mockMissions)
    setEvents(mockEvents)
    setLeaderboard(mockLeaderboard)
  }, [])

  const joinEvent = (eventId: string) => {
    setEvents(prev => prev.map(event => 
      event.id === eventId 
        ? { ...event, isJoined: true, participants: event.participants + 1 }
        : event
    ))
  }

  const leaveEvent = (eventId: string) => {
    setEvents(prev => prev.map(event => 
      event.id === eventId 
        ? { ...event, isJoined: false, participants: event.participants - 1 }
        : event
    ))
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'hard': return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400'
      case 'epic': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'daily': return <Calendar className="h-4 w-4" />
      case 'weekly': return <Clock className="h-4 w-4" />
      case 'special': return <Star className="h-4 w-4" />
      case 'seasonal': return <Gift className="h-4 w-4" />
      default: return <Target className="h-4 w-4" />
    }
  }

  const getEventTypeIcon = (type: string) => {
    switch (type) {
      case 'tournament': return <Trophy className="h-4 w-4" />
      case 'challenge': return <Target className="h-4 w-4" />
      case 'collaboration': return <Users className="h-4 w-4" />
      case 'celebration': return <Gift className="h-4 w-4" />
      default: return <Star className="h-4 w-4" />
    }
  }

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'study': return 'Estudo'
      case 'social': return 'Social'
      case 'achievement': return 'Conquista'
      case 'exploration': return 'Exploração'
      default: return 'Geral'
    }
  }

  const categories = [
    { value: 'all', label: 'Todas as Categorias' },
    { value: 'study', label: 'Estudo' },
    { value: 'social', label: 'Social' },
    { value: 'achievement', label: 'Conquista' },
    { value: 'exploration', label: 'Exploração' }
  ]

  const filteredMissions = selectedCategory === 'all' 
    ? missions 
    : missions.filter(mission => mission.category === selectedCategory)

  const tabs = [
    { id: 'missions', label: 'Missões', icon: <Target className="h-4 w-4" /> },
    { id: 'events', label: 'Eventos', icon: <Trophy className="h-4 w-4" /> },
    { id: 'leaderboard', label: 'Ranking', icon: <Star className="h-4 w-4" /> }
  ]

  return (
    <div className={cn('space-y-6', className)}>
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center space-x-3">
          <div className="p-3 bg-gradient-to-r from-yellow-100 to-orange-100 dark:from-yellow-900/20 dark:to-orange-900/20 rounded-full">
            <Trophy className="h-8 w-8 text-yellow-600 dark:text-yellow-400" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Gamificação Avançada
          </h1>
        </div>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Missões, eventos e competições para tornar seus estudos mais envolventes
        </p>
      </div>

      {/* Tab Navigation */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-2">
            {tabs.map((tab) => (
              <Button
                key={tab.id}
                variant={selectedTab === tab.id ? 'primary' : 'secondary'}
                onClick={() => setSelectedTab(tab.id as 'missions' | 'events' | 'leaderboard')}
                className="flex items-center space-x-2"
              >
                {tab.icon}
                <span>{tab.label}</span>
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Missions Tab */}
      {selectedTab === 'missions' && (
        <div className="space-y-6">
          {/* Category Filter */}
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-wrap gap-2">
                {categories.map((category) => (
                  <Button
                    key={category.value}
                    variant={selectedCategory === category.value ? 'primary' : 'secondary'}
                    onClick={() => setSelectedCategory(category.value)}
                    size="sm"
                  >
                    {category.label}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Missions Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {filteredMissions.map((mission) => (
              <Card key={mission.id} className="relative overflow-hidden">
                {mission.isCompleted && (
                  <div className="absolute top-0 right-0 bg-green-500 text-white px-2 py-1 text-xs rounded-bl-lg">
                    ✅ Concluída
                  </div>
                )}
                
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-2">
                      {getTypeIcon(mission.type)}
                      <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                        {mission.type === 'daily' ? 'Diária' : 
                         mission.type === 'weekly' ? 'Semanal' : 
                         mission.type === 'special' ? 'Especial' : 'Sazonal'}
                      </span>
                    </div>
                    <span className={cn(
                      'text-xs px-2 py-1 rounded-full',
                      getDifficultyColor(mission.difficulty)
                    )}>
                      {mission.difficulty === 'easy' ? 'Fácil' : 
                       mission.difficulty === 'medium' ? 'Médio' : 
                       mission.difficulty === 'hard' ? 'Difícil' : 'Épico'}
                    </span>
                  </div>
                  <CardTitle className="text-lg">{mission.title}</CardTitle>
                </CardHeader>
                
                <CardContent className="space-y-4">
                  <p className="text-gray-600 dark:text-gray-400">
                    {mission.description}
                  </p>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progresso</span>
                      <span>{mission.progress}/{mission.maxProgress}</span>
                    </div>
                    <Progress 
                      value={(mission.progress / mission.maxProgress) * 100} 
                      className="h-2"
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600 dark:text-gray-400">Categoria:</span>
                      <div className="font-medium">{getCategoryLabel(mission.category)}</div>
                    </div>
                    <div>
                      <span className="text-gray-600 dark:text-gray-400">Pontos:</span>
                      <div className="font-medium text-yellow-600 dark:text-yellow-400">
                        {mission.points} pts
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Recompensa:
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {mission.reward}
                    </p>
                  </div>
                  
                  <Button
                    disabled={mission.isCompleted}
                    className="w-full"
                    variant={mission.isCompleted ? 'secondary' : 'primary'}
                  >
                    {mission.isCompleted ? 'Missão Concluída' : 'Continuar Missão'}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Events Tab */}
      {selectedTab === 'events' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {events.map((event) => (
              <Card key={event.id} className="relative overflow-hidden">
                {event.isActive && (
                  <div className="absolute top-0 right-0 bg-green-500 text-white px-2 py-1 text-xs rounded-bl-lg">
                    🟢 Ativo
                  </div>
                )}
                
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-2">
                      {getEventTypeIcon(event.type)}
                      <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                        {event.type === 'tournament' ? 'Torneio' : 
                         event.type === 'challenge' ? 'Desafio' : 
                         event.type === 'collaboration' ? 'Colaboração' : 'Celebração'}
                      </span>
                    </div>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {event.participants}/{event.maxParticipants} participantes
                    </span>
                  </div>
                  <CardTitle className="text-lg">{event.name}</CardTitle>
                </CardHeader>
                
                <CardContent className="space-y-4">
                  <p className="text-gray-600 dark:text-gray-400">
                    {event.description}
                  </p>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600 dark:text-gray-400">Início:</span>
                      <div className="font-medium">
                        {event.startDate.toLocaleDateString('pt-BR')}
                      </div>
                    </div>
                    <div>
                      <span className="text-gray-600 dark:text-gray-400">Fim:</span>
                      <div className="font-medium">
                        {event.endDate.toLocaleDateString('pt-BR')}
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Recompensas:
                    </h4>
                    <ul className="space-y-1">
                      {event.rewards.map((reward, index) => (
                        <li key={`${event.id}-reward-${index}`} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                          <span className="text-yellow-500 mr-2">•</span>
                          {reward}
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <Button
                    onClick={() => event.isJoined ? leaveEvent(event.id) : joinEvent(event.id)}
                    variant={event.isJoined ? 'secondary' : 'primary'}
                    className="w-full"
                    disabled={!event.isActive}
                  >
                    {event.isJoined ? 'Sair do Evento' : 'Participar do Evento'}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Leaderboard Tab */}
      {selectedTab === 'leaderboard' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Star className="h-5 w-5 mr-2 text-yellow-500" />
                Ranking da Comunidade
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {leaderboard.map((entry) => (
                  <div key={entry.id} className="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full text-white font-bold text-lg">
                      {entry.rank}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gray-300 dark:bg-gray-600 rounded-full flex items-center justify-center">
                          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            {entry.username.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900 dark:text-white">
                            {entry.username}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            Nível {entry.level}
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-right space-y-1">
                      <div className="text-lg font-bold text-yellow-600 dark:text-yellow-400">
                        {entry.points.toLocaleString()} pts
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        Streak: {entry.streak} dias
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        {entry.achievements} conquistas
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Stats Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Resumo da Gamificação</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {missions.filter(m => m.isCompleted).length}
              </div>
              <p className="text-sm text-blue-600 dark:text-blue-400">Missões Concluídas</p>
            </div>
            
            <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {events.filter(e => e.isJoined).length}
              </div>
              <p className="text-sm text-green-600 dark:text-green-400">Eventos Ativos</p>
            </div>
            
            <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {missions.filter(m => m.isActive && !m.isCompleted).length}
              </div>
              <p className="text-sm text-purple-600 dark:text-purple-400">Missões Pendentes</p>
            </div>
            
            <div className="text-center p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
              <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                {missions.reduce((sum, m) => sum + m.points, 0)}
              </div>
              <p className="text-sm text-orange-600 dark:text-orange-400">Total de Pontos</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
