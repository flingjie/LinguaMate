from llm.chat import get_response_from_llm
from log import logger


def get_chat_response(dialogs, user_input):
    history = "\n".join([f'{item["role"]}:{item['content']}' for item in dialogs])
    # logger.debug(f'history: {history}')
    prompt = f"""
    You are a witty programmer. 
    Your task is to generate responses based on the programmer's role, considering user input and conversation history.
# user_input
{user_input}

# history
{history}    
"""
    return get_response_from_llm(prompt)


if __name__ == "__main__":
    history = [{
        "role": "user",
        "content": "Hey, how's it going?"
    }, {
        "role": "assistant",
        "content": "Not bad, just a bit busy with work. How about you?"
    },{
        "role": "user",
        "content": "Same here. Work has been crazy lately."
    },{
        "role": "assistant",
        "content": "Yeah, I know the feeling. Any plans for the weekend?"
    }]
    user_input = "Thinking of going for a hike. Wanna join?"
    result = get_chat_response(history, user_input)
    print(result)

