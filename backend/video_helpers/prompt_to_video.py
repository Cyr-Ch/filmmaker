import replicate
import requests
import os
import json

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

def find_model(style):
    f = open("./web/src/video-style-options.json")
    style_json = json.load(f)
    print('Video style json file loaded successfully!')
    for model in style_json:
        if model['name'] == style:
            print('Found model preference: ')
            print(model)
            return model
    print (f'{style} does not exist in the json file.')
    return None

def process_replicate_output(output):
    if isinstance(output, str):
        return output
    elif isinstance(output, dict) and "mp4" in output:
        return output["mp4"]
    else:
        return None 

def prompt_to_video(parsed_script, style):
    
    #find the model parameters in json file
    model = find_model(style)

    if model:
      model_id = model['model']
      model_input = model['modelInput']

      result = []
      i = 0
      for snippet in parsed_script:
          model_input['prompt'] = snippet['prompt']
          print(f'Ready to run {style} model with input: ')
          print(model_input)
          
          i += 1

          output = replicate.run(
              model_id,
              input = model_input
          )
          snippet["url"] = process_replicate_output(output)
          print(f'Replicate has returned output: ')
          print(output)

          #download the video from the returned replicate url
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

#example
# test_result = prompt_to_video(parsed_script = YOUR_SCRIPT)
# print(test_result)
# [{'text': 'In a world where efficient travel and remote living were becoming increasingly important, a group of savvy globetrotters shared their secrets for streamlining life on the go.', 'prompt': 'Discussing travel efficiency and remote living', 'mp4': 'https://replicate.delivery/yhqm/cgSR0J05zFI4Bl6pVZvlGVG4TQIQpY3fME5FOXsedUaEI3DTA/infinit_zoom.mp4'%7D, {'text': 'Nathalie introduced Earth Class Mail, a service that digitized physical mail, allowing nomads to manage their correspondence from anywhere.', 'prompt': 'Introducing digital mail for nomads', 'mp4': 'https://replicate.delivery/yhqm/HCWOIYoB3exMW6kyvn8YfrIsfjxvWfB5X7KjxjxRWarOhcPMB/infinit_zoom.mp4'%7D]

if __name__ == "__main__":
    prompt_to_video()