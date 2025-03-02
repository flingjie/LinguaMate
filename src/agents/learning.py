from llm.chat import get_response_from_llm
from utils.http_utils import fetch_url_content
from log import logger
from config import ModelName
import os
import json_repair


def generate_questions(content):
    prompt = """
    You are an experienced programmer. Your task is to generate 5 test questions based on the provided blog content.
    First, analyze the entire article to identify the core knowledge points. Then, select 5 knowledge points from these and generate test questions based on them.
    Finally, return 5 question descriptions in a JSON list. 

    ## Response Format
    [
        {
            "question": "question description",
            "knowledge_point": "knowledge point description"
        }
    ]
    
    ## Blog Content:
    """ + content

    # logger.debug(prompt)
    result = ''
    try:
        result = get_response_from_llm(prompt, model_name=ModelName.ARK_DEEPSEEKV3.value)
        result = json_repair.loads(result)
    except Exception as e:
        logger.exception(e)
    return result


def check_answer(question, knowledge_point, user_input):
    prompt = f"""
    You are a content analysis expert. Your task is to score the user's input based on the question and the knowledge point. 
    Return a value between 1 and 10, and provide a concise statement indicating which points are correct and which points need improvement.
    The statement should be from the second-person perspective.

    Question: "{question}"
    Knowledge Point: "{knowledge_point}"
    User Input: "{user_input}"
    """
    result = ''
    logger.debug(prompt)
    try:
        result = get_response_from_llm(prompt)
    except Exception as e:
        logger.exception(e)
    return result


if __name__ == "__main__":
    # content = fetch_url_content('https://www.paulgraham.com/greatwork.html')
    # questions = generate_questions(content[:2000])
    # logger.debug(questions)
    question = 'What habit should you develop to increase the likelihood of doing great work one day?'
    knowledge_point = "Develop a habit of working on your own projects. Don't let 'work' mean something other people tell you to do."
    reply = 'Do something great and exciting.'
    result = check_answer(question, knowledge_point, reply)
    logger.debug(result)