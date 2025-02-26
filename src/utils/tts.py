import os
import torch
import torchaudio
import numpy as np
import ChatTTS   
import os
from datetime import datetime  
import soundfile as sf
from log import logger

OUTPUT_DIR = "../output/audio"
chat = ChatTTS.Chat()
chat.load(compile=False)  

def text2audio(texts):
    wavs = chat.infer(texts)
    try:
        wav_data = np.array(wavs[0])
        save_file = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".opus"
        wav_save_path = os.path.join(OUTPUT_DIR, save_file)
        
        # First save as WAV temporarily
        temp_wav = "temp.wav"
        sf.write(temp_wav, wav_data, samplerate=24000)
        
        # Get duration from the WAV file
        audio_info = sf.info(temp_wav)
        logger.debug(f'audio_info: {audio_info}')
        duration = int(audio_info.duration * 1000)  # Convert seconds to milliseconds
        
        # Convert to opus using ffmpeg
        os.system(f'ffmpeg -i {temp_wav} -c:a libopus {wav_save_path}')
        
        # Remove temporary WAV file
        os.remove(temp_wav)
        
    except Exception as e:
        logger.exception(e)
        return None, 0
        
    return wav_save_path, duration


if __name__ == "__main__":
    texts = ["Yeah, I know the feeling. Any plans for the weekend?"]
    filepath, duration = text2audio(texts)
    print(filepath)
    print(f"Duration: {duration} milliseconds")