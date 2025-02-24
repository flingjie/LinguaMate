from llm.chat import get_response_from_llm


def check_grammar(text):
    prompt = f"""
"""
    result = get_response_from_llm(prompt)
    return result


if __name__ == "__main__":
    text = ''
    result = check_grammar(text)
    print(result)