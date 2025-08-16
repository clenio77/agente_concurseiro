'use client'

import React, { useState } from 'react'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { AppLayout } from '@/components/layout/AppLayout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Select } from '@/components/ui/Select'
import { Achievement } from '@/components/gamification/Achievement'
import { LevelSystem } from '@/components/gamification/LevelSystem'
import { Trophy, Target, Star, Zap, Filter } from 'lucide-react'

// Forçar renderização dinâmica para evitar erro de build estático
export const dynamic = 'force-dynamic'
export const revalidate = 0

// Dados mock para demonstração
const mockAchievements = [
  {
    id: '1',
    title: 'Primeiro Passo',
    description: 'Complete sua primeira sessão de estudo',
    icon: 'star' as const,
    category: 'study' as const,
    points: 50,
    isUnlocked: true,
    unlockedAt: new Date('2024-01-10'),
    rarity: 'common' as const
  },
  {
    id: '2',
    title: 'Estudante Dedicado',
    description: 'Estude por 7 dias seguidos',
    icon: 'zap' as const,
    category: 'streak' as const,
    points: 100,
    isUnlocked: true,
    unlockedAt: new Date('2024-01-15'),
    rarity: 'rare' as const
  },
  {
    id: '3',
    title: 'Mestre dos Flashcards',
    description: 'Complete 100 flashcards',
    icon: 'brain' as const,
    category: 'mastery' as const,
    points: 200,
    isUnlocked: false,
    progress: 75,
    maxProgress: 100,
    rarity: 'epic' as const
  },
  {
    id: '4',
    title: 'Quiz Perfeito',
    description: 'Acerte todas as questões de um quiz',
    icon: 'trophy' as const,
    category: 'study' as const,
    points: 150,
    isUnlocked: false,
    rarity: 'rare' as const
  },
  {
    id: '5',
    title: 'Especialista',
    description: 'Alcance nível 50',
    icon: 'target' as const,
    category: 'mastery' as const,
    points: 500,
    isUnlocked: false,
    rarity: 'legendary' as const
  },
  {
    id: '6',
    title: 'Social Butterfly',
    description: 'Conecte-se com 10 outros estudantes',
    icon: 'star' as const,
    category: 'social' as const,
    points: 75,
    isUnlocked: false,
    rarity: 'common' as const
  }
]

const mockLevelData = {
  currentLevel: 15,
  currentPoints: 1250,
  pointsToNextLevel: 2000,
  totalPoints: 1250,
  streak: 7,
  achievements: 2,
  rank: 'bronze' as const
}

const categories = [
  { value: 'all', label: 'Todas as categorias' },
  { value: 'study', label: 'Estudo' },
  { value: 'streak', label: 'Sequência' },
  { value: 'mastery', label: 'Maestria' },
  { value: 'social', label: 'Social' },
  { value: 'special', label: 'Especial' }
]

const rarities = [
  { value: 'all', label: 'Todas as raridades' },
  { value: 'common', label: 'Comum' },
  { value: 'rare', label: 'Raro' },
  { value: 'epic', label: 'Épico' },
  { value: 'legendary', label: 'Lendário' }
]

