import os
from config.dev import IMAGE_OUTPUT_DIR


def get_image_from_cache(word):
    filepath = os.path.join(IMAGE_OUTPUT_DIR, f"{word}.png")
    if os.path.exists(filepath):
        return filepath
    return None