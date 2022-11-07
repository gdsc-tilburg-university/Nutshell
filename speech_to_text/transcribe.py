import whisper
import warnings


def transcribe_audio(audiofile: str) -> str:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = whisper.load_model("small")
        result = model.transcribe(audiofile)
    print("Transcription complete\n")
    return result["text"]
