import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json

# Locate the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

client = OpenAI()

# SCRIPT = "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go. Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere. Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states. A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road. She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space. The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing. These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality."

def gpt_step_0(script):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Break this script into sections for a video. Each section will be its own 'scene' in the video. Please return as an array / json object with each section under the label 'text'. Script: " + script},
                ],
            }
        ],
        max_tokens=400,
    )
    return response.choices[0].message.content

def gpt_step_1(code, prompt):
    '''
    Sample output:
    [
        {
        "text": "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go.",
        "prompt": "Views of different modes of transport"
        },
        {
        "text": "Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere.",
        "prompt": "Digital screen showing incoming mail"
        },
        {
        "text": "Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states.",
        "prompt": "Electronic checks being scanned and processed"
        },
        {
        "text": "A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road.",
        "prompt": "Display of travel-friendly clothing and gadgets"
        },
        {
        "text": "She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space.",
        "prompt": "Baby travel essentials scattered on a table"
        },
        {
        "text": "The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing.",
        "prompt": "Inside of an empty airplane cabin"
        },
        {
        "text": "These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality.",
        "prompt": "Globe spinning with different countries highlighted"
        }
    ]
    '''
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", 
                     "text": prompt + "Add these to the JSON object with the label 'prompt' and keep the original 'text' section. Code: " + code},
                ],
            }
        ],
        max_tokens=800,
    )
    print(response)
    return json.loads(response.choices[0].message.content)


# Step 1: Request it to turn the script into sections in an array / json object under the label 'text'
# Step 2: Pass in the code generated previously and ask it to create prompts from these sections and add them under the label 'prompt' -- specifically scenes that could realistically have infinite zoom, like a hallway or forest path

# response = gpt_step_0(SCRIPT)
# print(response)
# response = gpt_step_1(response)
# print("BREAK")
# print(response)