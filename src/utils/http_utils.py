import requests
from typing import Optional
import html2text


def fetch_url_content(url: str) -> Optional[str]:
    """
    发送GET请求获取指定URL的内容
    
    Args:
        url (str): 要请求的URL地址
        
    Returns:
        Optional[str]: 如果请求成功返回响应内容，失败返回None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果响应状态码不是200，将引发异常
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_tables = True
        h.ignore_links = True
        return h.handle(response.text)
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None 