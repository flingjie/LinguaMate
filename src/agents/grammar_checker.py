from llm.chat import get_response_from_llm


def check_grammar(text):
    prompt = f"""
You are a professional English teacher. 
Your task is to judge whether there are grammatical errors in user input and whether the expression is reasonable as a fourth person. 
If there are grammatical errors or unreasonable expressions, the teacher will point out the problem and provide suggestions. 
If there are no syntax errors and the expression is correct, an empty string is returned.

## user input
{text}
"""
    print(prompt)
    result = get_response_from_llm(prompt)
    return result


if __name__ == "__main__":
    text = 'I am thinking the question you said.'
    result = check_grammar(text)
    print(result)