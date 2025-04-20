import React, { useEffect, useRef, useState } from 'react';
import { StreamingAvatar as HeygenAvatar, TaskType } from '@heygen/streaming-avatar';

interface StreamingAvatarProps {
  text: string;
  avatarName?: string;
  token: string;
  onSessionStart?: (sessionId: string) => void;
  onSessionEnd?: () => void;
  onError?: (error: any) => void;
  autoPlay?: boolean;
}

const StreamingAvatar: React.FC<StreamingAvatarProps> = ({
  text,
  avatarName = 'Anna',
  token,
  onSessionStart,
  onSessionEnd,
  onError,
  autoPlay = true,
}) => {
  const [isReady, setIsReady] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const avatarRef = useRef<HeygenAvatar | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Initialize the avatar
    try {
      avatarRef.current = new HeygenAvatar({ token });
      setIsReady(true);
    } catch (err) {
      console.error('Failed to initialize avatar:', err);
      setError('Failed to initialize avatar');
      if (onError) onError(err);
    }

    return () => {
      // Clean up when component unmounts
      if (sessionId) {
        stopSession();
      }
    };
  }, [token]);

  useEffect(() => {
    // Start the session if text is provided and autoPlay is enabled
    if (isReady && text && autoPlay && !sessionId) {
      startSession();
    }
  }, [isReady, text, autoPlay]);

  const startSession = async () => {
    if (!avatarRef.current) {
      setError('Avatar not initialized');
      return;
    }

    try {
      setIsPlaying(true);
      const sessionData = await avatarRef.current.createStartAvatar({
        avatarName,
        quality: 'high',
        container: containerRef.current as HTMLElement,
      });

      setSessionId(sessionData.session_id);
      if (onSessionStart) onSessionStart(sessionData.session_id);

      // Speak the text
      await avatarRef.current.speak({
        sessionId: sessionData.session_id,
        text,
        task_type: TaskType.SPEAK,
      });

      setIsPlaying(false);
      if (onSessionEnd) onSessionEnd();
    } catch (err) {
      console.error('Error in streaming avatar:', err);
      setError('Failed to stream avatar');
      setIsPlaying(false);
      if (onError) onError(err);
    }
  };

  const stopSession = async () => {
    if (!avatarRef.current || !sessionId) return;

    try {
      await avatarRef.current.stopAvatar({ sessionId });
      setSessionId(null);
      setIsPlaying(false);
    } catch (err) {
      console.error('Error stopping avatar session:', err);
    }
  };

  return (
    <div className="streaming-avatar-container">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}
      
      <div 
        ref={containerRef} 
        className="aspect-video bg-black rounded-lg overflow-hidden relative"
        style={{ minHeight: '360px' }}
      >
        {!isPlaying && !sessionId && (
          <div className="absolute inset-0 flex items-center justify-center text-white">
            {isReady ? 'Avatar ready to stream' : 'Initializing avatar...'}
          </div>
        )}
      </div>
      
      {!autoPlay && isReady && !isPlaying && (
        <button
          onClick={startSession}
          className="mt-4 btn-primary"
          disabled={!text || isPlaying}
        >
          Play Avatar
        </button>
      )}
    </div>
  );
};

export default StreamingAvatar; 