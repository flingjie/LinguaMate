def split_think_content(text: str) -> tuple[str, str]:
    """
    Split text into think content and remaining content.
    
    Args:
        text (str): Input text containing <think>...</think> tags
        
    Returns:
        tuple[str, str]: A tuple containing (think_content, remaining_content)
        where think_content is the text between <think> tags (without tags)
        and remaining_content is everything else
    """
    think_start = text.find("<think>")
    think_end = text.find("</think>")
    
    if think_start == -1 or think_end == -1:
        return "", text
        
    think_content = text[think_start + 7:think_end].strip()
    remaining_content = (text[:think_start].strip() + " " + 
                        text[think_end + 8:].strip()).strip()
    
    return think_content, remaining_content



