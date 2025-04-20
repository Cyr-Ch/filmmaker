import os
import argparse
from book_to_chunks.epub_to_chunks import process_epub
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json
import re
from .pipeline import pipeline

# Locate the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
#from ..book_to_chunks.epub_to_chunks import process_epub

# SCRIPT = "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go. Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere. Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states. A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road. She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space. The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing. These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality."
# prompt: make a claude api call and pass in the chapter
prompt = '''You are the world's best video creator for viral TikTok videos. You summarize books into digestible 60-second infotainment TikTok videos for each chapter. Take into account the following [[key elements]] and generate a narrative summary for this [[chapter]]. Always remember to prioritize making the script feel natural, and conversational. Your narrative summary should be able to fit into a 30 second video. Don't include emoji or anything else other than the summary itself in your answer. Don't make any intros, jump straight into the chapter summary content (don't say this is a summary).

[[Key Elements]] for Popular Infotainment Videos:
Script Elements:
Strong hook (first 3-5 seconds)
Clear, concise information
Storytelling approach
Actionable tips or takeaways
Call-to-action (CTA)
Voice Elements:
Engaging and energetic tone
Clear enunciation
Pacing that matches visual elements
Use of pauses for emphasis
Video Elements:
Eye-catching visuals
On-screen text for key points
Transitions and effects
Relevant background music
Subtitles for accessibility
'''
import anthropic

client = anthropic.Anthropic()


def get_script_from_chunk(chunk):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Summarize this chapter and just output the script, nothing else [[chapter]] " + chunk
                    }
                ]
            }
        ]
    )
    return message.content[0].text


def get_all_scripts_from_json(json_file):
    with open(json_file) as f:
        data = json.load(f)

    for i, item in enumerate(data):
        chunk = item['content']
        script = get_script_from_chunk(chunk)
        data[i]['script'] = script
        print(script)


# Given the json file, and chunk number, create the video for it
def make_video(json_file, i):
    with open(json_file) as f:
        data = json.load(f)

    script = data[i]['script']
    pipeline(script, f"data/output_{i}.mp4")


def make_epub_and_scripts(epub_file):
    json_file_name = process_epub(epub_file)
    # with open('../data/book.json', 'w') as f:
    #     json.dump(json_data, f)

    # with open(epub_file) as f:
    #     text = f.read()

    get_all_scripts_from_json(json_file_name)
    return json_file_name


#make_video("../data/Summarize Text Data.json", 5)


def get_script_from_json(json_file, i):
    with open(json_file) as f:
        data = json.load(f)

    chunk = data[i]['content']
    script = get_script_from_chunk(chunk)
    return script


def make_epub_and_one_script_and_one_video(epub_file, mp4_output_file):
    json_data = process_epub(epub_file)
    with open('../data/book.json', 'w') as f:
        json.dump(json_data, f)

    script = get_script_from_json('../data/book.json')
    pipeline(script, mp4_output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process an EPUB file and create video scripts.')
    parser.add_argument('epub_file', type=str, help='Path to the EPUB input file')
    parser.add_argument('mp4_file', type=str, help='Path to the mp4 output file')
    parser.add_argument('video_style', type=str, help='Style of the video')
    # video_style is one of the options from src/web/video-style-options.json

    args = parser.parse_args()

    script = get_script_from_chunk(open(args.epub_file).read())

    pipeline(script, args.mp4_file, args.video_style)

    #make_epub_and_one_script_and_one_video(args.epub_file, args.mp4_file)

