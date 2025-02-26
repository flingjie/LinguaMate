from llm.chat import get_response_from_llm


def get_word_hint(word):
    prompt = f"""
You are an experienced English teacher.  
Your task is to generate corresponding descriptions based on the input words by creating stories and using visual associations to enhance word memory.

## restrict
- Only return visual descriptions, do not return other content, otherwise you will be punished
- Return no more than 100 words

## word
 {word}
"""
    result = get_response_from_llm(prompt)
    return result

if __name__ == "__main__":
    word = "workaholic"
    result = get_word_hint(word)
    print(result)
