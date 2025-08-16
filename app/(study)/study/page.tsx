'use client'

import React, { useState } from 'react'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { AppLayout } from '@/components/layout/AppLayout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Select } from '@/components/ui/Select'
import { Flashcard } from '@/components/study/Flashcard'
import { Quiz } from '@/components/study/Quiz'
import { BookOpen, Target, Clock, Trophy, Brain } from 'lucide-react'

// Forçar renderização dinâmica para evitar erro de build estático
export const dynamic = 'force-dynamic'
export const revalidate = 0

// Dados mock para demonstração
const mockFlashcards = [
  {
    id: '1',
    front: 'Qual é a capital do Brasil?',
    back: 'Brasília',
    subject: 'Geografia',
    difficulty: 'easy' as const,
    lastReviewed: new Date('2024-01-15'),
    nextReview: new Date('2024-01-20')
  },
  {
    id: '2',
    front: 'Quem escreveu "Os Lusíadas"?',
    back: 'Luís de Camões',
    subject: 'Literatura',
    difficulty: 'medium' as const,
    lastReviewed: new Date('2024-01-14'),
    nextReview: new Date('2024-01-18')
  },
  {
    id: '3',
    front: 'Qual é a fórmula da água?',
    back: 'H₂O',
    subject: 'Química',
    difficulty: 'easy' as const,
    lastReviewed: new Date('2024-01-13'),
    nextReview: new Date('2024-01-16')
  }
]

const mockQuizQuestions = [
  {
    id: '1',
    question: 'Qual é o maior planeta do sistema solar?',
    options: ['Terra', 'Júpiter', 'Saturno', 'Marte'],
    correctAnswer: 1,
    explanation: 'Júpiter é o maior planeta do sistema solar, com uma massa 318 vezes maior que a da Terra.',
    subject: 'Astronomia',
    difficulty: 'medium' as const
  },
  {
    id: '2',
    question: 'Em que ano o Brasil se tornou independente?',
    options: ['1808', '1822', '1889', '1891'],
    correctAnswer: 1,
    explanation: 'O Brasil se tornou independente de Portugal em 7 de setembro de 1822.',
    subject: 'História',
    difficulty: 'easy' as const
  },
  {
    id: '3',
    question: 'Qual é a capital do estado de São Paulo?',
    options: ['São Paulo', 'Campinas', 'Santos', 'Ribeirão Preto'],
    correctAnswer: 0,
    explanation: 'A capital do estado de São Paulo é a cidade de São Paulo.',
    subject: 'Geografia',
    difficulty: 'easy' as const
  }
]

const studyModes = [
  { value: 'flashcards', label: 'Flashcards' },
  { value: 'quiz', label: 'Quiz' },
  { value: 'mixed', label: 'Misto' }
]

const subjects = [
  { value: 'all', label: 'Todas as matérias' },
  { value: 'matematica', label: 'Matemática' },
  { value: 'portugues', label: 'Português' },
  { value: 'historia', label: 'História' },
  { value: 'geografia', label: 'Geografia' },
  { value: 'ciencias', label: 'Ciências' },
  { value: 'direito', label: 'Direito' }
]

