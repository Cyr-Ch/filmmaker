# FFMPEG commands

# Embed subtitles
```bash
ffmpeg -i input.mp4 -i subtitles.srt -c:v copy -c:a copy -c:s mov_text output.mp4
```

# Merge multiple videos
```bash
ffmpeg -i "input1.mp4[input1] -i "input2.mp4[input2] -i "input3.mp4[input3] -filter_complex "[input1][input2][input3]concat" -c:v libx264 -c:a aac -movflags faststart output.mp4
```

# Some more ffmpeg commands
```
printf "file '%s'\n" scene1_350227355493707788.mp4 scene2_350222075787694084.mp4 scene3_350230471672844290.mp4 scene4_350233663471063043.mp4 scene5_350234908378251272.mp4 > file_list.txt && ffmpeg -f concat -safe 0 -i file_list.txt -c copy output.mp4


ffmpeg -i output.mp4 -vf "subtitles=output.srt:force_style='FontSize=24'" -c:a copy output_hardcoded.mp4
```