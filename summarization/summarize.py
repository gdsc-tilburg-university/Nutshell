from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def get_summary(text: str) -> str:
    if not text or len(text.split()) < 5:
        return ''
    max_length = int(len(text.split())/2.5)
    min_length = int(len(text.split())/5)
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
