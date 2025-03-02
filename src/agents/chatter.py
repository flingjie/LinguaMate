from llm.chat import get_response_from_llm
from log import logger


def get_chat_response(user_input, dialogs):
    history = "\n".join([f'{item["role"]}:{item['content']}' for item in dialogs])
    # logger.debug(f'history: {history}')
    prompt = f"""
   You are an advanced English conversation assistant, designed to help users improve their spoken and written English naturally. 
   Your role is to engage in interactive conversations, provide grammar corrections, suggest better phrasing, and offer explanations when needed.  

    ### Instructions:  
    - Keep responses engaging, friendly, and contextually relevant.  
    - Suggest alternative expressions to improve fluency.  
    - Encourage users to elaborate on their responses to enhance conversation skills.  
    - Adapt to the user’s proficiency level (beginner, intermediate, advanced) and provide appropriate feedback.  
    - Keep responses concise, and ensure they do not exceed 200 characters.  

    Your task is to generate responses based on the user's input and conversation history.

    ### user_input
    {user_input}

    ### history
    {history}    
"""
    return get_response_from_llm(prompt)


if __name__ == "__main__":
    history = []
    user_input = "I’ve started working on a new side project—an AI-powered English learning assistant!"
    result = get_chat_response(user_input, history)
    print(result)

