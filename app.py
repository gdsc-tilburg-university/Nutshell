from frontend.main import renderGUI
from summarization.service import SummaryService, testSummaryService
from queue import Queue


if __name__ == "__main__":
    renderGUI()

    transcribedTextQueue = Queue()
    transcribedTextQueue.join()

    summaryService = SummaryService(transcribedTextQueue)
    summaryService.start()

    testSummaryService(transcribedTextQueue)
    summaryService.join()
