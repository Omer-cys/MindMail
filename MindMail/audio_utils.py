# audio_utils.py
import sounddevice as sd
import numpy as np
import wave
import whisper

def record_audio(filename="input.wav", duration=5, fs=44100):
    print("Recording audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    
    # Save as WAV
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())
    
    print(f"Recording saved as {filename}")
    return filename

def transcribe_audio(filename="input.wav"):
    print("Transcribing audio...")
    model = whisper.load_model("base")  # or "small" for low RAM
    result = model.transcribe(filename)
    return result["text"]
