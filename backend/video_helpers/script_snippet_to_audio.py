#https://replicate.com/lucataco/xtts-v2

from openai import OpenAI
from pathlib import Path

def extract_text_list(data):
    # Initialize an empty list to store extracted texts
    extracted_texts = []
    # Iterate through each item in the list
    for item in data:
        # Check if 'text' key exists in the dictionary
        if 'text' in item:
            # Add the text to the extracted_texts list
            extracted_texts.append(item['text'])
        else:
            # Raise an error if any item in the list lacks a 'text' key
            raise ValueError("Missing 'text' key in some items")
    
    # Check if the extracted_texts list is empty
    if not extracted_texts:
        # Raise an error if no text was extracted
        raise ValueError("No texts were extracted from the input data")
    
    # Return the list of extracted texts
    return extracted_texts

def generate_speech_and_transcription(text, filename):
    client = OpenAI()
    
    speech_file_path = Path("data/" + filename + ".mp3")
    
    speech_response = client.audio.speech.create(
        model="tts-1",  # Choose the model
        voice="alloy",  # Choose the voice
        input=text
    )
    speech_response.stream_to_file(speech_file_path)
  
    with open(speech_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",  
            timestamp_granularities=["word"]  
        )
    
    return str(speech_file_path), transcription


# extracted_texts_list = extract_text_list(input)
# for i, text in enumerate(extracted_texts_list):
#   audio_path, transcription_data = generate_speech_and_transcription(text, filename="Generate_speech_"+str(i))
  # print(f"Audio File Saved: {audio_path}")
  # print("Transcription Data:", transcription_data)
