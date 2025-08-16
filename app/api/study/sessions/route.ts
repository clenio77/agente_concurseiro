import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Temporariamente retornando dados mock
    return NextResponse.json({ 
      sessions: [],
      message: 'Study sessions API em modo mock'
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch study sessions' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { user_id, subject, duration_minutes } = body

    // Temporariamente retornando sucesso mock
    return NextResponse.json({ 
      session: { 
        id: 'temp-session-id', 
        user_id, 
        subject, 
        duration_minutes,
        start_time: new Date().toISOString()
      },
      message: 'Study session created (mock)'
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create study session' },
      { status: 500 }
    )
  }
}
