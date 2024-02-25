from  openai import OpenAI
from src.audio.MicrophoneStream import MicrophoneStream
import wave
import os

def transcribe_speech(audio_file):
    client = OpenAI()

    with open(audio_file, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=f, 
            response_format="text"
        )
    os.remove(audio_file)
    return transcript


def record_5_sec():
    CHUNK = 1024
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
    file = record_5_sec()
    transcript = transcribe_speech(file)
    print(transcript)
