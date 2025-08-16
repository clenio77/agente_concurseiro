import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Temporariamente retornando dados mock
    return NextResponse.json({ 
      users: [],
      message: 'API temporariamente em modo mock'
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch users' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { email, full_name, study_level = 'iniciante' } = body

    // Temporariamente retornando sucesso mock
    return NextResponse.json({ 
      user: { id: 'temp-id', email, full_name, study_level },
      message: 'User created (mock)'
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 500 }
    )
  }
}
