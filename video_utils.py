import os
from moviepy.editor import ImageSequenceClip, VideoFileClip

def frames_to_video(frame_paths, out_path, fps=8):
    clip = ImageSequenceClip(frame_paths, fps=fps)
    clip.write_videofile(out_path, codec="libx264", fps=fps, verbose=False, logger=None)
    return out_path

def clip_to_stream(path):
    # For streaming if needed
    return open(path, "rb")
