from speech_to_text.transcribe import transcribe_audio
from recording.record import record
from summarization.summarize import get_summary

if __name__ == "__main__":
    transcription = transcribe_audio(record(duration=30))
    print(transcription)
    summary = get_summary(transcription)
    print(summary)
