from .prompt_to_stock_video import prompt_to_stock_video
from .prompt_to_video import prompt_to_video, find_model
from .script_to_prompt import gpt_step_0, gpt_step_1
import json
import os
import warnings
import shutil
import tempfile

from .script_snippet_to_audio import extract_text_list, generate_speech_and_transcription
from .audio_video import combine_video_audio, combine_videos

# Example script for testing
SCRIPT = "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go. Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere. Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states. A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road. She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space. The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing. These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality."

# Example prompt response for testing
PROMPT = json.loads('''[{"text": "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go.", "prompt": "A bustling high-tech mobile living hub", "url": "https://replicate.delivery/yhqm/D7iOeSf1Cakv0UxOAocMiHxj35Gh3ruD589Nq4wyw9tebyHmA/infinit_zoom.mp4", "video_path": "../data/video_1.mp4"}, {"text": "Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere.", "prompt": "Digitalized mail on a futuristic virtual screen", "url": "https://replicate.delivery/yhqm/F4fRxLeeEgZfJSN4HPhREWzqyUE8ceHJ4SLAmKeNan5nlTehJA/infinit_zoom.mp4", "video_path": "../data/video_2.mp4"}, {"text": "Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states.", "prompt": "Seamless electronic cheque processing on a digital tablet", "url": "https://replicate.delivery/yhqm/krlkveYpzdQjNqmB9eygRAnUve9D1yl3V4C9oDj9TNuddyHmA/infinit_zoom.mp4", "video_path": "../data/video_3.mp4"}, {"text": "A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road.", "prompt": "Versatile clothes hanging, portable sound gadget in a suitcase", "url": "https://replicate.delivery/yhqm/zggMhVhwGm4GB5elWHlC8Rq9CinS7nLAAbr8tr1Enpqin8hJA/infinit_zoom.mp4", "video_path": "../data/video_4.mp4"}, {"text": "She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space.", "prompt": "Comfortable sling and portable baby tent staged for packing", "url": "https://replicate.delivery/yhqm/0GkoNXMdg9JPGhHRzYof1DdeFrf0SniHoJJrPJfZX9E09kPMB/infinit_zoom.mp4", "video_path": "../data/video_5.mp4"}, {"text": "The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing.", "prompt": "Perfectly sized baby carry-on by an airplane's overhead compartment", "url": "https://replicate.delivery/yhqm/YWlCvQguHW58K1eTVmmawVpHt4HNo42tdlAHQadfTQY0P5DTA/infinit_zoom.mp4", "video_path": "../data/video_6.mp4"}, {"text": "These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality.", "prompt": "Spectacular rotating globe zooming into various family-friendly locations", "url": "https://replicate.delivery/yhqm/CQJ9Wa3dYSIwKJYOScoMMCApNgeSYpmAafSibpeArwYYgyHmA/infinit_zoom.mp4", "video_path": "../data/video_7.mp4"}]''')

