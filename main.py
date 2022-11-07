from speech_to_text.transcribe import transcribe_audio
from speech_to_text.record import record

if __name__ == "__main__":
    transcription = transcribe_audio(record())
    print(transcription)
