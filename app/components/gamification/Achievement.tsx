'use client'

import React from 'react'
import { Card, CardContent } from '@/components/ui/Card'
import { Trophy, Lock, Star, Target, BookOpen, Brain, Zap } from 'lucide-react'
import { cn } from '@/lib/utils/cn'

interface AchievementData {
  id: string
  title: string
  description: string
  icon: 'trophy' | 'star' | 'target' | 'book' | 'brain' | 'zap'
  category: 'study' | 'streak' | 'mastery' | 'social' | 'special'
  points: number
  isUnlocked: boolean
  unlockedAt?: Date
  progress?: number
  maxProgress?: number
  rarity: 'common' | 'rare' | 'epic' | 'legendary'
}

interface AchievementProps {
  achievement: AchievementData
  onClick?: () => void
  className?: string
}

export const Achievement: React.FC<AchievementProps> = ({
  achievement,
  onClick,
  className
}) => {
  const getIcon = (icon: string) => {
    switch (icon) {
      case 'trophy': return <Trophy className="h-6 w-6" />
      case 'star': return <Star className="h-6 w-6" />
      case 'target': return <Target className="h-6 w-6" />
      case 'book': return <BookOpen className="h-6 w-6" />
      case 'brain': return <Brain className="h-6 w-6" />
      case 'zap': return <Zap className="h-6 w-6" />
      default: return <Trophy className="h-6 w-6" />
    }
  }

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case 'common': return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
      case 'rare': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
      case 'epic': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400'
      case 'legendary': return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const getRarityLabel = (rarity: string) => {
    switch (rarity) {
      case 'common': return 'Comum'
      case 'rare': return 'Raro'
      case 'epic': return 'Épico'
      case 'legendary': return 'Lendário'
      default: return 'Comum'
    }
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'study': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'streak': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
      case 'mastery': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400'
      case 'social': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'special': return 'bg-pink-100 text-pink-800 dark:bg-pink-900/20 dark:text-pink-400'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'study': return 'Estudo'
      case 'streak': return 'Sequência'
      case 'mastery': return 'Maestria'
      case 'social': return 'Social'
      case 'special': return 'Especial'
      default: return 'Geral'
    }
  }

  const progressPercentage = achievement.progress && achievement.maxProgress 
    ? (achievement.progress / achievement.maxProgress) * 100 
    : 0

  return (
    <Card 
      className={cn(
        'relative overflow-hidden transition-all duration-300 hover:shadow-lg',
        achievement.isUnlocked 
          ? 'cursor-pointer hover:scale-105' 
          : 'opacity-60 cursor-not-allowed',
        className
      )}
    >
      <div 
        onClick={achievement.isUnlocked ? onClick : undefined}
        className="cursor-pointer"
      >
        {/* Background Pattern */}
        <div className={cn(
          'absolute inset-0 opacity-5',
          achievement.isUnlocked ? 'bg-gradient-to-br from-primary-400 to-primary-600' : 'bg-gray-400'
        )} />

        <CardContent className="relative p-6">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className={cn(
              'p-3 rounded-full',
              achievement.isUnlocked 
                ? 'bg-primary-100 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-400'
            )}>
              {achievement.isUnlocked ? getIcon(achievement.icon) : <Lock className="h-6 w-6" />}
            </div>
            
            <div className="text-right">
              <span className={cn(
                'text-xs px-2 py-1 rounded-full',
                getRarityColor(achievement.rarity)
              )}>
                {getRarityLabel(achievement.rarity)}
              </span>
              <div className="mt-1">
                <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  +{achievement.points} pts
                </span>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="space-y-3">
            <h3 className={cn(
              'text-lg font-semibold',
              achievement.isUnlocked 
                ? 'text-gray-900 dark:text-white' 
                : 'text-gray-500 dark:text-gray-400'
            )}>
              {achievement.title}
            </h3>
            
            <p className={cn(
              'text-sm',
              achievement.isUnlocked 
                ? 'text-gray-600 dark:text-gray-300' 
                : 'text-gray-400 dark:text-gray-500'
            )}>
              {achievement.description}
            </p>

            {/* Category Badge */}
            <div className="flex items-center justify-between">
              <span className={cn(
                'text-xs px-2 py-1 rounded-full',
                getCategoryColor(achievement.category)
              )}>
                {getCategoryLabel(achievement.category)}
              </span>
              
              {achievement.isUnlocked && achievement.unlockedAt && (
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {achievement.unlockedAt.toLocaleDateString('pt-BR')}
                </span>
              )}
            </div>

            {/* Progress Bar */}
            {achievement.progress !== undefined && achievement.maxProgress && (
              <div className="space-y-2">
                <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
                  <span>Progresso</span>
                  <span>{achievement.progress}/{achievement.maxProgress}</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    className={cn(
                      'h-2 rounded-full transition-all duration-300',
                      achievement.isUnlocked 
                        ? 'bg-primary-600' 
                        : 'bg-gray-400'
                    )}
                    style={{ width: `${progressPercentage}%` }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* Unlock Animation */}
          {achievement.isUnlocked && (
            <div className="absolute top-0 right-0 w-16 h-16 overflow-hidden">
              <div className="absolute top-0 right-0 w-8 h-8 bg-yellow-400 transform rotate-45 translate-x-2 -translate-y-2" />
              <Star className="absolute top-1 right-1 h-4 w-4 text-yellow-600" />
            </div>
          )}
        </CardContent>
      </div>
    </Card>
  )
}
