from queue import Queue
import threading
from summarization.summarize import get_summary
from .api_example import query

summarizedTextStore = []
lock = threading.Lock()


class SummaryService(threading.Thread):
    def __init__(self, transcribedTextQueue: Queue, useApi: bool = True):
        threading.Thread.__init__(self)
        self.transcribedTextQueue = transcribedTextQueue
        self.useApi = useApi

    def run(self):
        global summarizedTextStore
        while True:
            # Get last block of transcribed text from queue
            # Queue.get() is natively blocking, i.e. this code will only run if the queue is not empty
            transcribedText = self.transcribedTextQueue.get()

            # Summarize that text
            if self.useApi:
                response = query(
                    transcribedText, model_id="facebook/bart-large-cnn")
                summaryText = response[0].get("summary_text")
            else:
                summaryText = get_summary(transcribedText)

            # Add new block of summarized text to the global summary storage
            with lock:
                summarizedTextStore.append(summaryText)

            print(f"Full Summary: {summarizedTextStore}")
            self.transcribedTextQueue.task_done()
