'use client'

import { useState, useEffect, useCallback } from 'react'

interface UseSpeechSynthesisOptions {
  lang?: string
  pitch?: number
  rate?: number
  volume?: number
  voice?: string
  onStart?: () => void
  onEnd?: () => void
  onError?: (error: string) => void
}

interface UseSpeechSynthesisReturn {
  isSpeaking: boolean
  isSupported: boolean
  voices: SpeechSynthesisVoice[]
  speak: (text: string) => void
  stop: () => void
  pause: () => void
  resume: () => void
  error: string | null
}

export function useSpeechSynthesis(options: UseSpeechSynthesisOptions = {}): UseSpeechSynthesisReturn {
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([])
  const [error, setError] = useState<string | null>(null)
  const [synth, setSynth] = useState<any>(null)

  const {
    lang = 'pt-BR',
    pitch = 1,
    rate = 1,
    volume = 1,
    voice,
    onStart,
    onEnd,
    onError
  } = options

  // Verificar suporte do navegador
  const isSupported = typeof window !== 'undefined' && 'speechSynthesis' in window

  useEffect(() => {
    if (!isSupported) {
      setError('Speech synthesis not supported in this browser')
      return
    }

    const speechSynthesis = (window as any).speechSynthesis
    setSynth(speechSynthesis)

    // Carregar vozes disponíveis
    const loadVoices = () => {
      const availableVoices = speechSynthesis.getVoices()
      setVoices(availableVoices)
    }

    // Chrome carrega vozes de forma assíncrona
    if (speechSynthesis.onvoiceschanged !== undefined) {
      speechSynthesis.onvoiceschanged = loadVoices
    }

    // Carregar vozes iniciais
    loadVoices()

    return () => {
      if (speechSynthesis) {
        speechSynthesis.cancel()
      }
    }
  }, [isSupported])

  const speak = useCallback((text: string) => {
    if (!synth || !isSupported) {
      setError('Speech synthesis not available')
      return
    }

    try {
      // Cancelar fala anterior
      synth.cancel()

      const utterance = new SpeechSynthesisUtterance(text)
      
      // Configurar propriedades
      utterance.lang = lang
      utterance.pitch = pitch
      utterance.rate = rate
      utterance.volume = volume

      // Selecionar voz se especificada
      if (voice) {
        const selectedVoice = voices.find(v => v.name === voice)
        if (selectedVoice) {
          utterance.voice = selectedVoice
        }
      }

      // Eventos
      utterance.onstart = () => {
        setIsSpeaking(true)
        setError(null)
        if (onStart) onStart()
      }

      utterance.onend = () => {
        setIsSpeaking(false)
        if (onEnd) onEnd()
      }

      utterance.onerror = (event: any) => {
        setIsSpeaking(false)
        const errorMessage = getSynthesisErrorMessage(event.error)
        setError(errorMessage)
        if (onError) onError(errorMessage)
      }

      synth.speak(utterance)
    } catch (err) {
      const errorMessage = 'Failed to start speech synthesis'
      setError(errorMessage)
      if (onError) onError(errorMessage)
    }
  }, [synth, isSupported, lang, pitch, rate, volume, voice, voices, onStart, onEnd, onError])

  const stop = useCallback(() => {
    if (synth) {
      synth.cancel()
      setIsSpeaking(false)
    }
  }, [synth])

  const pause = useCallback(() => {
    if (synth && isSpeaking) {
      synth.pause()
    }
  }, [synth, isSpeaking])

  const resume = useCallback(() => {
    if (synth && isSpeaking) {
      synth.resume()
    }
  }, [synth, isSpeaking])

  return {
    isSpeaking,
    isSupported,
    voices,
    speak,
    stop,
    pause,
    resume,
    error
  }
}

function getSynthesisErrorMessage(error: string): string {
  const errorMessages: Record<string, string> = {
    'canceled': 'Síntese de voz cancelada.',
    'interrupted': 'Síntese de voz interrompida.',
    'audio-busy': 'Sistema de áudio ocupado. Tente novamente.',
    'audio-hardware': 'Erro no hardware de áudio.',
    'network': 'Erro de rede na síntese de voz.',
    'synthesis-unavailable': 'Síntese de voz não disponível.',
    'synthesis-failed': 'Falha na síntese de voz.',
    'language-unavailable': 'Idioma não disponível para síntese.',
    'voice-unavailable': 'Voz não disponível.',
    'text-too-long': 'Texto muito longo para síntese.',
    'invalid-argument': 'Argumento inválido para síntese.',
    'not-allowed': 'Síntese de voz não permitida.'
  }

  return errorMessages[error] || `Erro desconhecido: ${error}`
}


