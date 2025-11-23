import os
from moviepy.editor import TextClip
import tempfile

def generate_from_text(prompt: str, duration: int = 5, output_dir: str = None) -> str:
    """
    Replace this with the real text->video pipeline (ModelScope/Zeroscope/Diffusion model).
    The stub below creates a simple text overlay video for placeholder/testing.
    """
    

    w, h = 512, 512
    fps = 8
    txt_clip = TextClip(prompt[:300], fontsize=24, size=(w, h), method='caption')
    txt_clip = txt_clip.set_duration(duration)
    out_dir = output_dir or tempfile.mkdtemp()
    out_path = os.path.join(out_dir, "text_out.mp4")
    txt_clip.write_videofile(out_path, fps=fps, codec="libx264", verbose=False, logger=None)
    return out_path
