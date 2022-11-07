import os
import requests
from dotenv import load_dotenv
load_dotenv()
api_token = os.environ["hf_api_token"]
# You're going to need to create a file named ".env" in the root directory. Then, add the line: hf_api_token=hf_XXXXXXXXXXX (where hf_XXXXX is your huggingface access token)


def query(payload, model_id):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


if __name__ == "__main__":
    testArticle = "One of the main advantages of the philosophical approach is that it allows us to ask much broader questions than those of other disciplines. A cognitive psychologist studying memory for nouns might wonder why concrete nouns are recalled better than abstract ones. This psychologist is constrained into formulating specific questions and hypotheses by the narrow focus of the research. This very focus, of course, is an advantage since it allows the researcher to scientifically examine and understand a natural phenomenon in depth. A philosopher examining the results of this same research is free to inquire about the nature of concreteness or what it means that something is abstract. He or she could also inquire as to how concrete or abstract stimuli are processed in other cognitive systems, such as attention and language. Of course, he or she is free to ask even more fundamental questions, such as, Why do we have memory? What purpose does memory serve? What would a person be like without a memory? Philosophy thus shows us the “bigger picture.” It gives us key insights into the relationships between different areas of study—within and between disciplines—and, therefore, plays a very important role in the interdisciplinary endeavor of cognitive science."
    model_id = "facebook/bart-large-cnn"
    data = query(testArticle, model_id)
    print(data)
