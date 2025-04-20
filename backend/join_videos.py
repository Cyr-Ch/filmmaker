#!/usr/bin/env python3

import sys
from moviepy.editor import VideoFileClip, concatenate_videoclips
from datetime import datetime

def join_videos(video_files):
    if len(video_files) < 2:
        print("Error: Please provide at least 2 video files as arguments")
        sys.exit(1)

    try:
        # Load all video clips
        clips = [VideoFileClip(file) for file in video_files]
        
        # Concatenate clips
        final_clip = concatenate_videoclips(clips)
        
        # Generate output name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"joined_video_{timestamp}.mp4"
        
        # Write the result
        final_clip.write_videofile(output_name)
        
        # Close all clips to free up resources
        for clip in clips:
            clip.close()
        final_clip.close()
        
        print(f"Successfully created {output_name}")
        
    except Exception as e:
        print(f"Error while joining videos: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Remove script name from arguments
    video_files = sys.argv[1:]
    join_videos(video_files)
