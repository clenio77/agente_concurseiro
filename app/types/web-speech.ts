// Tipos seguros para Web Speech API
export interface SpeechRecognitionEvent {
  resultIndex: number
  results: SpeechRecognitionResultList
}

export interface SpeechRecognitionResultList {
  length: number
  item(index: number): SpeechRecognitionResult
  [index: number]: SpeechRecognitionResult
}

export interface SpeechRecognitionResult {
  isFinal: boolean
  length: number
  item(index: number): SpeechRecognitionAlternative
  [index: number]: SpeechRecognitionAlternative
}

export interface SpeechRecognitionAlternative {
  transcript: string
  confidence: number
}

export interface SpeechRecognitionErrorEvent {
  error: string
  message: string
}

export interface SpeechRecognition extends EventTarget {
  continuous: boolean
  interimResults: boolean
  lang: string
  maxAlternatives: number
  serviceURI: string
  start(): void
  stop(): void
  abort(): void
  onstart: ((this: SpeechRecognition, ev: Event) => any) | null
  onresult: ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => any) | null
  onerror: ((this: SpeechRecognition, ev: SpeechRecognitionErrorEvent) => any) | null
  onend: ((this: SpeechRecognition, ev: Event) => any) | null
}

export interface SpeechSynthesisUtterance extends EventTarget {
  text: string
  lang: string
  pitch: number
  rate: number
  volume: number
  voice: SpeechSynthesisVoice | null
  onstart: ((this: SpeechSynthesisUtterance, ev: Event) => any) | null
  onend: ((this: SpeechSynthesisUtterance, ev: Event) => any) | null
  onerror: ((this: SpeechSynthesisUtterance, ev: Event) => any) | null
}

export interface SpeechSynthesisVoice {
  voiceURI: string
  name: string
  lang: string
  localService: boolean
  default: boolean
}

export interface SpeechSynthesis extends EventTarget {
  speaking: boolean
  pending: boolean
  paused: boolean
  onvoiceschanged: ((this: SpeechSynthesis, ev: Event) => any) | null
  speak(utterance: SpeechSynthesisUtterance): void
  cancel(): void
  pause(): void
  resume(): void
  getVoices(): SpeechSynthesisVoice[]
}


