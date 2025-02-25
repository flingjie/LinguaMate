from config import ModelName, API_BASE
from litellm import completion
from utils.response import split_think_content
from log import logger


def get_response_from_llm(prompt, model_name=ModelName.QWEN.value):
    messages = [{"role": "user", "content": prompt}]
    return chat_with_llm(messages, model_name)


def chat_with_llm(messages, model_name=ModelName.QWEN.value):
    try:
        response = completion(
            model=model_name, 
            messages=messages,
            api_base=API_BASE
        )
        text = response.choices[0].message.content
        think, result = split_think_content(text)
        logger.debug(think)
        return result
        
    except Exception as e:
        return f"error : {str(e)}"


if __name__ == "__main__":
    prompt = 'tell me a joke'
    res = get_response_from_llm(prompt)
    print(res)