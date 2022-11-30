from queue import Queue
import threading
from summarization.summarize import summarize

summarizedTextStore = []
summarizedTextFragment = ['']

# TODO: summarizedTextFragment should not need to be a list, a string would do.
# However changing to a different string is thread-unsafe


def get_summarized_text():
    return summarizedTextStore + [summarizedTextFragment[-1]]


class SummaryService(threading.Thread):
    def __init__(self, transcribedTextQueue: Queue, useApi: bool = True):
        threading.Thread.__init__(self)
        self.transcribedTextQueue = transcribedTextQueue
        self.useApi = useApi
        self.textBuffer = ''
        self.lock = threading.Lock()

    def run(self):
        global summarizedTextStore

        while True:
            # Get last block of transcribed text from queue
            # Queue.get() is natively blocking, i.e. this code will only run if the queue is not empty
            transcribedText: str = self.transcribedTextQueue.get()

            # ideally, summarize in blocks of max 1024 tokens
            would_exceed_max_length = len(
                self.textBuffer.split()) + len(transcribedText.split()) >= 1024

            if not would_exceed_max_length:
                self.textBuffer += transcribedText
                continue

            summaryText = summarize(self.textBuffer, self.useApi)
            self.textBuffer = ''

            with self.lock:
                summarizedTextStore.append(summaryText)

            self.transcribedTextQueue.task_done()