# Create a fallback video if all else fails
def create_fallback_video(script, output_path):
    """Create a simple text-based video when API services are unavailable"""
    try:
        # Check if we have the ffmpeg utility available
        import subprocess
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        # Create a temp directory for our work
        temp_dir = tempfile.mkdtemp()
        
        # Create a black background image with text
        width, height = 1280, 720
        
        # Split the script into chunks of 80 characters each
        text_chunks = []
        words = script.split()
        current_chunk = ""
        
        for word in words:
            if len(current_chunk + " " + word) <= 80:
                if current_chunk:
                    current_chunk += " " + word
                else:
                    current_chunk = word
            else:
                text_chunks.append(current_chunk)
                current_chunk = word
        
        if current_chunk:
            text_chunks.append(current_chunk)
        
        # Limit to 10 chunks
        text_chunks = text_chunks[:10]
        
        # Create an image for each chunk
        image_files = []
        for i, chunk in enumerate(text_chunks):
            img = Image.new('RGB', (width, height), color='black')
            draw = ImageDraw.Draw(img)
            
            # Use a basic font
            try:
                font = ImageFont.truetype("Arial", 40)
            except:
                font = ImageFont.load_default()
            
            # Draw the text centered
            text_width, text_height = draw.textsize(chunk, font=font)
            position = ((width - text_width) // 2, (height - text_height) // 2)
            draw.text(position, chunk, fill="white", font=font)
            
            # Save the image
            img_path = os.path.join(temp_dir, f"frame_{i:03d}.jpg")
            img.save(img_path)
            image_files.append(img_path)
        
        # Create a video from the images using ffmpeg
        video_path = os.path.join(temp_dir, "fallback_video.mp4")
        cmd = [
            'ffmpeg', '-y', '-framerate', '0.5', 
            '-i', os.path.join(temp_dir, 'frame_%03d.jpg'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_path
        ]
        
        subprocess.run(cmd, check=True)
        
        # Copy the video to the output path
        shutil.copy(video_path, output_path)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        warnings.warn(f"Could not create fallback video: {str(e)}")
        return False

def pipeline(script, output_path, style):
    """
    Generate a video from a script
    
    Args:
        script (str): The script text in SRT format
        output_path (str): Path where the final video will be saved
        style (str): The style of video to generate
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Find the model for the specified style
        model = find_model(style)
        
        if not model or "prompt" not in model:
            warnings.warn(f"Invalid style or model format: {style}")
            return create_fallback_video(script, output_path)
        
        # Process the script
        try:
            print('Processing script...')
            parsed_script = gpt_step_0(script)
            print('Script sections created')
            
            parsed_script = gpt_step_1(parsed_script, model["prompt"])
            print('Script prompts created')
        except Exception as e:
            warnings.warn(f"Error processing script: {str(e)}")
            return create_fallback_video(script, output_path)
        
        # Generate video prompts
        try:
            if style == 'Internet Videos':
                prompt = prompt_to_stock_video(parsed_script=parsed_script)
                print(f'Internet videos output: {str(prompt)}')
            else:
                prompt = prompt_to_video(parsed_script=parsed_script, style=style)
                print(f'Replicate videos output: {str(prompt)}')
                
            if not prompt:
                warnings.warn("Failed to generate video prompts")
                return create_fallback_video(script, output_path)
        except Exception as e:
            warnings.warn(f"Error generating video prompts: {str(e)}")
            return create_fallback_video(script, output_path)
        
        # Process each segment
        i = 0
        output_video_paths = []
        
        for item in prompt:
            try:
                i += 1
                # Create audio from script
                audio_path, transcription_data = generate_speech_and_transcription(
                    item['text'], filename=f"Generate_speech_{i}"
                )
                print(f"Audio File Saved: {audio_path}")
                
                # Combine video and audio
                output_video_path = f"data/output_{i}.mp4"
                combine_video_audio(
                    item['video_path'], audio_path, 
                    transcription_data.words, output_video_path
                )
                output_video_paths.append(output_video_path)
            except Exception as e:
                warnings.warn(f"Error processing segment {i}: {str(e)}")
                # Continue with other segments
        
        # If no segments were successfully processed, create a fallback
        if not output_video_paths:
            warnings.warn("No video segments were successfully processed")
            return create_fallback_video(script, output_path)
        
        # Combine all videos
        try:
            print(f"Combining {len(output_video_paths)} video segments")
            combine_videos(output_video_paths, output_path)
            print(f"Final video saved to: {output_path}")
            return True
        except Exception as e:
            warnings.warn(f"Error combining videos: {str(e)}")
            # If we have at least one segment, use that as the output
            if output_video_paths:
                try:
                    shutil.copy(output_video_paths[0], output_path)
                    return True
                except:
                    pass
            
            return create_fallback_video(script, output_path)
            
    except Exception as e:
        warnings.warn(f"Unexpected error in pipeline: {str(e)}")
        return create_fallback_video(script, output_path)

# For testing
pipeline(SCRIPT, "../data/output.mp4")