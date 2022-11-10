function getSummarizedText() {
  url = "/summarized_text";
  axios
    .get(url)
    .then(function (response) {
      summaryContainer = document.getElementById("summaryContainer");
      summaryContainer.innerHTML = "";
      response.data.forEach((summaryBlock) => {
        const p = document.createElement("p");
        p.textContent = summaryBlock;
        summaryContainer.appendChild(p);
      });
    })
    .catch(console.error);
}

// This calls the function getSummarizedText() every 2 seconds
var intervalID = window.setInterval(getSummarizedText, 2000);

function getTranscribedText() {
  url = "/transcribed_text";
  axios
    .get(url)
    .then(function (response) {
      transcriptionContainer = document.getElementById("transcriptionContainer");
      transcriptionContainer.innerHTML = "";
      response.data.forEach((transcriptionBlock) => {
        const p = document.createElement("p");
        p.textContent = transcriptionBlock;
        transcriptionContainer.appendChild(p);
      });
    })
    .catch(console.error);
}

var intervalID2 = window.setInterval(getTranscribedText, 2000);
