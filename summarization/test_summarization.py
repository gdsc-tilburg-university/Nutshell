from queue import Queue
from time import sleep

from summarization.service import SummaryService


def testSummaryService(transcribedTextQueue: Queue):
    testArticle1 = "One of the main advantages of the philosophical approach is that it allows us to ask much broader questions than those of other disciplines. A cognitive psychologist studying memory for nouns might wonder why concrete nouns are recalled better than abstract ones. This psychologist is constrained into formulating specific questions and hypotheses by the narrow focus of the research. This very focus, of course, is an advantage since it allows the researcher to scientifically examine and understand a natural phenomenon in depth. A philosopher examining the results of this same research is free to inquire about the nature of concreteness or what it means that something is abstract. He or she could also inquire as to how concrete or abstract stimuli are processed in other cognitive systems, such as attention and language. Of course, he or she is free to ask even more fundamental questions, such as, Why do we have memory? What purpose does memory serve? What would a person be like without a memory? Philosophy thus shows us the “bigger picture.” It gives us key insights into the relationships between different areas of study—within and between disciplines—and, therefore, plays a very important role in the interdisciplinary endeavor of cognitive science."
    testArticle2 = "We have covered a plethora of theoretical positions in this chapter. There are several reasons for this. Psychology was the first discipline to systematically apply experimentation to the study of mind. It was thus a new discipline with many followers advocating many positions. Psychologists additionally had a very difficult task in front of them, which was to try to understand things that at the time could not be easily seen or measured. This lack of precision and early reliance on nonscientific methods such as introspection may have led to an overreliance on theory. Also, as was not the case in other disciplines, there was no overarching theory or framework for psychologists to work within. It would not be until the rise of the cognitive approach and the adoption of an information processing perspective that some kind of unity would come to the field. We turn our attention to this cognitive approach in the next chapter."
    testArticle3 = "Now back to capacity. How much can be retained in semantic long-term memory? It has been proposed that we remember virtually everything we've ever experienced in our entire lives but simply have difficulty recalling it. Therefore, although information may get into long-term memory and stay there without its being lost, our inability to remember it could be due to a failure in “getting it out.” One researcher estimates that the average adult has about a billion bits of information in memory and a storage capacity that is perhaps one thousand to one million times greater than that (Landauer, 1986). However, we must be skeptical about such estimates, since the inability to recall an item in a memory test can be due to either retrieval failure or decay."

    transcribedTextQueue.put(testArticle1)
    sleep(10)
    transcribedTextQueue.put(testArticle2)
    sleep(25)
    transcribedTextQueue.put(testArticle3)


if __name__ == "__main__":
    from api_example import query
    transcribedTextQueue = Queue()
    transcribedTextQueue.join()

    summaryService = SummaryService(transcribedTextQueue)
    summaryService.start()

    testSummaryService(transcribedTextQueue)
    summaryService.join()
else:
    from .api_example import query
