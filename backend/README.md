# Film Crew AI

## Agentic AI crew to generate a short film from 0 to masterpiece, fully autonomous.

This project uses [crewAI](https://crew.ai/) to create a network of AI agents that collaborate to generate a short movie script along with image (DALL-E, Flux) and video (Sora, Hailuo) generation prompts for visualization.

## Demo Example

![img](example.gif)

MP4: https://github.com/sundai-club/filmmaker/blob/main/example.mp4

## Setup

1. Install dependencies:
```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL_NAME=gpt-4o-mini
OTEL_SDK_DISABLED=true
```

## Usage

Run the script generator:
```bash
python filmcrew.py
```
