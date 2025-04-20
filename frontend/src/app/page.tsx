'use client';

import React, { useState, useEffect } from 'react';
import { FilmmakerAPI } from '@/services/api';
import Button from '@/components/Button';
import TextArea from '@/components/TextArea';
import Card from '@/components/Card';
import Select from '@/components/Select';
import Loader from '@/components/Loader';

// App states
enum AppState {
  INITIAL = 'INITIAL',
  GENERATING_SCRIPT = 'GENERATING_SCRIPT',
  SCRIPT_READY = 'SCRIPT_READY',
  GENERATING_VIDEO = 'GENERATING_VIDEO',
  VIDEO_READY = 'VIDEO_READY',
  ERROR = 'ERROR',
}

export default function Home() {
  // State
  const [appState, setAppState] = useState<AppState>(AppState.INITIAL);
  const [inputText, setInputText] = useState('');
  const [scriptText, setScriptText] = useState('');
  const [videoStyle, setVideoStyle] = useState('');
  const [videoPath, setVideoPath] = useState('');
  const [error, setError] = useState('');
  const [availableStyles, setAvailableStyles] = useState<Array<{ value: string; label: string }>>([]);
  const [scriptPath, setScriptPath] = useState('');

  // Fetch available styles on component mount
  useEffect(() => {
    const fetchStyles = async () => {
      const response = await FilmmakerAPI.getAvailableStyles();
      if (response.success) {
        setAvailableStyles(
          response.styles.map((style) => ({
            value: style,
            label: style,
          }))
        );
        if (response.styles.length > 0) {
          setVideoStyle(response.styles[0]);
        }
      }
    };

    fetchStyles();
  }, []);

  // Handle script generation
  const handleGenerateScript = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text to generate a script.');
      return;
    }

    try {
      setAppState(AppState.GENERATING_SCRIPT);
      setError('');

      const response = await FilmmakerAPI.generateScript(inputText);

      if (response.success) {
        // Store the script path
        setScriptPath(response.script_path);
        
        // Try to fetch the actual script content
        try {
          const scriptUrl = FilmmakerAPI.getFileUrl(response.script_path);
          const scriptResponse = await fetch(scriptUrl);
          
          if (scriptResponse.ok) {
            // Use the actual script content
            const scriptContent = await scriptResponse.text();
            setScriptText(scriptContent);
          } else {
            // Fallback to a template if we can't get the content
            const defaultContent = `1
00:00:00,000 --> 00:00:05,000
${response.title}: Scene 1

2
00:00:05,000 --> 00:00:10,000
[Character appears, looking determined]

3
00:00:10,000 --> 00:00:15,000
"This journey begins with a simple step."

4
00:00:15,000 --> 00:00:20,000
[Character walks forward, the landscape changes]

5
00:00:20,000 --> 00:00:25,000
Adventure awaits at every turn.`;
            setScriptText(defaultContent);
          }
        } catch (fetchErr) {
          // Fallback to default content on error
          console.error('Error fetching script content:', fetchErr);
          setScriptText(`1
00:00:00,000 --> 00:00:05,000
${response.title || 'Movie'}: Scene 1

2
00:00:05,000 --> 00:00:10,000
[Add your script here]`);
        }
        
        setAppState(AppState.SCRIPT_READY);
      } else {
        setError(response.error || 'Failed to generate script.');
        setAppState(AppState.ERROR);
      }
    } catch (err) {
      setError('An unexpected error occurred.');
      setAppState(AppState.ERROR);
    }
  };

  // Handle video generation
  const handleGenerateVideo = async () => {
    if (!scriptText.trim()) {
      setError('Script cannot be empty.');
      return;
    }

    try {
      setAppState(AppState.GENERATING_VIDEO);
      setError('');

      // Use either script path or text
      let response;
      if (scriptPath) {
        response = await FilmmakerAPI.generateVideoFromPath(scriptPath, videoStyle);
      } else {
        response = await FilmmakerAPI.generateVideoFromText(scriptText, videoStyle);
      }

      if (response.success) {
        setVideoPath(response.video_path);
        setAppState(AppState.VIDEO_READY);
      } else {
        setError(response.error || 'Failed to generate video.');
        setAppState(AppState.ERROR);
      }
    } catch (err) {
      setError('An unexpected error occurred.');
      setAppState(AppState.ERROR);
    }
  };

  // Handle restart
  const handleRestart = () => {
    setAppState(AppState.INITIAL);
    setInputText('');
    setScriptText('');
    setVideoPath('');
    setError('');
    setScriptPath('');
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-12 text-center">
        <h1 className="text-4xl font-bold mb-2">Create Videos with AI</h1>
        <p className="text-xl text-gray-600">
          Transform your ideas into cinematic experiences
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Step 1: Text Input */}
      {(appState === AppState.INITIAL || appState === AppState.GENERATING_SCRIPT) && (
        <Card title="Step 1: What's your story about?">
          <TextArea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Describe what you want your video to be about..."
            label="Enter a description or prompt for your video"
            rows={5}
            disabled={appState === AppState.GENERATING_SCRIPT}
          />
          <div className="mt-4">
            <Button
              onClick={handleGenerateScript}
              loading={appState === AppState.GENERATING_SCRIPT}
              disabled={appState === AppState.GENERATING_SCRIPT || !inputText.trim()}
            >
              Generate Script
            </Button>
          </div>
        </Card>
      )}

      {/* Step 2: Script Editing */}
      {(appState === AppState.SCRIPT_READY ||
        appState === AppState.GENERATING_VIDEO ||
        appState === AppState.VIDEO_READY) && (
        <Card title="Step 2: Edit Your Script" className="mb-8">
          <TextArea
            value={scriptText}
            onChange={(e) => setScriptText(e.target.value)}
            label="Edit your script as needed"
            rows={10}
            disabled={appState === AppState.GENERATING_VIDEO}
          />
          <div className="mt-4 flex flex-wrap gap-3 items-center">
            <Select
              options={availableStyles}
              value={videoStyle}
              onChange={(e) => setVideoStyle(e.target.value)}
              label="Video Style"
              disabled={appState === AppState.GENERATING_VIDEO}
            />
            <Button
              onClick={handleGenerateVideo}
              loading={appState === AppState.GENERATING_VIDEO}
              disabled={
                appState === AppState.GENERATING_VIDEO || !scriptText.trim()
              }
              className="ml-auto"
            >
              Generate Video
            </Button>
          </div>
        </Card>
      )}

      {/* Step 3: Video Display */}
      {appState === AppState.GENERATING_VIDEO && (
        <Card title="Step 3: Video Generation" className="mb-8">
          <div className="py-16 flex flex-col items-center justify-center">
            <Loader size="large" className="mb-4" />
            <p className="text-gray-600">
              Creating your video... This may take a few minutes.
            </p>
          </div>
        </Card>
      )}

      {appState === AppState.VIDEO_READY && videoPath && (
        <Card title="Step 3: Your Video" className="mb-8">
          <div className="aspect-video bg-black rounded-lg overflow-hidden mb-4">
            <video
              src={FilmmakerAPI.getFileUrl(videoPath)}
              controls
              className="w-full h-full"
              poster="/video-poster.jpg"
            />
          </div>
          <div className="flex justify-between">
            <Button
              variant="secondary"
              onClick={handleRestart}
            >
              Create New Video
            </Button>
            <a
              href={FilmmakerAPI.getFileUrl(videoPath)}
              download
              className="btn-primary inline-block"
            >
              Download Video
            </a>
          </div>
        </Card>
      )}
    </div>
  );
} 