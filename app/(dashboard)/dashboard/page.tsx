import React from 'react'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { AppLayout } from '@/components/layout/AppLayout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { 
  BookOpen, 
  Target, 
  Trophy, 
  TrendingUp, 
  Clock, 
  Award,
  Calendar,
  BarChart3
} from 'lucide-react'

// Forçar renderização dinâmica para evitar erro de build estático
export const dynamic = 'force-dynamic'

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <AppLayout>
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Dashboard
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                Bem-vindo de volta! Aqui está o resumo do seu progresso.
              </p>
            </div>
            
            <Button>
              <BookOpen className="h-4 w-4 mr-2" />
              Iniciar Estudo
            </Button>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 dark:bg-blue-900/20 rounded-lg">
                    <BookOpen className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      Tempo de Estudo
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      12h 30m
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 dark:bg-green-900/20 rounded-lg">
                    <Target className="h-6 w-6 text-green-600 dark:text-green-400" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      Metas Alcançadas
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      8/12
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
                    <Trophy className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      Pontos
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      1,250
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-orange-100 dark:bg-orange-900/20 rounded-lg">
                    <TrendingUp className="h-6 w-6 text-orange-600 dark:text-orange-400" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      Nível
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      15
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Recent Activity */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Clock className="h-5 w-5 mr-2" />
                    Atividade Recente
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { action: 'Completou quiz de Matemática', time: '2 horas atrás', points: '+50' },
                      { action: 'Estudou Direito Constitucional', time: '4 horas atrás', points: '+30' },
                      { action: 'Alcançou meta diária', time: '6 horas atrás', points: '+100' },
                      { action: 'Completou sessão de flashcards', time: '8 horas atrás', points: '+25' },
                    ].map((activity, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                        <div>
                          <p className="font-medium text-gray-900 dark:text-white">
                            {activity.action}
                          </p>
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            {activity.time}
                          </p>
                        </div>
                        <span className="text-sm font-medium text-green-600 dark:text-green-400">
                          {activity.points}
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Quick Actions */}
            <div>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Award className="h-5 w-5 mr-2" />
                    Ações Rápidas
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button variant="secondary" className="w-full justify-start">
                    <Calendar className="h-4 w-4 mr-2" />
                    Agendar Estudo
                  </Button>
                  <Button variant="secondary" className="w-full justify-start">
                    <BarChart3 className="h-4 w-4 mr-2" />
                    Ver Progresso
                  </Button>
                  <Button variant="secondary" className="w-full justify-start">
                    <BookOpen className="h-4 w-4 mr-2" />
                    Criar Flashcard
                  </Button>
                  <Button variant="secondary" className="w-full justify-start">
                    <Target className="h-4 w-4 mr-2" />
                    Definir Meta
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </AppLayout>
    </ProtectedRoute>
  )
}
