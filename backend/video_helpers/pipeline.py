from .prompt_to_stock_video import prompt_to_stock_video
from .prompt_to_video import prompt_to_video, find_model
from .script_to_prompt import gpt_step_0, gpt_step_1
import json

from .script_snippet_to_audio import extract_text_list, generate_speech_and_transcription
from .audio_video import combine_video_audio, combine_videos

# create script from text files
SCRIPT = "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go. Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere. Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states. A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road. She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space. The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing. These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality."

PROMPT = json.loads('''[{"text": "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go.", "prompt": "A bustling high-tech mobile living hub", "url": "https://replicate.delivery/yhqm/D7iOeSf1Cakv0UxOAocMiHxj35Gh3ruD589Nq4wyw9tebyHmA/infinit_zoom.mp4", "video_path": "../data/video_1.mp4"}, {"text": "Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere.", "prompt": "Digitalized mail on a futuristic virtual screen", "url": "https://replicate.delivery/yhqm/F4fRxLeeEgZfJSN4HPhREWzqyUE8ceHJ4SLAmKeNan5nlTehJA/infinit_zoom.mp4", "video_path": "../data/video_2.mp4"}, {"text": "Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states.", "prompt": "Seamless electronic cheque processing on a digital tablet", "url": "https://replicate.delivery/yhqm/krlkveYpzdQjNqmB9eygRAnUve9D1yl3V4C9oDj9TNuddyHmA/infinit_zoom.mp4", "video_path": "../data/video_3.mp4"}, {"text": "A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road.", "prompt": "Versatile clothes hanging, portable sound gadget in a suitcase", "url": "https://replicate.delivery/yhqm/zggMhVhwGm4GB5elWHlC8Rq9CinS7nLAAbr8tr1Enpqin8hJA/infinit_zoom.mp4", "video_path": "../data/video_4.mp4"}, {"text": "She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space.", "prompt": "Comfortable sling and portable baby tent staged for packing", "url": "https://replicate.delivery/yhqm/0GkoNXMdg9JPGhHRzYof1DdeFrf0SniHoJJrPJfZX9E09kPMB/infinit_zoom.mp4", "video_path": "../data/video_5.mp4"}, {"text": "The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing.", "prompt": "Perfectly sized baby carry-on by an airplane's overhead compartment", "url": "https://replicate.delivery/yhqm/YWlCvQguHW58K1eTVmmawVpHt4HNo42tdlAHQadfTQY0P5DTA/infinit_zoom.mp4", "video_path": "../data/video_6.mp4"}, {"text": "These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality.", "prompt": "Spectacular rotating globe zooming into various family-friendly locations", "url": "https://replicate.delivery/yhqm/CQJ9Wa3dYSIwKJYOScoMMCApNgeSYpmAafSibpeArwYYgyHmA/infinit_zoom.mp4", "video_path": "../data/video_7.mp4"}]''')

def pipeline(script, output_path, style):
    
    model = find_model(style)

    if model and "prompt" in model:

    # create video from script
        print('script: ',script)
        parsed_script = gpt_step_0(script)
        print('parsed_script 1: ', parsed_script)

        parsed_script = gpt_step_1(parsed_script, model["prompt"])
        print('parsed_script 2: ', parsed_script)


        if style == 'Internet Videos':
            prompt = prompt_to_stock_video(parsed_script = parsed_script)
            print (f'Internet videos output: ' + str(prompt))
        else:
            prompt = prompt_to_video(parsed_script = parsed_script, style = style)
            print (f'Replicate videos output: ' + str(prompt))
        
        i = 0
        output_video_paths = []
        for item in prompt:
            i += 1
            # create audio from script
            audio_path, transcription_data = generate_speech_and_transcription(item['text'], filename="Generate_speech_"+str(i))
            print(f"Audio File Saved: {audio_path}")
            print(f"transcription_data: {transcription_data}")
            # combine video and audio
            output_video_path = "data/output_"+str(i)+".mp4"
            combine_video_audio(item['video_path'], audio_path, transcription_data.words, output_video_path)
            output_video_paths.append(output_video_path)
        
        # combine all videos together
        # output_video_paths = ['../data/output_1.mp4', '../data/output_2.mp4', '../data/output_3.mp4', '../data/output_4.mp4', '../data/output_5.mp4', '../data/output_6.mp4', '../data/output_7.mp4']
        print(output_video_paths)
        combine_videos(output_video_paths, output_path)
        
# pipeline(SCRIPT, "../data/output.mp4")