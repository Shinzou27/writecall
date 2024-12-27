import threading
import pyaudio
import wave
import time
import noisereduce as nr
import numpy as np
from whispertest import analyze_text
from utils import post_audio, post_transcription
import signal
import sys

transcribed_text = []
file, text, nr_filename = (None, "", "")
counter = 1
recording = False
# Configurações do áudio
FORMAT = pyaudio.paInt16  # Tipo de formato
CHANNELS = 1  # Número de canais (mono)
RATE = 44100  # Taxa de amostragem (frequência de amostragem)
CHUNK = 1024  # Tamanho do buffer
RECORD_SECONDS = 30  # Duração da gravação (30 segundos)
OUTPUT_FILENAME_TEMPLATE = "gravacao_{}.wav"  # Nome do arquivo de saída

def handler(signum, frame):
    global recording
    print("Interrupção detectada. Finalizando gravação...")
    recording = False 

signal.signal(signal.SIGINT, handler)

def record_audio(filename):
    global file, text, nr_filename
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print(f"Gravando {filename}...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)   
        if not recording:
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print(f"Áudio gravado em {filename}")
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=RATE)
    nr_filename = "reduced_" + filename
    with wave.open(nr_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(reduced_noise_audio.tobytes())

def get_audio_data():
    return (file, text)

def do_requests():
    global file
    global counter
    text = analyze_text(nr_filename)
    transcribed_text.append(text)
    for t in transcribed_text:
        print(f"{t}\n")
    with open(nr_filename, 'rb') as file:
        audio_chunk = post_audio(file)
    if not audio_chunk:
        print("Erro ao enviar áudio.")
        stop_recording()
        return
    post_transcription(audio_chunk, text)

def record_thread():
    global recording, counter
    while recording:
        filename = OUTPUT_FILENAME_TEMPLATE.format(counter)    
        record_audio(filename)
        print("Gravando")
        api_thread = threading.Thread(target=do_requests)
        api_thread.daemon = True
        api_thread.start()
        counter += 1

def start_recording():
    global recording
    if not recording: 
        recording = True
        thread = threading.Thread(target=record_thread)
        thread.daemon = True 
        thread.start()
        print("Gravação iniciada")

def stop_recording():
    global recording
    recording = False
    print("Gravação encerrada")