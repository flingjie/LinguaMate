from llm.chat import get_response_from_llm
import random
from log import logger


def get_word_meaning(word):
    prompt = f"""
    You are a professional English teacher.
    Your task is to analyze the input word and provide a concise and accurate meaning in one sentence.

    ## word
    {word}
    """
    result = get_response_from_llm(prompt)
    return result


def get_word_hint(word, meaning, theme="realistic"):
    scene_templates = [
        f"A highly detailed depiction of '{word}', symbolizing {meaning}.",
        f"A surreal artistic representation of '{word}', visually expressing its meaning as {meaning}.",
        f"A cinematic scene illustrating '{word}', metaphorically showing {meaning}.",
        f"A fantasy-inspired vision of '{word}', creatively embodying {meaning}.",
        f"A thought-provoking, symbolic image of '{word}', emphasizing its concept as {meaning}.",
    ]
    
    # Select a random template
    scene_description = random.choice(scene_templates)
    scene_description = f"A thought-provoking, symbolic image of '{word}', emphasizing its concept as {meaning}."


    # Style descriptions based on the chosen theme
    styles = {
        "realistic": "hyper-realistic, ultra-detailed, 8K resolution, cinematic lighting",
        "fantasy": "dreamlike, ethereal, magical realism, glowing lights, fantasy art",
        "cyberpunk": "neon lights, futuristic cityscape, high-tech, cyberpunk aesthetics",
        "sketch": "hand-drawn illustration, vintage style, artistic, detailed pencil sketch"
    }

    style_description = styles.get(theme, styles["fantasy"])
    logger.info(f"style_description: {style_description}")
    # Combine everything into a final prompt
    prompt = f"""
{scene_description}\n {style_description}
"""
    result = get_response_from_llm(prompt)
    return result

if __name__ == "__main__":
    word = "workaholic"
    meaning = get_word_meaning(word)
    print(meaning)
    result = get_word_hint(word, meaning)
    print(result)
