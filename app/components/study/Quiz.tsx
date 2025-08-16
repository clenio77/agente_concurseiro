'use client'

import React, { useState, useCallback } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Radio } from '@/components/ui/Radio'
import { CheckCircle, XCircle, ArrowRight, Timer } from 'lucide-react'
import { cn } from '../../lib/utils/cn'

interface QuizQuestion {
  id: string
  question: string
  options: string[]
  correctAnswer: number
  explanation?: string
  subject: string
  difficulty: 'easy' | 'medium' | 'hard'
}

interface QuizProps {
  questions: QuizQuestion[]
  onComplete: (score: number, total: number, timeSpent: number) => void
  timeLimit?: number // em segundos
  className?: string
}

export const Quiz: React.FC<QuizProps> = ({
  questions,
  onComplete,
  timeLimit,
  className
}) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showAnswer, setShowAnswer] = useState(false)
  const [answers, setAnswers] = useState<Array<{ questionId: string; selected: number; correct: boolean; timeSpent: number }>>([])
  const [startTime, setStartTime] = useState<number>(Date.now())
  const [timeRemaining, setTimeRemaining] = useState(timeLimit || 0)

  const currentQuestion = questions[currentQuestionIndex]
  const isLastQuestion = currentQuestionIndex === questions.length - 1

  const handleComplete = useCallback(() => {
    const totalTime = Math.floor((Date.now() - startTime) / 1000)
    const correctAnswers = answers.filter(a => a.correct).length
    onComplete(correctAnswers, questions.length, totalTime)
  }, [startTime, answers, questions.length, onComplete])

  // Timer effect
  React.useEffect(() => {
    if (timeLimit && timeRemaining > 0) {
      const timer = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            handleComplete()
            return 0
          }
          return prev - 1
        })
      }, 1000)

      return () => clearInterval(timer)
    }
    return undefined
  }, [timeLimit, timeRemaining, handleComplete])

  const handleAnswerSelect = (answerIndex: number) => {
    setSelectedAnswer(answerIndex)
  }

  const handleSubmitAnswer = () => {
    if (selectedAnswer === null) return

    const timeSpent = Math.floor((Date.now() - startTime) / 1000)
    const isCorrect = selectedAnswer === currentQuestion!.correctAnswer

    setAnswers(prev => [...prev, {
      questionId: currentQuestion!.id,
      selected: selectedAnswer,
      correct: isCorrect,
      timeSpent
    }])

    setShowAnswer(true)
    setStartTime(Date.now()) // Reset timer for next question
  }

  const handleNextQuestion = () => {
    if (isLastQuestion) {
      handleComplete()
    } else {
      setCurrentQuestionIndex(prev => prev + 1)
      setSelectedAnswer(null)
      setShowAnswer(false)
      setStartTime(Date.now())
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
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

  if (questions.length === 0) {
    return (
      <Card className={cn('w-full max-w-2xl mx-auto', className)}>
        <CardContent className="p-6 text-center">
          <p className="text-gray-500 dark:text-gray-400">Nenhuma questão disponível</p>
        </CardContent>
      </Card>
    )
  }

  if (!currentQuestion) {
    return (
      <Card className={cn('w-full max-w-2xl mx-auto', className)}>
        <CardContent className="p-6 text-center">
          <p className="text-gray-500 dark:text-gray-400">Carregando questão...</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className={cn('w-full max-w-2xl mx-auto', className)}>
      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-600 dark:text-gray-400">
            Questão {currentQuestionIndex + 1} de {questions.length}
          </span>
          {timeLimit && (
            <div className="flex items-center space-x-2">
              <Timer className="h-4 w-4 text-gray-400" />
              <span className={cn(
                'text-sm font-medium',
                timeRemaining <= 30 ? 'text-red-600 dark:text-red-400' : 'text-gray-600 dark:text-gray-400'
              )}>
                {formatTime(timeRemaining)}
              </span>
            </div>
          )}
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
          />
        </div>
      </div>

      {/* Question Card */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">
              {currentQuestion.question}
            </CardTitle>
            <span className={cn(
              'text-xs px-2 py-1 rounded-full',
              getDifficultyColor(currentQuestion.difficulty)
            )}>
              {getDifficultyLabel(currentQuestion.difficulty)}
            </span>
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            {currentQuestion.subject}
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Answer Options */}
          <Radio
            options={currentQuestion.options.map((option, index) => ({
              value: index.toString(),
              label: option,
              disabled: showAnswer
            }))}
            value={selectedAnswer?.toString() || ''}
            onChange={(value) => handleAnswerSelect(parseInt(value))}
            name={`question-${currentQuestion.id}`}
          />

          {/* Answer Feedback */}
          {showAnswer && (
            <div className={cn(
              'p-4 rounded-lg border',
              selectedAnswer === currentQuestion.correctAnswer
                ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
            )}>
              <div className="flex items-center space-x-2 mb-2">
                {selectedAnswer === currentQuestion.correctAnswer ? (
                  <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400" />
                ) : (
                  <XCircle className="h-5 w-5 text-red-600 dark:text-red-400" />
                )}
                <span className={cn(
                  'font-medium',
                  selectedAnswer === currentQuestion.correctAnswer
                    ? 'text-green-800 dark:text-green-200'
                    : 'text-red-800 dark:text-red-200'
                )}>
                  {selectedAnswer === currentQuestion.correctAnswer ? 'Correto!' : 'Incorreto'}
                </span>
              </div>
              
              {currentQuestion.explanation && (
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  {currentQuestion.explanation}
                </p>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex justify-end space-x-3 pt-4">
            {!showAnswer ? (
              <Button
                onClick={handleSubmitAnswer}
                disabled={selectedAnswer === null}
                className="min-w-[120px]"
              >
                Responder
              </Button>
            ) : (
              <Button
                onClick={handleNextQuestion}
                className="min-w-[120px]"
              >
                {isLastQuestion ? 'Finalizar' : 'Próxima'}
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
