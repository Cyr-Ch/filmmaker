from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip

from .overlay_text_on_video import subtitles_main

def crop_and_resize(video,target_width=1080,target_height=1350):
    # Resize if necessary
    if video.w < target_width or video.h < target_height:
        resize_factor = max(target_width / video.w, target_height / video.h)
        video = video.resize(resize_factor)    
        
    # Calculate the center coordinates of the video
    center_x = video.w / 2
    center_y = video.h / 2
    
    # Calculate the top-left coordinates of the crop box
    crop_x = center_x - target_width / 2
    crop_y = center_y - target_height / 2
    
    # Crop the video
    cropped_video = video.crop(x1=crop_x, y1=crop_y, width=target_width, height=target_height)

    return cropped_video
    
    

def combine_video_audio(video_path, audio_path, words, output_path):
    # Load the video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # Adjust video length to match audio length by repeating and cutting the video
    repeat_times = int(audio.duration // video.duration) + 1
    videos = [video] * repeat_times
    edited_video = concatenate_videoclips(videos)
    edited_video = edited_video.subclip(0, audio.duration)
    
    # Resize the video to 9:16 aspect ratio and 1080x1920 resolution
    #edited_video = edited_video.resize(newsize=(1080, 1920))
    cropped_video = crop_and_resize(edited_video,target_width=1080,target_height=1350)
    
    cropped_video = cropped_video.set_audio(audio)
    cropped_video = subtitles_main(words, cropped_video)
    
    cropped_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    

def combine_videos(video_paths, output_path):
    # Load all video clips
    video_clips = [VideoFileClip(video) for video in video_paths]
    
    # Concatenate the video clips
    final_clip = concatenate_videoclips(video_clips, method="compose")

    #add water mark
    watermark = ImageClip("./web/src/sundai_logo.png")
    watermark = watermark.set_opacity(0.6)
    watermark = watermark.set_duration(final_clip.duration)
    watermark = watermark.set_position(("right", "bottom"))

    final_video = CompositeVideoClip([final_clip, watermark])

    print("Watermark duration:", watermark.duration)
    print("Final video duration:", final_clip.duration)
    print("Final video size:", final_clip.size)

    
    # Write the final output video to the specified path
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
#combine_video_audio("../data/video1.mp4", "../data/audio1.wav", "../data/output.mp4")
# combine_video_audio("src/output.mp4", "src/replicate-prediction-evvvrghn4drj60cgd8xrtc403g.wav", "src/output-main.mp4")
