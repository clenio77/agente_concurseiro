'use client'

import React, { useState } from 'react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { RotateCcw, Check, X, Eye, EyeOff } from 'lucide-react'
import { cn } from '@/lib/utils/cn'

interface FlashcardData {
  id: string
  front: string
  back: string
  subject: string
  difficulty: 'easy' | 'medium' | 'hard'
  lastReviewed?: Date
  nextReview?: Date
}

interface FlashcardProps {
  flashcard: FlashcardData
  onAnswer: (quality: 'again' | 'hard' | 'good' | 'easy') => void
  className?: string
}

export const Flashcard: React.FC<FlashcardProps> = ({
  flashcard,
  onAnswer,
  className
}) => {
  const [isFlipped, setIsFlipped] = useState(false)
  const [showAnswer, setShowAnswer] = useState(false)

  const handleFlip = () => {
    setIsFlipped(!isFlipped)
    if (!showAnswer) {
      setShowAnswer(true)
    }
  }

  const handleAnswer = (quality: 'again' | 'hard' | 'good' | 'easy') => {
    onAnswer(quality)
    setIsFlipped(false)
    setShowAnswer(false)
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'hard': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  const getDifficultyLabel = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'Fácil'
      case 'medium': return 'Médio'
      case 'hard': return 'Difícil'
      default: return 'N/A'
    }
  }

  return (
    <div className={cn('w-full max-w-md mx-auto', className)}>
      {/* Flashcard */}
      <Card className="relative h-64 cursor-pointer overflow-hidden">
        <CardContent 
          className="h-full p-6 flex flex-col justify-center items-center text-center cursor-pointer"
        >
          <div onClick={handleFlip} className="w-full h-full flex flex-col justify-center items-center">
          {/* Subject Badge */}
          <div className="absolute top-3 left-3">
            <span className="text-xs px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400 rounded-full">
              {flashcard.subject}
            </span>
          </div>

          {/* Difficulty Badge */}
          <div className="absolute top-3 right-3">
            <span className={cn(
              'text-xs px-2 py-1 rounded-full',
              getDifficultyColor(flashcard.difficulty)
            )}>
              {getDifficultyLabel(flashcard.difficulty)}
            </span>
          </div>

          {/* Content */}
          <div className="flex-1 flex items-center justify-center w-full">
            {!isFlipped ? (
              <div className="space-y-4">
                <Eye className="h-8 w-8 mx-auto text-gray-400" />
                <p className="text-lg font-medium text-gray-900 dark:text-white">
                  {flashcard.front}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Clique para ver a resposta
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <EyeOff className="h-8 w-8 mx-auto text-gray-400" />
                <p className="text-lg font-medium text-gray-900 dark:text-white">
                  {flashcard.back}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Como você se saiu?
                </p>
              </div>
            )}
          </div>

          {/* Flip Indicator */}
          <div className="absolute bottom-3 right-3">
            <RotateCcw className="h-4 w-4 text-gray-400" />
          </div>
        </div>
      </CardContent>
      </Card>

      {/* Answer Buttons */}
      {showAnswer && (
        <div className="mt-6 space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <Button
              variant="error"
              size="sm"
              onClick={() => handleAnswer('again')}
              className="w-full"
            >
              <X className="h-4 w-4 mr-2" />
              De novo
            </Button>
            <Button
              variant="warning"
              size="sm"
              onClick={() => handleAnswer('hard')}
              className="w-full"
            >
              Difícil
            </Button>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Button
              variant="success"
              size="sm"
              onClick={() => handleAnswer('good')}
              className="w-full"
            >
              Bom
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={() => handleAnswer('easy')}
              className="w-full"
            >
              <Check className="h-4 w-4 mr-2" />
              Fácil
            </Button>
          </div>
        </div>
      )}

      {/* Progress Info */}
      {flashcard.lastReviewed && (
        <div className="mt-4 text-center text-sm text-gray-500 dark:text-gray-400">
          <p>Última revisão: {flashcard.lastReviewed.toLocaleDateString('pt-BR')}</p>
          {flashcard.nextReview && (
            <p>Próxima revisão: {flashcard.nextReview.toLocaleDateString('pt-BR')}</p>
          )}
        </div>
      )}
    </div>
  )
}
