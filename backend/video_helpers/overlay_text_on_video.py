from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
from PIL import Image, ImageDraw, ImageFont

# Load the video file
#video = VideoFileClip("src/output-main.mp4")

# words will come from the Transcription object
#words = [{'word': 'Nathalie', 'start': 0.0, 'end': 0.5}, {'word': 'introduced', 'start': 0.5, 'end': 1.2000000476837158}, {'word': 'Earth', 'start': 1.2000000476837158, 'end': 1.5800000429153442}, {'word': 'Class', 'start': 1.5800000429153442, 'end': 2.0199999809265137}, {'word': 'Mail', 'start': 2.0199999809265137, 'end': 2.259999990463257}, {'word': 'a', 'start': 2.940000057220459, 'end': 2.9800000190734863}, {'word': 'service', 'start': 2.9800000190734863, 'end': 3.259999990463257}, {'word': 'that', 'start': 3.259999990463257, 'end': 3.6600000858306885}, {'word': 'digitized', 'start': 3.6600000858306885, 'end': 4.21999979019165}, {'word': 'physical', 'start': 4.21999979019165, 'end': 4.599999904632568}, {'word': 'mail', 'start': 4.599999904632568, 'end': 4.980000019073486}, {'word': 'allowing', 'start': 5.699999809265137, 'end': 5.760000228881836}, {'word': 'nomads', 'start': 5.760000228881836, 'end': 6.260000228881836}, {'word': 'to', 'start': 6.260000228881836, 'end': 6.800000190734863}, {'word': 'manage', 'start': 6.800000190734863, 'end': 6.800000190734863}, {'word': 'their', 'start': 6.800000190734863, 'end': 7.119999885559082}, {'word': 'correspondence', 'start': 7.119999885559082, 'end': 7.679999828338623}, {'word': 'from', 'start': 7.679999828338623, 'end': 8.140000343322754}, {'word': 'anywhere', 'start': 8.140000343322754, 'end': 8.520000457763672}]


# Function to create text from words and add to video
def create_text_clip(words_chunk, start_time, end_time):
    text = ' '.join([word['word'] for word in words_chunk])
    txt_clip = TextClip(
            text,
            font='DejaVuSans', # Change Font if not found
            fontsize=64,
            color="white",
            align='center',
            method='caption',
            size=(820, None),
            bg_color="black"
        )
    txt_clip = txt_clip.set_start(start_time).set_end(end_time).set_position(('center', 200))
    return txt_clip

def subtitles_main(words, video):
    WORDS_PER_SCREEN = 8

    # Create a list to hold all the TextClips
    text_clips = []
    # Create TextClips for each chunk of 8 words
    i = 0
    while i < len(words):
        words_chunk = words[i:i+WORDS_PER_SCREEN]
        start_time = words_chunk[0]['start']
        end_time = words_chunk[-1]['end']
        text_clips.append(create_text_clip(words_chunk, start_time, end_time))
        i += WORDS_PER_SCREEN

    # Composite video with text
    final_video = CompositeVideoClip([video] + text_clips)

    # Write the final video to a file
    # #final_video.write_videofile("src/output_with_text.mp4", codec="libx264", fps=video.fps)
    return final_video


#subtitles_main(words, video)