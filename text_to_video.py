import os
from video_utils import generate_dummy_video

def generate_from_text(prompt: str, duration: int = 5, output_dir: str = None) -> str:
    """
    THIS IS A SAFE PLACEHOLDER.
    Generates simple solid-color dummy video (3 seconds) for testing on Render.
    """
    output_path = os.path.join(output_dir or ".", "text_out.mp4")
    return generate_dummy_video(output_path)
