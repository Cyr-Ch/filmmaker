import requests

response = requests.get("https://replicate.delivery/yhqm/hoIjcD198XYnOlYGlsfUX3DeBfW75vPUwMNdOZJqp1MeikPMB/infinit_zoom.mp4")
with open('../data/video.mp4', 'wb') as file:
    file.write(response.content)