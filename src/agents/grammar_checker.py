from llm.chat import get_response_from_llm
import time
from config import ModelName


def is_grammer_right(text):
    prompt = f"""
You are a professional English teacher. 
Your job is to determine whether the user input contains grammatical errors and whether the second-person expression is reasonable. 
If there is a syntax error or unreasonable expression, 0 is returned, otherwise 1 is returned.

## restrict
- The result only returns 0 or 1, do not return to the inference process, otherwise you will be punished 

## user input
{text}
"""
    print(prompt)
    result = get_response_from_llm(prompt)
    return result == '1'


def get_suggestion(text):
    prompt = f"""
You are a professional English teacher. 
Your task is to analyze user input for grammatical errors or unreasonable expressions, 
point out problems and provide suggestions from a second-person perspective.

## user input
{text}
"""
    result = get_response_from_llm(prompt, model_name=ModelName.DEEPSEEK.value)
    return result

if __name__ == "__main__":
    text = 'I am thinking the question you said.'
    # text = 'hi'
    result = is_grammer_right(text)
    print(result)
    result = get_suggestion(text)
    print(result)
    