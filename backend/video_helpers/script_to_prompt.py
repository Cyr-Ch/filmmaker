import os
from dotenv import load_dotenv, find_dotenv
import json
import warnings

# Locate the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

# Mock response data for when OpenAI API key is not available
MOCK_SECTIONS_RESPONSE = '''[
    {"text": "Section 1: Introduction to the story or concept."},
    {"text": "Section 2: Character or element introduction."},
    {"text": "Section 3: Development of the situation or concept."},
    {"text": "Section 4: Exploration of details or examples."},
    {"text": "Section 5: Conclusion or resolution of the concept."}
]'''

MOCK_PROMPTS_RESPONSE = '''[
    {"text": "Section 1: Introduction to the story or concept.", "prompt": "A deep, endless hallway with soft lighting"},
    {"text": "Section 2: Character or element introduction.", "prompt": "A person standing at the beginning of a forest path"},
    {"text": "Section 3: Development of the situation or concept.", "prompt": "A winding road disappearing into the horizon"},
    {"text": "Section 4: Exploration of details or examples.", "prompt": "A series of connected rooms with objects on display"},
    {"text": "Section 5: Conclusion or resolution of the concept.", "prompt": "A vast open landscape with a path leading to the distance"}
]'''

# Initialize OpenAI client if API key is available
client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI()
    except ImportError:
        warnings.warn("OpenAI package not installed. Mock responses will be used.")
else:
    warnings.warn("OpenAI API key not found. Mock responses will be used.")

# SCRIPT = "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go. Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere. Andrew chimed in, adding that he used GreenByPhone to process checks electronically, creating a seamless financial system across different states. A seasoned female traveler and new mom then offered her insights, recommending quick-dry, versatile clothing from Athleta, and essential gadgets like a portable sound machine for better sleep on the road. She didn't stop there, sharing her must-haves for traveling with a baby, including a comfortable sling and a portable tent that doubled as a familiar sleep space. The conversation concluded with tips on navigating air travel with little ones, from choosing the right carry-on size to keeping babies comfortable during takeoff and landing. These modern adventurers had cracked the code to effortless, family-friendly globe-trotting, turning the dream of a flexible, location-independent lifestyle into a reality."

def gpt_step_0(script):
    """Break script into sections"""
    # Locate the .env file
    print("Loading environment variables...")
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')    
    # Initialize OpenAI client if API key is available
    client = None
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI()
        except ImportError:
            warnings.warn("OpenAI package not installed. Mock responses will be used.")
    else:
        warnings.warn("OpenAI API key not found. Mock responses will be used.")
    print("Initializing OpenAI client...")
    print(OPENAI_API_KEY)
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
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
        except Exception as e:
            warnings.warn(f"Error calling OpenAI API: {str(e)}. Using mock response.")
            return MOCK_SECTIONS_RESPONSE
    else:
        # Use mock response if OpenAI client is not available
        print("Using mock response for script sections (no OpenAI API key)")
        return MOCK_SECTIONS_RESPONSE

def gpt_step_1(code, prompt):
    """Add prompts to each section"""
    # Locate the .env file
    print("Loading environment variables...")
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')    
    # Initialize OpenAI client if API key is available
    client = None
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI()
        except ImportError:
            warnings.warn("OpenAI package not installed. Mock responses will be used.")
    else:
        warnings.warn("OpenAI API key not found. Mock responses will be used.")
    print("Initializing OpenAI client...")
    print(OPENAI_API_KEY)
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
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
            # Try to parse the response as JSON
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                warnings.warn("Could not parse OpenAI response as JSON. Using mock response.")
                return json.loads(MOCK_PROMPTS_RESPONSE)
        except Exception as e:
            warnings.warn(f"Error calling OpenAI API: {str(e)}. Using mock response.")
            return json.loads(MOCK_PROMPTS_RESPONSE)
    else:
        # Use mock response if OpenAI client is not available
        print("Using mock response for script prompts (no OpenAI API key)")
        return json.loads(MOCK_PROMPTS_RESPONSE)

# Debug functions to test the script
# Step 1: Request it to turn the script into sections in an array / json object under the label 'text'
# Step 2: Pass in the code generated previously and ask it to create prompts from these sections and add them under the label 'prompt' -- specifically scenes that could realistically have infinite zoom, like a hallway or forest path

# response = gpt_step_0(SCRIPT)
# print(response)
# response = gpt_step_1(response)
# print("BREAK")
# print(response)