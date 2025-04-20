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
REPLICATE_API_TOKEN=your_replicate_api_token_here
PEXELS_API_KEY=your_pexels_api_key_here
VIDEO_STYLE=Infinite Zoom
```

For video generation, you'll need to obtain:
- An API key from [Replicate](https://replicate.com/) for AI video generation
- An API key from [Pexels](https://www.pexels.com/api/) for stock video (if using the 'Internet Videos' style)

## Usage

Run the script generator:
```bash
python filmcrew.py
```

The system will:
1. Generate a movie script with characters and scenes
2. Create image prompts for characters
3. Design scene descriptions
4. Generate music prompts
5. Create narration with timed subtitles
6. Generate a title
7. Automatically produce a video based on the narration using the selected video style

## Video Style Options

You can change the video style by setting the `VIDEO_STYLE` environment variable to one of:
- `Infinite Zoom` - Creates zoom-in effect videos using Stable Diffusion
- `Anime` - Creates anime-style videos using Animate-Diff
- `Internet Videos` - Uses stock videos from Pexels based on AI-generated keywords

To disable video generation, set `generator.enable_video = False` in the code.
