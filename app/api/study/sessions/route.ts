import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')

    if (!userId) {
      return NextResponse.json(
        { error: 'User ID is required' },
        { status: 400 }
      )
    }

    const { data: sessions, error } = await supabase
      .from('study_sessions')
      .select('*')
      .eq('user_id', userId)
      .order('start_time', { ascending: false })
      .limit(50)

    if (error) throw error

    return NextResponse.json({ sessions })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch study sessions' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { user_id, subject, topic, duration_minutes, start_time } = body

    const { data: session, error } = await supabase
      .from('study_sessions')
      .insert([{
        user_id,
        subject,
        topic,
        duration_minutes,
        start_time: new Date(start_time).toISOString()
      }])
      .select()
      .single()

    if (error) throw error

    return NextResponse.json({ session })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create study session' },
      { status: 500 }
    )
  }
}
