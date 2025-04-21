import { NextResponse } from 'next/server'
import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export async function POST(request: Request) {
  try {
    const { content, notes } = await request.json()

    if (!content) {
      return NextResponse.json(
        { error: 'Blog content is required' },
        { status: 400 }
      )
    }

    // Build the prompt with context for the summary
    const prompt = `
    Please provide a concise summary of the following content.
    The summary should capture the main points and key insights. You should write it from the view point of the writer of the post. Use the pronoun "I" to refer to the writer and "you" to refer to the reader. Do not mention that this is a summary. But make it sound like you are talking to the reader.
    
    ${notes ? `Additional instructions: ${notes}` : ''}
    
    Blog content:
    ${content}
    `

    // Call OpenAI API with GPT-4o
    const response = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: 'You are an expert content summarizer. Your task is to create clear, concise summaries that retain the essential information from the original content.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.5, // Lower temperature for more focused summaries
      max_tokens: 1000, // Reduced token count for shorter summaries
    })

    // Extract the summary from the response
    const summary = response.choices[0]?.message?.content || ''

    return NextResponse.json({ summary })
  } catch (error) {
    console.error('Error summarizing content:', error)
    return NextResponse.json(
      { error: 'Failed to summarize content' },
      { status: 500 }
    )
  }
} 