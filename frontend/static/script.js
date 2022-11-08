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
