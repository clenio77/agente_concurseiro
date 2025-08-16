'use client'

import { useState, useEffect, useCallback } from 'react'
import type { SpeechRecognition, SpeechRecognitionEvent, SpeechRecognitionErrorEvent } from '@/types/web-speech'

interface UseSpeechRecognitionOptions {
  continuous?: boolean
  interimResults?: boolean
  lang?: string
  onResult?: (transcript: string, isFinal: boolean) => void
  onError?: (error: string) => void
}

interface UseSpeechRecognitionReturn {
  transcript: string
  isListening: boolean
  isSupported: boolean
  startListening: () => void
  stopListening: () => void
  resetTranscript: () => void
  error: string | null
}

export function useSpeechRecognition(options: UseSpeechRecognitionOptions = {}): UseSpeechRecognitionReturn {
  const [transcript, setTranscript] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(null)

  const {
    continuous = true,
    interimResults = true,
    lang = 'pt-BR',
    onResult,
    onError
  } = options

  // Verificar suporte do navegador
  const isSupported = typeof window !== 'undefined' && 'webkitSpeechRecognition' in window

  useEffect(() => {
    if (!isSupported) {
      setError('Speech recognition not supported in this browser')
      return
    }

    // Usar webkitSpeechRecognition para compatibilidade
    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition
    const recognitionInstance = new SpeechRecognition()

    recognitionInstance.continuous = continuous
    recognitionInstance.interimResults = interimResults
    recognitionInstance.lang = lang

    recognitionInstance.onstart = () => {
      setIsListening(true)
      setError(null)
    }

    recognitionInstance.onresult = (event: SpeechRecognitionEvent) => {
      let finalTranscript = ''
      let interimTranscript = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i]
        if (result && result.length > 0) {
          const transcript = result[0]?.transcript || ''
          if (result.isFinal) {
            finalTranscript += transcript
          } else {
            interimTranscript += transcript
          }
        }
      }

      const newTranscript = finalTranscript || interimTranscript
      setTranscript(newTranscript)

      if (onResult) {
        onResult(newTranscript, !!finalTranscript)
      }
    }

    recognitionInstance.onerror = (event: SpeechRecognitionErrorEvent) => {
      const errorMessage = getErrorMessage(event.error)
      setError(errorMessage)
      setIsListening(false)
      
      if (onError) {
        onError(errorMessage)
      }
    }

    recognitionInstance.onend = () => {
      setIsListening(false)
    }

    setRecognition(recognitionInstance)

    return () => {
      if (recognitionInstance) {
        recognitionInstance.abort()
      }
    }
  }, [continuous, interimResults, lang, onResult, onError, isSupported])

  const startListening = useCallback(() => {
    if (recognition && !isListening) {
      try {
        recognition.start()
      } catch (err) {
        setError('Failed to start speech recognition')
      }
    }
  }, [recognition, isListening])

  const stopListening = useCallback(() => {
    if (recognition && isListening) {
      try {
        recognition.stop()
      } catch (err) {
        setError('Failed to stop speech recognition')
      }
    }
  }, [recognition, isListening])

  const resetTranscript = useCallback(() => {
    setTranscript('')
    setError(null)
  }, [])

  return {
    transcript,
    isListening,
    isSupported,
    startListening,
    stopListening,
    resetTranscript,
    error
  }
}

function getErrorMessage(error: string): string {
  const errorMessages: Record<string, string> = {
    'no-speech': 'Nenhuma fala detectada. Tente novamente.',
    'audio-capture': 'Erro ao capturar áudio. Verifique as permissões do microfone.',
    'not-allowed': 'Permissão de microfone negada. Permita o acesso ao microfone.',
    'aborted': 'Reconhecimento de voz interrompido.',
    'network': 'Erro de rede. Verifique sua conexão.',
    'service-not-allowed': 'Serviço de reconhecimento de voz não permitido.',
    'bad-grammar': 'Erro de gramática no reconhecimento.',
    'language-not-supported': 'Idioma não suportado.'
  }

  return errorMessages[error] || `Erro desconhecido: ${error}`
}


