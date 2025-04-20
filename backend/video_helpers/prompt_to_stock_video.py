from litellm import completion
from dotenv import load_dotenv
from tqdm import tqdm
import os
import requests


TEST_SCRIPT= [
  {
    "text": "In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go.",
    "prompt": "Discussing travel efficiency and remote living"
  },
  {
    "text": "Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere.",
    "prompt": "Introducing digital mail for nomads"
  }
]


def script2url(script):
  # through 1:
  # scene

  scene_res = completion(
    model="gpt-3.5-turbo",
    messages=[
      { "content": "Imagine the following script is a part of a video book. What is the perfect background video for the script? It can only be a single shot of some scene: \n" + script, "role": "user"}
      ]
  )

  # through 2:
  # query keywords

  query_keywords_res = completion(
    model="gpt-3.5-turbo",
    messages=[
      { "content": "Imagine the following script is a part of a video book. What is the perfect background video for the script? It can only be a single shot of some scene" + script, "role": "user"}, 
      scene_res.choices[0].message, 
      { "content": "Describe this video with up to 5 keywords for a video search query. Write them single line, space separated", "role": "user"}
      ]
  )
  query_kerywords = query_keywords_res.choices[0].message["content"].replace("\n", "").replace(".", "").replace(",", "").lower()

  # out:
  # stock video

  video_res = requests.get("https://api.pexels.com/videos/search?orientation=portrait&query=" + query_kerywords + "&per_page=1", headers={"Authorization": os.getenv("PEXELS_API_KEY")}).json()
  video_url = video_res["videos"][0]["video_files"][0]["link"]

  return video_url


def prompt_to_stock_video(parsed_script):
  print("Getting videos...")
  result = []
  
  for i, snippet in enumerate(tqdm(parsed_script)):
      
      output_url = script2url(snippet.get("text"))

      snippet["url"] = output_url

      response = requests.get(snippet["url"])

      if not os.path.exists("data"): 
            
          # if the demo_folder directory is not present  
          # then create it. 
          os.makedirs("data") 

      snippet["video_path"] = 'data/video_'+str(i)+'.mp4'
      with open(snippet["video_path"], 'wb') as file:
        # Write the content of the response to the file
        file.write(response.content)

      result.append(snippet)

  return result


if __name__ == "__main__":
    load_dotenv()
    print(prompt_to_video(TEST_SCRIPT))