export default function StudyPage() {
  const [studyMode, setStudyMode] = useState('flashcards')
  const [selectedSubject, setSelectedSubject] = useState('all')
  const [currentFlashcardIndex, setCurrentFlashcardIndex] = useState(0)
  const [showResults, setShowResults] = useState(false)
  const [quizResults, setQuizResults] = useState<{ score: number; total: number; timeSpent: number } | null>(null)

  const handleFlashcardAnswer = (quality: 'again' | 'hard' | 'good' | 'easy') => {
    // Aqui você implementaria a lógica do algoritmo de repetição espaçada
    console.log('Flashcard answer:', quality)
    
    // Avançar para o próximo flashcard
    if (currentFlashcardIndex < mockFlashcards.length - 1) {
      setCurrentFlashcardIndex(prev => prev + 1)
    } else {
      // Sessão de flashcards concluída
      setShowResults(true)
    }
  }

  const handleQuizComplete = (score: number, total: number, timeSpent: number) => {
    setQuizResults({ score, total, timeSpent })
    setShowResults(true)
  }

  const resetSession = () => {
    setCurrentFlashcardIndex(0)
    setShowResults(false)
    setQuizResults(null)
  }

  const filteredFlashcards = selectedSubject === 'all' 
    ? mockFlashcards 
    : mockFlashcards.filter(f => f.subject.toLowerCase().includes(selectedSubject))

  const filteredQuizQuestions = selectedSubject === 'all' 
    ? mockQuizQuestions 
    : mockQuizQuestions.filter(q => q.subject.toLowerCase().includes(selectedSubject))

  return (
    <ProtectedRoute>
      <AppLayout>
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Sessão de Estudo
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                Escolha seu modo de estudo e comece a aprender
              </p>
            </div>
            
            <div className="flex items-center space-x-2">
              <Clock className="h-5 w-5 text-gray-400" />
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Tempo de estudo: 0:00
              </span>
            </div>
          </div>

          {/* Study Controls */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Brain className="h-5 w-5 mr-2" />
                Configurações de Estudo
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Modo de Estudo
                  </label>
                  <Select
                    options={studyModes}
                    value={studyMode}
                    onChange={setStudyMode}
                    placeholder="Selecione o modo"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Matéria
                  </label>
                  <Select
                    options={subjects}
                    value={selectedSubject}
                    onChange={setSelectedSubject}
                    placeholder="Selecione a matéria"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between pt-4">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <BookOpen className="h-4 w-4 text-blue-500" />
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {filteredFlashcards.length} flashcards
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Target className="h-4 w-4 text-green-500" />
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {filteredQuizQuestions.length} questões
                    </span>
                  </div>
                </div>

                <Button onClick={resetSession} variant="secondary">
                  Reiniciar Sessão
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Study Content */}
          {!showResults && (
            <div className="space-y-6">
              {studyMode === 'flashcards' && filteredFlashcards.length > 0 && (
                <div className="text-center">
                  <div className="mb-4">
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      Flashcard {currentFlashcardIndex + 1} de {filteredFlashcards.length}
                    </span>
                  </div>
                  {filteredFlashcards[currentFlashcardIndex] && (
                    <Flashcard
                      flashcard={filteredFlashcards[currentFlashcardIndex]!}
                      onAnswer={handleFlashcardAnswer}
                    />
                  )}
                </div>
              )}

              {studyMode === 'quiz' && filteredQuizQuestions.length > 0 && (
                <Quiz
                  questions={filteredQuizQuestions}
                  onComplete={handleQuizComplete}
                  timeLimit={300} // 5 minutos
                />
              )}

              {studyMode === 'mixed' && (
                <div className="space-y-6">
                  <div className="text-center">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                      Flashcards
                    </h3>
                    {filteredFlashcards[currentFlashcardIndex] && (
                      <Flashcard
                        flashcard={filteredFlashcards[currentFlashcardIndex]!}
                        onAnswer={handleFlashcardAnswer}
                      />
                    )}
                  </div>
                  
                  <div className="text-center">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                      Quiz
                    </h3>
                    <Quiz
                      questions={filteredQuizQuestions.slice(0, 2)} // Apenas 2 questões para demonstração
                      onComplete={handleQuizComplete}
                      timeLimit={120}
                    />
                  </div>
                </div>
              )}

              {filteredFlashcards.length === 0 && filteredQuizQuestions.length === 0 && (
                <Card>
                  <CardContent className="p-12 text-center">
                    <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      Nenhum conteúdo disponível
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400">
                      Não há flashcards ou questões para a matéria selecionada.
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>
          )}

          {/* Results */}
          {showResults && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Trophy className="h-5 w-5 mr-2" />
                  Sessão Concluída!
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {quizResults && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                        {quizResults.score}/{quizResults.total}
                      </div>
                      <p className="text-sm text-blue-600 dark:text-blue-400">Acertos</p>
                    </div>
                    <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                      <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                        {Math.round((quizResults.score / quizResults.total) * 100)}%
                      </div>
                      <p className="text-sm text-green-600 dark:text-green-400">Taxa de Acerto</p>
                    </div>
                    <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                        {Math.floor(quizResults.timeSpent / 60)}:{(quizResults.timeSpent % 60).toString().padStart(2, '0')}
                      </div>
                      <p className="text-sm text-purple-600 dark:text-purple-400">Tempo Total</p>
                    </div>
                  </div>
                )}

                <div className="text-center pt-4">
                  <Button onClick={resetSession} size="lg">
                    <BookOpen className="h-4 w-4 mr-2" />
                    Nova Sessão
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </AppLayout>
    </ProtectedRoute>
  )
}
