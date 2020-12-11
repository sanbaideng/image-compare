from moviepy.video.io.ffmpeg_writer import ffmpeg_write_image
from moviepy.editor import VideoFileClip



clip = (VideoFileClip("lzr.mp4")  # File containing the original video
        .subclip(3, 13)  # cut between t=23 and 47 seconds
        .fadein(1).fadeout(1)
        .audio_fadein(1).audio_fadeout(1))
clip.write_videofile("lzr2.mp4")
