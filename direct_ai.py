"""
This code is the base of the main app
It simply takes your api key and URL
Queries the AI model
Gets the data and converts it into a usable .wav file format
"""



import requests
import numpy as np
import ffmpeg
from io import BytesIO

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def audio_write(file_name, audio_data, sample_rate):
    """
    Save the audio to a file and apply loudness compression using ffmpeg.
    Ensure the file has a .wav extension.
    """
    if not file_name.endswith('.wav'):
        file_name += '.wav'  
    input_stream = BytesIO(audio_data)
    
    ffmpeg.input('pipe:0').output(file_name, format='wav', acodec='pcm_s16le', ar=str(sample_rate)).run(input=input_stream.read())
    print(f"Audio saved as {file_name}")

def convert_audio_to_numpy(audio_bytes, sample_rate):
    """
    Convert the audio bytes to a NumPy array after decoding with ffmpeg.
    """
    out, _ = (
        ffmpeg
        .input('pipe:0')
        .output('pipe:1', format='wav', acodec='pcm_s16le', ar=str(sample_rate))
        .run(input=audio_bytes, capture_stdout=True, capture_stderr=True)
    )
    
    audio_data = np.frombuffer(out, dtype=np.int16)
    return audio_data

audio_bytes = query({
    "inputs": "Create an intro music track for a podcast about artificial intelligence. Use a modern and polished sound with a blend of digital synths, soft electronic beats, and lo-fi elements like vinyl crackles and mellow piano chords. The melody should evoke curiosity and innovation, with a relaxed and chill vibe. Incorporate subtle robotic voice effects or glitchy sound accents for an AI-inspired touch, keeping them minimal and seamless. Tone down the bass slightly to maintain clarity and a smooth, laid-back mix. End with a soft fade-out or a dreamy resolution to transition smoothly into the podcast.",
})

sample_rate = 22050  
audio_data = convert_audio_to_numpy(audio_bytes, sample_rate)

audio_write('output', audio_bytes, sample_rate)
