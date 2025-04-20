# Filmmaker Frontend

A modern, minimalist Next.js application for generating AI videos from text.

## Features

- Step-by-step video creation workflow
- Generate scripts from text prompts
- Edit scripts to customize your video
- Select from various video styles
- Generate and download the final video

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see backend documentation)

### Installation

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. Enter a description or prompt for your video.
2. Generate a script based on your input.
3. Edit the script as needed.
4. Select a video style.
5. Generate the video.
6. Watch and download your video.

## Development

### Build for Production

```bash
npm run build
```

### Start Production Server

```bash
npm start
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000/api`. The API endpoints include:

- `/api/generate-script` - Generate a script from input text
- `/api/generate-video` - Generate a video from a script
- `/api/available-styles` - Get available video styles

See the backend documentation for more details. 