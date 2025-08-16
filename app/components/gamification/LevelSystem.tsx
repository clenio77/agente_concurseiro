'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Star, Trophy, Target, Zap } from 'lucide-react'
import { cn } from '../../lib/utils/cn'

interface LevelData {
  currentLevel: number
  currentPoints: number
  pointsToNextLevel: number
  totalPoints: number
  streak: number
  achievements: number
  rank: 'bronze' | 'silver' | 'gold' | 'platinum' | 'diamond'
}

interface LevelSystemProps {
  levelData: LevelData
  className?: string
}

export const LevelSystem: React.FC<LevelSystemProps> = ({
  levelData,
  className
}) => {
  const getRankInfo = (rank: string) => {
    switch (rank) {
      case 'bronze':
        return { color: 'bg-amber-600', label: 'Bronze', icon: '🥉' }
      case 'silver':
        return { color: 'bg-gray-400', label: 'Prata', icon: '🥈' }
      case 'gold':
        return { color: 'bg-yellow-500', label: 'Ouro', icon: '🥇' }
      case 'platinum':
        return { color: 'bg-blue-400', label: 'Platina', icon: '💎' }
      case 'diamond':
        return { color: 'bg-purple-500', label: 'Diamante', icon: '💎' }
      default:
        return { color: 'bg-gray-400', label: 'Iniciante', icon: '⭐' }
    }
  }

  const getLevelColor = (level: number) => {
    if (level < 10) return 'bg-green-500'
    if (level < 25) return 'bg-blue-500'
    if (level < 50) return 'bg-purple-500'
    if (level < 100) return 'bg-orange-500'
    return 'bg-red-500'
  }

  const rankInfo = getRankInfo(levelData.rank)
  const progressPercentage = (levelData.currentPoints / levelData.pointsToNextLevel) * 100

  return (
    <div className={cn('space-y-6', className)}>
      {/* Main Level Card */}
      <Card className="relative overflow-hidden">
        <div className={cn(
          'absolute top-0 left-0 w-full h-1',
          getLevelColor(levelData.currentLevel)
        )} />
        
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Nível {levelData.currentLevel}</span>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {levelData.currentPoints}/{levelData.pointsToNextLevel} pts
              </span>
              <div className={cn(
                'w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold',
                getLevelColor(levelData.currentLevel)
              )}>
                {levelData.currentLevel}
              </div>
            </div>
          </CardTitle>
        </CardHeader>
        
        <CardContent className="space-y-4">
          {/* Progress Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400">
              <span>Progresso para o próximo nível</span>
              <span>{Math.round(progressPercentage)}%</span>
            </div>
            <Progress className="w-full h-3" value={progressPercentage} />
          </div>

          {/* Rank Display */}
          <div className="flex items-center justify-center p-4 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 rounded-lg">
            <div className="text-center">
              <div className="text-3xl mb-2">{rankInfo.icon}</div>
              <div className={cn(
                'inline-block px-3 py-1 rounded-full text-white text-sm font-medium mb-2',
                rankInfo.color
              )}>
                {rankInfo.label}
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Continue estudando para subir de rank!
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Total Points */}
        <Card>
          <CardContent className="p-4 text-center">
            <div className="flex items-center justify-center w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-full mx-auto mb-3">
              <Star className="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {levelData.totalPoints.toLocaleString()}
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Total de Pontos
            </p>
          </CardContent>
        </Card>

        {/* Streak */}
        <Card>
          <CardContent className="p-4 text-center">
            <div className="flex items-center justify-center w-12 h-12 bg-orange-100 dark:bg-orange-900/20 rounded-full mx-auto mb-3">
              <Zap className="h-6 w-6 text-orange-600 dark:text-orange-400" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {levelData.streak}
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Dias Seguidos
            </p>
          </CardContent>
        </Card>

        {/* Achievements */}
        <Card>
          <CardContent className="p-4 text-center">
            <div className="flex items-center justify-center w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-full mx-auto mb-3">
              <Trophy className="h-6 w-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {levelData.achievements}
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Conquistas
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Next Milestones */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="h-5 w-5 mr-2" />
            Próximas Metas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { level: levelData.currentLevel + 1, points: levelData.pointsToNextLevel },
              { level: levelData.currentLevel + 5, points: levelData.pointsToNextLevel * 5 },
              { level: levelData.currentLevel + 10, points: levelData.pointsToNextLevel * 10 }
            ].map((milestone, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className={cn(
                    'w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold',
                    getLevelColor(milestone.level)
                  )}>
                    {milestone.level}
                  </div>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Nível {milestone.level}
                  </span>
                </div>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {milestone.points.toLocaleString()} pts
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// Componente Progress simples para a barra de progresso
const Progress: React.FC<{ value: number; className?: string }> = ({ value, className }) => (
  <div className={cn('w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden', className)}>
    <div 
      className="h-full bg-primary-600 transition-all duration-300"
      style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
    />
  </div>
)