export default function AchievementsPage() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedRarity, setSelectedRarity] = useState('all')
  const [showUnlockedOnly, setShowUnlockedOnly] = useState(false)
  const [viewMode, setViewMode] = useState<'achievements' | 'level'>('achievements')

  const filteredAchievements = mockAchievements.filter(achievement => {
    const categoryMatch = selectedCategory === 'all' || achievement.category === selectedCategory
    const rarityMatch = selectedRarity === 'all' || achievement.rarity === selectedRarity
    const unlockedMatch = !showUnlockedOnly || achievement.isUnlocked
    
    return categoryMatch && rarityMatch && unlockedMatch
  })

  const unlockedAchievements = mockAchievements.filter(a => a.isUnlocked)
  const totalPoints = unlockedAchievements.reduce((sum, a) => sum + a.points, 0)

  const handleAchievementClick = (achievement: typeof mockAchievements[0]) => {
    if (achievement.isUnlocked) {
      // Mostrar detalhes da conquista
      console.log('Achievement clicked:', achievement)
    }
  }

  return (
    <ProtectedRoute>
      <AppLayout>
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Conquistas e Progresso
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                Acompanhe seu progresso e desbloqueie conquistas
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                  {totalPoints.toLocaleString()}
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  Total de Pontos
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {unlockedAchievements.length}/{mockAchievements.length}
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  Conquistas
                </div>
              </div>
            </div>
          </div>

          {/* View Mode Toggle */}
          <div className="flex space-x-2">
            <Button
              variant={viewMode === 'achievements' ? 'primary' : 'secondary'}
              onClick={() => setViewMode('achievements')}
              className="flex items-center"
            >
              <Trophy className="h-4 w-4 mr-2" />
              Conquistas
            </Button>
            <Button
              variant={viewMode === 'level' ? 'primary' : 'secondary'}
              onClick={() => setViewMode('level')}
              className="flex items-center"
            >
              <Target className="h-4 w-4 mr-2" />
              Níveis
            </Button>
          </div>

          {viewMode === 'achievements' && (
            <>
              {/* Filters */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Filter className="h-5 w-5 mr-2" />
                    Filtros
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Categoria
                      </label>
                      <Select
                        options={categories}
                        value={selectedCategory}
                        onChange={setSelectedCategory}
                        placeholder="Selecione a categoria"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Raridade
                      </label>
                      <Select
                        options={rarities}
                        value={selectedRarity}
                        onChange={setSelectedRarity}
                        placeholder="Selecione a raridade"
                      />
                    </div>
                    
                    <div className="flex items-end">
                      <Button
                        variant={showUnlockedOnly ? 'primary' : 'secondary'}
                        onClick={() => setShowUnlockedOnly(!showUnlockedOnly)}
                        className="w-full"
                      >
                        {showUnlockedOnly ? 'Mostrar Todas' : 'Apenas Desbloqueadas'}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Achievements Grid */}
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Conquistas ({filteredAchievements.length})
                  </h2>
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    {unlockedAchievements.length} de {mockAchievements.length} desbloqueadas
                  </div>
                </div>

                {filteredAchievements.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredAchievements.map((achievement) => (
                      <Achievement
                        key={achievement.id}
                        achievement={achievement}
                        onClick={() => handleAchievementClick(achievement)}
                      />
                    ))}
                  </div>
                ) : (
                  <Card>
                    <CardContent className="p-12 text-center">
                      <Trophy className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                        Nenhuma conquista encontrada
                      </h3>
                      <p className="text-gray-600 dark:text-gray-400">
                        Tente ajustar os filtros ou continue estudando para desbloquear novas conquistas!
                      </p>
                    </CardContent>
                  </Card>
                )}
              </div>
            </>
          )}

          {viewMode === 'level' && (
            <LevelSystem levelData={mockLevelData} />
          )}

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4 text-center">
                <div className="flex items-center justify-center w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-full mx-auto mb-3">
                  <Star className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="text-2xl font-bold text-gray-900 dark:text-white">
                  {mockLevelData.currentLevel}
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Nível Atual
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 text-center">
                <div className="flex items-center justify-center w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-full mx-auto mb-3">
                  <Zap className="h-6 w-6 text-green-600 dark:text-green-400" />
                </div>
                <div className="text-2xl font-bold text-gray-900 dark:text-white">
                  {mockLevelData.streak}
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Dias Seguidos
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 text-center">
                <div className="flex items-center justify-center w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-full mx-auto mb-3">
                  <Trophy className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                </div>
                <div className="text-2xl font-bold text-gray-900 dark:text-white">
                  {unlockedAchievements.length}
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Conquistas
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 text-center">
                <div className="flex items-center justify-center w-12 h-12 bg-orange-100 dark:bg-orange-900/20 rounded-full mx-auto mb-3">
                  <Target className="h-6 w-6 text-orange-600 dark:text-orange-400" />
                </div>
                <div className="text-2xl font-bold text-gray-900 dark:text-white">
                  {Math.round((mockLevelData.currentPoints / mockLevelData.pointsToNextLevel) * 100)}%
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Próximo Nível
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </AppLayout>
    </ProtectedRoute>
  )
}
