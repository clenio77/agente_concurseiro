import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { user_id, command_text, action_taken, success } = body

    // Criar sessão de voz se não existir
    const { data: session, error: sessionError } = await supabase
      .from('voice_assistant_sessions')
      .insert([{
        user_id,
        session_start: new Date().toISOString(),
        commands_processed: 1
      }])
      .select()
      .single()

    if (sessionError) throw sessionError

    // Registrar comando de voz
    const { data: command, error: commandError } = await supabase
      .from('voice_commands')
      .insert([{
        session_id: session.id,
        command_text,
        action_taken,
        success,
        processing_time_ms: Date.now()
      }])
      .select()
      .single()

    if (commandError) throw commandError

    return NextResponse.json({ 
      success: true, 
      session, 
      command 
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to process voice command' },
      { status: 500 }
    )
  }
}
