'use client'

import React, { useState, useRef, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Select } from '@/components/ui/Select'
import { Camera, Eye, EyeOff, Target, Zap, BookOpen, Brain, Globe } from 'lucide-react'
import { cn } from '../../lib/utils/cn'

interface ARExperience {
  id: string
  name: string
  description: string
  category: 'anatomy' | 'geography' | 'architecture' | 'chemistry' | 'physics' | 'history'
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  duration: number
  features: string[]
  thumbnail: string
}

interface ARSession {
  id: string
  experienceId: string
  startTime: Date
  endTime?: Date
  progress: number
  interactions: number
  score: number
}

interface AugmentedRealityProps {
  className?: string
  userId?: string
}

export const AugmentedReality: React.FC<AugmentedRealityProps> = ({
  className
}) => {
  const [isARActive, setIsARActive] = useState(false)
  const [selectedExperience, setSelectedExperience] = useState<string>('')
  const [currentSession, setCurrentSession] = useState<ARSession | null>(null)
  const [arMode, setArMode] = useState<'view' | 'interactive' | 'learning'>('view')
  const [cameraPermission, setCameraPermission] = useState<boolean>(false)
  const [arSupported, setArSupported] = useState<boolean>(false)
  
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // Experiências AR disponíveis
  const arExperiences: ARExperience[] = [
    {
      id: '1',
      name: 'Anatomia Humana 3D',
      description: 'Explore o corpo humano em realidade aumentada com órgãos interativos',
      category: 'anatomy',
      difficulty: 'intermediate',
      duration: 15,
      features: ['Órgãos 3D interativos', 'Informações detalhadas', 'Quiz integrado'],
      thumbnail: '/api/placeholder/300/200'
    },
    {
      id: '2',
      name: 'Geografia Mundial AR',
      description: 'Viaje pelo mundo através de mapas 3D e pontos de interesse',
      category: 'geography',
      difficulty: 'beginner',
      duration: 20,
      features: ['Mapas 3D', 'Pontos históricos', 'Informações culturais'],
      thumbnail: '/api/placeholder/300/200'
    },
    {
      id: '3',
      name: 'Arquitetura Histórica',
      description: 'Visite construções históricas em escala real no seu ambiente',
      category: 'architecture',
      difficulty: 'advanced',
      duration: 25,
      features: ['Construções em escala', 'História detalhada', 'Exploração 360°'],
      thumbnail: '/api/placeholder/300/200'
    },
    {
      id: '4',
      name: 'Laboratório de Química AR',
      description: 'Realize experimentos químicos virtuais com segurança total',
      category: 'chemistry',
      difficulty: 'intermediate',
      duration: 18,
      features: ['Experimentos virtuais', 'Materiais seguros', 'Resultados em tempo real'],
      thumbnail: '/api/placeholder/300/200'
    }
  ]

  // Verificar suporte a AR
  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Verificar WebXR API
      const hasWebXR = 'xr' in navigator
      setArSupported(hasWebXR)
      
      // Verificar permissão de câmera
      if ('permissions' in navigator) {
        navigator.permissions.query({ name: 'camera' as PermissionName })
          .then(result => setCameraPermission(result.state === 'granted'))
          .catch(() => setCameraPermission(false))
      }
    }
  }, [])

  const startARSession = async (experienceId: string) => {
    if (!arSupported) {
      alert('Realidade Aumentada não é suportada neste dispositivo')
      return
    }

    if (!cameraPermission) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        setCameraPermission(true)
        stream.getTracks().forEach(track => track.stop())
      } catch (error) {
        alert('Permissão de câmera necessária para AR')
        return
      }
    }

    const experience = arExperiences.find(exp => exp.id === experienceId)
    if (!experience) return

    const session: ARSession = {
      id: Date.now().toString(),
      experienceId,
      startTime: new Date(),
      progress: 0,
      interactions: 0,
      score: 0
    }

    setCurrentSession(session)
    setIsARActive(true)
    setSelectedExperience(experienceId)

    // Iniciar câmera
    if (videoRef.current) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { facingMode: 'environment' } 
        })
        videoRef.current.srcObject = stream
        videoRef.current.play()
      } catch (error) {
        console.error('Erro ao acessar câmera:', error)
      }
    }
  }

  const stopARSession = () => {
    if (currentSession) {
      const updatedSession = {
        ...currentSession,
        endTime: new Date()
      }
      setCurrentSession(updatedSession)
    }

    setIsARActive(false)
    setSelectedExperience('')
    
    // Parar câmera
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream
      stream.getTracks().forEach(track => track.stop())
      videoRef.current.srcObject = null
    }
  }

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'anatomy': return <Brain className="h-5 w-5" />
      case 'geography': return <Globe className="h-5 w-5" />
      case 'architecture': return <Target className="h-5 w-5" />
      case 'chemistry': return <Zap className="h-5 w-5" />
      case 'physics': return <Zap className="h-5 w-5" />
      case 'history': return <BookOpen className="h-5 w-5" />
      default: return <Target className="h-5 w-5" />
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'intermediate': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'advanced': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'anatomy': return 'Anatomia'
      case 'geography': return 'Geografia'
      case 'architecture': return 'Arquitetura'
      case 'chemistry': return 'Química'
      case 'physics': return 'Física'
      case 'history': return 'História'
      default: return 'Geral'
    }
  }

  const categories = [
    { value: 'all', label: 'Todas as Categorias' },
    { value: 'anatomy', label: 'Anatomia' },
    { value: 'geography', label: 'Geografia' },
    { value: 'architecture', label: 'Arquitetura' },
    { value: 'chemistry', label: 'Química' },
    { value: 'physics', label: 'Física' },
    { value: 'history', label: 'História' }
  ]

  const filteredExperiences = selectedExperience === 'all' 
    ? arExperiences 
    : arExperiences.filter(exp => exp.category === selectedExperience)

  return (
    <div className={cn('space-y-6', className)}>
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center space-x-3">
          <div className="p-3 bg-purple-100 dark:bg-purple-900/20 rounded-full">
            <Camera className="h-8 w-8 text-purple-600 dark:text-purple-400" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Realidade Aumentada
          </h1>
        </div>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Explore o mundo através de experiências imersivas em realidade aumentada
        </p>
      </div>

      {/* AR Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="h-5 w-5 mr-2" />
            Status da Realidade Aumentada
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {arSupported ? '✅' : '❌'}
              </div>
              <p className="text-sm text-blue-600 dark:text-blue-400">
                {arSupported ? 'AR Suportado' : 'AR Não Suportado'}
              </p>
            </div>
            
            <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {cameraPermission ? '✅' : '❌'}
              </div>
              <p className="text-sm text-green-600 dark:text-green-400">
                {cameraPermission ? 'Câmera Permitida' : 'Câmera Bloqueada'}
              </p>
            </div>
            
            <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {isARActive ? '🟢' : '⚪'}
              </div>
              <p className="text-sm text-purple-600 dark:text-purple-400">
                {isARActive ? 'AR Ativo' : 'AR Inativo'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* AR Experiences */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            Experiências Disponíveis
          </h2>
          
          <div className="flex items-center space-x-4">
            <Select
              options={categories}
              value={selectedExperience}
              onChange={setSelectedExperience}
              placeholder="Filtrar por categoria"
            />
            
            <Button
              onClick={() => setArMode(arMode === 'view' ? 'interactive' : 'view')}
              variant="secondary"
              className="flex items-center"
            >
              {arMode === 'view' ? <Eye className="h-4 w-4 mr-2" /> : <EyeOff className="h-4 w-4 mr-2" />}
              {arMode === 'view' ? 'Modo Visual' : 'Modo Interativo'}
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredExperiences.map((experience) => (
            <Card key={experience.id} className="overflow-hidden">
              <div className="aspect-video bg-gradient-to-br from-purple-100 to-blue-100 dark:from-purple-900/20 dark:to-blue-900/20 flex items-center justify-center">
                <div className="text-center">
                  {getCategoryIcon(experience.category)}
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                    {experience.name}
                  </p>
                </div>
              </div>
              
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-lg">{experience.name}</CardTitle>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {experience.description}
                    </p>
                  </div>
                  <span className={cn(
                    'text-xs px-2 py-1 rounded-full',
                    getDifficultyColor(experience.difficulty)
                  )}>
                    {experience.difficulty === 'beginner' ? 'Iniciante' : 
                     experience.difficulty === 'intermediate' ? 'Intermediário' : 'Avançado'}
                  </span>
                </div>
              </CardHeader>
              
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Categoria:</span>
                    <span className="font-medium">{getCategoryLabel(experience.category)}</span>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span>Duração:</span>
                    <span className="font-medium">{experience.duration} min</span>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Recursos:
                  </h4>
                  <ul className="space-y-1">
                    {experience.features.map((feature, index) => (
                      <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start">
                        <span className="text-purple-500 mr-2">•</span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <Button
                  onClick={() => startARSession(experience.id)}
                  disabled={!arSupported || !cameraPermission || isARActive}
                  className="w-full"
                >
                  <Camera className="h-4 w-4 mr-2" />
                  Iniciar Experiência AR
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* AR Camera View */}
      {isARActive && currentSession && (
        <Card className="relative">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Experiência AR Ativa</span>
              <Button
                onClick={stopARSession}
                variant="error"
                size="sm"
              >
                Parar AR
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Camera Feed */}
              <div className="relative aspect-video bg-black rounded-lg overflow-hidden">
                <video
                  ref={videoRef}
                  className="w-full h-full object-cover"
                  autoPlay
                  playsInline
                  muted
                />
                
                {/* AR Overlay */}
                <canvas
                  ref={canvasRef}
                  className="absolute inset-0 w-full h-full"
                  style={{ pointerEvents: 'none' }}
                />
                
                {/* AR Controls */}
                <div className="absolute bottom-4 left-4 right-4 flex justify-center space-x-2">
                  <Button
                    onClick={() => setArMode('view')}
                    variant={arMode === 'view' ? 'primary' : 'secondary'}
                    size="sm"
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    Visualizar
                  </Button>
                  
                  <Button
                    onClick={() => setArMode('interactive')}
                    variant={arMode === 'interactive' ? 'primary' : 'secondary'}
                    size="sm"
                  >
                    <Target className="h-4 w-4 mr-1" />
                    Interagir
                  </Button>
                  
                  <Button
                    onClick={() => setArMode('learning')}
                    variant={arMode === 'learning' ? 'primary' : 'secondary'}
                    size="sm"
                  >
                    <BookOpen className="h-4 w-4 mr-1" />
                    Aprender
                  </Button>
                </div>
              </div>
              
              {/* Session Info */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <div className="text-lg font-bold text-blue-600 dark:text-blue-400">
                    {Math.round(currentSession.progress)}%
                  </div>
                  <p className="text-sm text-blue-600 dark:text-blue-400">Progresso</p>
                </div>
                
                <div className="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <div className="text-lg font-bold text-green-600 dark:text-green-400">
                    {currentSession.interactions}
                  </div>
                  <p className="text-sm text-green-600 dark:text-green-400">Interações</p>
                </div>
                
                <div className="text-center p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                  <div className="text-lg font-bold text-purple-600 dark:text-purple-400">
                    {currentSession.score}
                  </div>
                  <p className="text-sm text-purple-600 dark:text-purple-400">Pontos</p>
                </div>
                
                <div className="text-center p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                  <div className="text-lg font-bold text-orange-600 dark:text-orange-400">
                    {arMode === 'view' ? 'Visual' : arMode === 'interactive' ? 'Interativo' : 'Aprendizado'}
                  </div>
                  <p className="text-sm text-orange-600 dark:text-orange-400">Modo</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* AR Tips */}
      <Card>
        <CardHeader>
          <CardTitle>Dicas para Realidade Aumentada</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <h4 className="font-semibold text-gray-900 dark:text-white">
                🎯 Antes de Começar
              </h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>• Certifique-se de ter boa iluminação</li>
                <li>• Mantenha o dispositivo estável</li>
                <li>• Permita acesso à câmera</li>
                <li>• Use fones de ouvido para imersão</li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-gray-900 dark:text-white">
                🚀 Durante a Experiência
              </h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>• Mova-se lentamente para melhor tracking</li>
                <li>• Toque nos elementos para interagir</li>
                <li>• Use gestos para navegar</li>
                <li>• Tire screenshots para revisão</li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-gray-900 dark:text-white">
                📱 Otimizações
              </h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>• Feche apps em segundo plano</li>
                <li>• Mantenha bateria acima de 30%</li>
                <li>• Use Wi-Fi para downloads</li>
                <li>• Limpe a câmera regularmente</li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-gray-900 dark:text-white">
                🎓 Dicas de Estudo
              </h4>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>• Revise o conteúdo após a experiência</li>
                <li>• Faça anotações durante a sessão</li>
                <li>• Compartilhe descobertas com colegas</li>
                <li>• Use AR como complemento aos estudos</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
