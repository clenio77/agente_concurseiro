import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { globalRateLimiter, strictRateLimiter } from './app/lib/rate-limiter'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()
  const ip = request.ip || 'unknown'
  const userAgent = request.headers.get('user-agent') || 'unknown'

  // Headers de segurança
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set('X-XSS-Protection', '1; mode=block')
  response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')

  // CSP (Content Security Policy) mais restritivo
  const csp = [
    "default-src 'self'",
    "script-src 'self' 'unsafe-eval' 'unsafe-inline' https://vercel.live",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data: https: blob:",
    "media-src 'self' https:",
    "connect-src 'self' https: wss:",
    "frame-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "upgrade-insecure-requests"
  ].join('; ')

  response.headers.set('Content-Security-Policy', csp)

  // Rate limiting real por IP
  const rateLimitResult = globalRateLimiter.checkByIP(ip)
  
  if (!rateLimitResult.success) {
    // Rate limit excedido
    response.headers.set('X-RateLimit-Limit', rateLimitResult.limit.toString())
    response.headers.set('X-RateLimit-Remaining', rateLimitResult.remaining.toString())
    response.headers.set('X-RateLimit-Reset', rateLimitResult.reset.toString())
    
    if (rateLimitResult.retryAfter) {
      response.headers.set('Retry-After', rateLimitResult.retryAfter.toString())
    }

    return new NextResponse(
      JSON.stringify({
        error: 'Rate limit exceeded',
        message: 'Too many requests, please try again later',
        retryAfter: rateLimitResult.retryAfter
      }),
      {
        status: 429,
        headers: {
          'Content-Type': 'application/json',
          ...response.headers
        }
      }
    )
  }

  // Rate limiting mais restritivo para endpoints sensíveis
  if (request.nextUrl.pathname.startsWith('/api/auth') || 
      request.nextUrl.pathname.startsWith('/api/admin')) {
    const strictRateLimit = strictRateLimiter.checkByIP(ip)
    
    if (!strictRateLimit.success) {
      return new NextResponse(
        JSON.stringify({
          error: 'Strict rate limit exceeded',
          message: 'Too many requests to sensitive endpoint',
          retryAfter: strictRateLimit.retryAfter
        }),
        {
          status: 429,
          headers: {
            'Content-Type': 'application/json',
            'X-RateLimit-Limit': strictRateLimit.limit.toString(),
            'X-RateLimit-Remaining': strictRateLimit.remaining.toString(),
            'X-RateLimit-Reset': strictRateLimit.reset.toString(),
            ...response.headers
          }
        }
      )
    }
  }

  // Headers de rate limit para todas as respostas
  response.headers.set('X-RateLimit-Limit', rateLimitResult.limit.toString())
  response.headers.set('X-RateLimit-Remaining', rateLimitResult.remaining.toString())
  response.headers.set('X-RateLimit-Reset', rateLimitResult.reset.toString())

  // Detecção e log de bots suspeitos
  const isBot = userAgent.includes('bot') || 
                userAgent.includes('crawler') || 
                userAgent.includes('spider') ||
                userAgent.includes('scraper')

  if (isBot) {
    console.log(`Bot detected: ${ip} - ${request.url} - User-Agent: ${userAgent}`)
    
    // Rate limiting mais restritivo para bots
    const botRateLimit = strictRateLimiter.checkByIP(`bot:${ip}`)
    if (!botRateLimit.success) {
      return new NextResponse(
        JSON.stringify({
          error: 'Bot rate limit exceeded',
          message: 'Bot requests are being rate limited'
        }),
        {
          status: 429,
          headers: {
            'Content-Type': 'application/json',
            'X-RateLimit-Limit': botRateLimit.limit.toString(),
            'X-RateLimit-Remaining': botRateLimit.remaining.toString(),
            'X-RateLimit-Reset': botRateLimit.reset.toString()
          }
        }
      )
    }
  }

  // Log de requisições suspeitas
  if (request.headers.get('x-forwarded-for') && !request.ip) {
    console.warn(`Suspicious request: Missing IP address - ${request.url}`)
  }

  return response
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!api|_next/static|_next/image|favicon.ico|public).*)',
  ],
}
