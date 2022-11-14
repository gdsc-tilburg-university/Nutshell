import whisper


def transcribe_audio(audiofile: str) -> str:
    model = whisper.load_model("small")
    result = model.transcribe(audiofile)
    
    print("Transcription complete\n")
    return result["text"]
