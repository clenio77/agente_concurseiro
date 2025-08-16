import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { command } = body

    // Temporariamente retornando resposta mock
    return NextResponse.json({ 
      response: `Comando recebido: ${command}`,
      message: 'Voice API em modo mock'
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to process voice command' },
      { status: 500 }
    )
  }
}
