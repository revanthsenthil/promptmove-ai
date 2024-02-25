from  openai import OpenAI
from src.audio.MicrophoneStream import MicrophoneStream
import pyaudio
import wave

def transcribe_speech(audio_file):
    client = OpenAI()

    audio_file = open(audio_file, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )
    return transcript


def record_5_sec():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    WAVE_OUTPUT_FILENAME = "speech.wav"

    with MicrophoneStream(RATE, CHUNK) as stream:
        print("Recording...")
        audio = stream.generator()
        frames = []
        for i in range(0, int(RATE / CHUNK * 5)):
            frames.append(audio.__next__())

    print("Finished recording.")
    

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return WAVE_OUTPUT_FILENAME

if __name__ == "__main__":
    import os
    file = record_5_sec()
    transcript = transcribe_speech(file)
    os.remove(file)
    print(transcript)
