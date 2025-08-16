'use client'

import React, { useState, useRef, useEffect, useCallback } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Mic, MicOff, Volume2, VolumeX, Brain, MessageSquare } from 'lucide-react'
import { cn } from '../../lib/utils/cn'

interface VoiceCommand {
  id: string
  command: string
  response: string
  timestamp: Date
  confidence: number
}

interface VoiceAssistantProps {
  className?: string
  onCommandProcessed?: (command: string, response: string) => void
}

export const VoiceAssistant: React.FC<VoiceAssistantProps> = ({
  className,
  onCommandProcessed
}) => {
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [response, setResponse] = useState('')
  const [commands, setCommands] = useState<VoiceCommand[]>([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState('')
  
  const recognitionRef = useRef<any>(null)
  const synthesisRef = useRef<SpeechSynthesis | null>(null)

  // Inicializar Web Speech API
  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Speech Recognition
      if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
        recognitionRef.current = new SpeechRecognition()
        recognitionRef.current.continuous = false
        recognitionRef.current.interimResults = false
        recognitionRef.current.lang = 'pt-BR'
        
        recognitionRef.current.onstart = () => {
          setIsListening(true)
          setError('')
        }
        
                            recognitionRef.current.onresult = (event: any) => {
                      const transcript = event.results[0][0].transcript
                      setTranscript(transcript)
                      // eslint-disable-next-line react-hooks/exhaustive-deps
                      processVoiceCommand(transcript)
                    }
        
        recognitionRef.current.onerror = (event: any) => {
          setError(`Erro de reconhecimento: ${event.error}`)
          setIsListening(false)
        }
        
        recognitionRef.current.onend = () => {
          setIsListening(false)
        }
      } else {
        setError('Speech Recognition não suportado neste navegador')
      }

      // Speech Synthesis
      if ('speechSynthesis' in window) {
        synthesisRef.current = window.speechSynthesis
      } else {
        setError('Speech Synthesis não suportado neste navegador')
      }
    }
  }, [])

  const processVoiceCommand = useCallback(async (command: string) => {
    setIsProcessing(true)
    setError('')

    try {
      // Simular processamento de IA (será substituído por Supabase/OpenAI)
      const aiResponse = await simulateAIResponse(command)
      
      const newCommand: VoiceCommand = {
        id: Date.now().toString(),
        command,
        response: aiResponse,
        timestamp: new Date(),
        confidence: Math.random() * 0.3 + 0.7 // Simular confiança 70-100%
      }

      setCommands(prev => [newCommand, ...prev.slice(0, 9)]) // Manter apenas 10 comandos
      setResponse(aiResponse)
      
      // Callback para componente pai
      onCommandProcessed?.(command, aiResponse)
      
      // Falar a resposta
      speakResponse(aiResponse)
      
    } catch (error) {
      setError('Erro ao processar comando de voz')
    } finally {
      setIsProcessing(false)
    }
  }, [onCommandProcessed])

  const simulateAIResponse = async (command: string): Promise<string> => {
    // Simular delay de processamento
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const lowerCommand = command.toLowerCase()
    
    // Comandos educacionais básicos
    if (lowerCommand.includes('estudar') || lowerCommand.includes('estudo')) {
      return 'Vamos começar uma sessão de estudo! Qual matéria você gostaria de revisar hoje?'
    }
    
    if (lowerCommand.includes('flashcard') || lowerCommand.includes('cartão')) {
      return 'Perfeito! Vou abrir os flashcards. Você pode escolher entre Matemática, Português, História ou Direito.'
    }
    
    if (lowerCommand.includes('quiz') || lowerCommand.includes('teste')) {
      return 'Excelente ideia! Vou preparar um quiz personalizado baseado no seu progresso recente.'
    }
    
    if (lowerCommand.includes('progresso') || lowerCommand.includes('desempenho')) {
      return 'Vou mostrar seu progresso atual. Você está no nível 15 com 1.250 pontos. Continue assim!'
    }
    
    if (lowerCommand.includes('ajuda') || lowerCommand.includes('help')) {
      return 'Posso ajudar você com: iniciar estudo, abrir flashcards, fazer quiz, ver progresso, ou definir metas. O que você gostaria?'
    }
    
    if (lowerCommand.includes('meta') || lowerCommand.includes('objetivo')) {
      return 'Vamos definir uma meta de estudo! Quantas horas você gostaria de estudar hoje?'
    }
    
    // Resposta padrão para comandos não reconhecidos
    return 'Desculpe, não entendi esse comando. Tente dizer "ajuda" para ver o que posso fazer por você.'
  }

  const speakResponse = (text: string) => {
    if (synthesisRef.current) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'pt-BR'
      utterance.rate = 0.9
      utterance.pitch = 1.0
      
      utterance.onstart = () => setIsSpeaking(true)
      utterance.onend = () => setIsSpeaking(false)
      utterance.onerror = () => setIsSpeaking(false)
      
      synthesisRef.current.speak(utterance)
    }
  }

  const startListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start()
    }
  }

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop()
    }
  }

  const toggleListening = () => {
    if (isListening) {
      stopListening()
    } else {
      startListening()
    }
  }

  const stopSpeaking = () => {
    if (synthesisRef.current) {
      synthesisRef.current.cancel()
      setIsSpeaking(false)
    }
  }

  return (
    <div className={cn('space-y-6', className)}>
      {/* Main Voice Interface */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Brain className="h-5 w-5 mr-2" />
            Assistente de Voz Inteligente
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Voice Controls */}
          <div className="flex items-center justify-center space-x-4">
            <Button
              onClick={toggleListening}
              disabled={isProcessing}
              variant={isListening ? 'error' : 'primary'}
              size="lg"
              className="w-24 h-24 rounded-full"
            >
              {isListening ? (
                <MicOff className="h-8 w-8" />
              ) : (
                <Mic className="h-8 w-8" />
              )}
            </Button>
            
            {isSpeaking && (
              <Button
                onClick={stopSpeaking}
                variant="secondary"
                size="sm"
                className="flex items-center"
              >
                <VolumeX className="h-4 w-4 mr-2" />
                Parar
              </Button>
            )}
          </div>

          {/* Status Display */}
          <div className="text-center">
            {isListening && (
              <div className="flex items-center justify-center space-x-2 text-primary-600 dark:text-primary-400">
                <div className="w-3 h-3 bg-primary-600 rounded-full animate-pulse" />
                <span className="text-sm font-medium">Ouvindo...</span>
              </div>
            )}
            
            {isProcessing && (
              <div className="flex items-center justify-center space-x-2 text-blue-600 dark:text-blue-400">
                <div className="w-3 h-3 bg-blue-600 rounded-full animate-pulse" />
                <span className="text-sm font-medium">Processando...</span>
              </div>
            )}
            
            {isSpeaking && (
              <div className="flex items-center justify-center space-x-2 text-green-600 dark:text-green-400">
                <Volume2 className="h-4 w-4" />
                <span className="text-sm font-medium">Falando...</span>
              </div>
            )}
          </div>

          {/* Transcript and Response */}
          <div className="space-y-4">
            {transcript && (
              <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <Mic className="h-4 w-4 text-gray-500" />
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Você disse:
                  </span>
                </div>
                <p className="text-gray-900 dark:text-white">{transcript}</p>
              </div>
            )}

            {response && (
              <div className="p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <MessageSquare className="h-4 w-4 text-primary-500" />
                  <span className="text-sm font-medium text-primary-700 dark:text-primary-300">
                    Resposta:
                  </span>
                </div>
                <p className="text-primary-900 dark:text-primary-100">{response}</p>
              </div>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </div>
          )}

          {/* Quick Commands */}
          <div className="space-y-3">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Comandos de Voz Disponíveis:
            </h4>
            <div className="grid grid-cols-2 gap-2">
              {[
                'Iniciar estudo',
                'Abrir flashcards',
                'Fazer quiz',
                'Ver progresso',
                'Definir meta',
                'Pedir ajuda'
              ].map((command) => (
                                  <Button
                    key={command}
                    variant="secondary"
                    size="sm"
                    onClick={() => processVoiceCommand(command)}
                    className="text-xs"
                  >
                    &ldquo;{command}&rdquo;
                  </Button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Command History */}
      {commands.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Histórico de Comandos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {commands.map((cmd) => (
                <div key={cmd.id} className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {cmd.command}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {cmd.response}
                      </p>
                    </div>
                    <div className="text-right text-xs text-gray-500 dark:text-gray-400">
                      <div>{cmd.timestamp.toLocaleTimeString('pt-BR')}</div>
                      <div>Confiança: {Math.round(cmd.confidence * 100)}%</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
