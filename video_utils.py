import os
from moviepy.editor import ImageSequenceClip, VideoFileClip
from moviepy.editor import ColorClip
def frames_to_video(frame_paths, out_path, fps=8):
    clip = ImageSequenceClip(frame_paths, fps=fps)
    clip.write_videofile(out_path, codec="libx264", fps=fps, verbose=False, logger=None)
    return out_path

def clip_to_stream(path):
    # For streaming if needed
    return open(path, "rb")

def generate_dummy_video(output_path):
    # 512x512 blue color ka 3-second video
    clip = ColorClip(size=(512, 512), color=(0, 128, 255), duration=3)
    clip.write_videofile(output_path, fps=24)
    return output_path
