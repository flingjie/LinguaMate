import requests
import base64
import io
from PIL import Image
import time
import os
from log import logger
from config.dev import IMAGE_OUTPUT_DIR
def generate_image(word, prompt, negative_prompt="watermark, ugly, mutation, lowres, low quality, extra limbs, text, signature, artist name, bad anatomy, poorly drawn, malformed, deformed, blurry, out of focus, noise, dust", 
                   steps=20, width=512, height=512):
    """
    调用Stable Diffusion WebUI的API生成图片
    
    参数:
        prompt (str): 正向提示词
        negative_prompt (str): 负向提示词
        steps (int): 推理步数
        width (int): 图片宽度
        height (int): 图片高度
    
    返回:
        PIL.Image: 生成的图片对象
    """
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "width": width,
        "height": height,
    }
    filepath = ''

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析返回的base64图片数据
        image_data = response.json()['images'][0]
        image_bytes = base64.b64decode(image_data)
        
        # 转换为PIL图片对象
        image = Image.open(io.BytesIO(image_bytes))
        
        # 保存图片到OUTPUT_DIR目录
        os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)  # 确保输出目录存在
        filepath = os.path.join(IMAGE_OUTPUT_DIR, f"{word}.png")
        image.save(filepath)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API请求失败: {str(e)}")
    except Exception as e:
        logger.error(f"处理图片时出错: {str(e)}")
    return filepath

if __name__ == "__main__":
    prompt = "A man trapped in a never-ending cycle of offices, computers, and paperwork, his freedom restricted by the four walls of his cubicle."
    filepath = generate_image(prompt)
    print(filepath)
