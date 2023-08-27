from moviepy.editor import *
import os
import sys
import random
from moviepy.video.fx.all import crop

def main(videoname, seriesname, audioname):
    video_clip = VideoFileClip(rf"background\{videoname}").without_audio()
    audio_clip = AudioFileClip(rf"audiostories\{seriesname}")
    audio_duration = audio_clip.duration

    start_time = random.random()*(video_clip.duration - audio_clip.duration - 60)

    full_video = video_clip.subclip(start_time, start_time + audio_clip.duration)
    (w, h) = full_video.size
    full_video = crop(full_video, width=608, height=1080, x_center=w/2, y_center=h/2)
    full_video = full_video.set_audio(audio_clip)

    clips = []

    while full_video.duration > 60:
        clips.append(full_video.subclip(0, 60))
        full_video = full_video.subclip(55, full_video.duration)

    clips.append(full_video.subclip(0, full_video.duration))

    for (i,c) in enumerate(clips):
        c.write_videofile(rf"output\{seriesname[:seriesname.index('.mp3')]}_part{i+1}.mp4")
        

if __name__ == "__main__":
    n = len(sys.argv)

    if n < 4:
        print("Please provide the name of the video, series, and audio")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])



