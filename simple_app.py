from speech_to_text.transcribe import transcribe_audio
from recording.record import record
from summarization.summarize import get_summary

if __name__ == "__main__":
    recording = record(duration=30)
    transcription = transcribe_audio(recording)
    print(transcription)
    summary = get_summary(transcription)
    print(summary)
