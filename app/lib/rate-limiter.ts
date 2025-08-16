interface RateLimitOptions {
  uniqueTokenPerInterval?: number
  interval?: number
  maxRequests?: number
}

interface RateLimitResult {
  success: boolean
  limit: number
  remaining: number
  reset: number
  retryAfter: number | null
}

export class RateLimiter {
  private tokenCache: Map<string, number[]>
  private options: Required<RateLimitOptions>

  constructor(options: RateLimitOptions = {}) {
    this.options = {
      uniqueTokenPerInterval: options.uniqueTokenPerInterval || 500,
      interval: options.interval || 60000, // 1 minuto
      maxRequests: options.maxRequests || 100,
    }

    this.tokenCache = new Map()
  }

  /**
   * Verifica se uma requisição está dentro do limite de taxa
   */
  check(token: string): RateLimitResult {
    const now = Date.now()
    const windowStart = now - this.options.interval

    // Obter timestamps existentes para este token
    const timestamps = this.tokenCache.get(token) || []
    
    // Filtrar timestamps dentro da janela atual
    const validTimestamps = timestamps.filter(timestamp => timestamp > windowStart)
    
    // Verificar se está dentro do limite
    const isAllowed = validTimestamps.length < this.options.maxRequests
    
    if (isAllowed) {
      // Adicionar timestamp atual
      validTimestamps.push(now)
      this.tokenCache.set(token, validTimestamps)
    }

    // Limpar tokens antigos para evitar vazamento de memória
    if (this.tokenCache.size > this.options.uniqueTokenPerInterval) {
      this.cleanup()
    }

    // Calcular tempo até reset
    const reset = windowStart + this.options.interval
    
    // Calcular requisições restantes
    const remaining = Math.max(0, this.options.maxRequests - validTimestamps.length)
    
    // Calcular tempo de espera se excedeu o limite
    let retryAfter: number | null = null
    if (!isAllowed && validTimestamps.length > 0) {
      const oldestTimestamp = Math.min(...validTimestamps)
      retryAfter = Math.ceil((oldestTimestamp + this.options.interval - now) / 1000)
    }

    return {
      success: isAllowed,
      limit: this.options.maxRequests,
      remaining,
      reset,
      retryAfter,
    }
  }

  /**
   * Limpa tokens antigos para evitar vazamento de memória
   */
  private cleanup(): void {
    const now = Date.now()
    const windowStart = now - this.options.interval
    
    const tokens = Array.from(this.tokenCache.keys())
    for (const token of tokens) {
      const timestamps = this.tokenCache.get(token) || []
      const validTimestamps = timestamps.filter(timestamp => timestamp > windowStart)
      if (validTimestamps.length === 0) {
        this.tokenCache.delete(token)
      } else {
        this.tokenCache.set(token, validTimestamps)
      }
    }
  }

  /**
   * Verifica rate limit por IP
   */
  checkByIP(ip: string): RateLimitResult {
    return this.check(`ip:${ip}`)
  }

  /**
   * Verifica rate limit por usuário
   */
  checkByUser(userId: string): RateLimitResult {
    return this.check(`user:${userId}`)
  }

  /**
   * Verifica rate limit por endpoint
   */
  checkByEndpoint(endpoint: string, identifier: string): RateLimitResult {
    return this.check(`endpoint:${endpoint}:${identifier}`)
  }

  /**
   * Reseta rate limit para um token específico
   */
  reset(token: string): void {
    this.tokenCache.delete(token)
  }

  /**
   * Obtém estatísticas de rate limit
   */
  getStats(token: string): { requests: number; reset: number } | null {
    const timestamps = this.tokenCache.get(token)
    if (!timestamps) return null

    const now = Date.now()
    const windowStart = now - this.options.interval
    const validRequests = timestamps.filter(timestamp => timestamp > windowStart).length

    return {
      requests: validRequests,
      reset: windowStart + this.options.interval,
    }
  }

  /**
   * Limpa todos os caches
   */
  clear(): void {
    this.tokenCache.clear()
  }
}

// Instância global para uso em toda a aplicação
export const globalRateLimiter = new RateLimiter({
  uniqueTokenPerInterval: 1000,
  interval: 60000, // 1 minuto
  maxRequests: 100,
})

// Rate limiter mais restritivo para endpoints sensíveis
export const strictRateLimiter = new RateLimiter({
  uniqueTokenPerInterval: 500,
  interval: 60000, // 1 minuto
  maxRequests: 20,
})

// Rate limiter para autenticação
export const authRateLimiter = new RateLimiter({
  uniqueTokenPerInterval: 100,
  interval: 300000, // 5 minutos
  maxRequests: 5,
})
