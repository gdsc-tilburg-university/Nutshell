function getContent() {
  summarySelected = Boolean(summaryButton.getAttribute("selected") === "true");
  console.log("Summary?: ", summarySelected);
  url = summarySelected ? "/summarized_text" : "/transcribed_text";
  axios
    .get(url)
    .then(function (response) {
      contentContainer = document.getElementById("content");
      contentContainer.innerHTML = "";
      response.data.forEach((paragraph) => {
        const p = document.createElement("p");
        p.textContent = paragraph;
        contentContainer.appendChild(p);
      });
    })
    .catch(console.error);
}

var transcriptionButton = document.getElementById("transcriptionButton");
var summaryButton = document.getElementById("summaryButton");
var recordButton = document.getElementById("recordButton");
var waveAnimation = document.getElementById("wave");

// initialize
transcriptionButton.setAttribute("selected", "true");
getContent();
var updater = window.setInterval(getContent, 2000);
waveAnimation.setAttribute("recording", "true");

transcriptionButton.addEventListener("click", function () {
  transcriptionButton.setAttribute("selected", "true");
  summaryButton.setAttribute("selected", "false");
  // clearInterval(updater);
  getContent();
  updater = window.setInterval(getContent, 2000);
});

summaryButton.addEventListener("click", function () {
  summaryButton.setAttribute("selected", "true");
  transcriptionButton.setAttribute("selected", "false");
  // clearInterval(updater);
  getContent();
  updater = window.setInterval(getContent, 2000);
});

recordButton.addEventListener("click", function () {
  if (updater) {
    waveAnimation.setAttribute("recording", "false");
    clearInterval(updater);
    updater = undefined;
  } else {
    waveAnimation.setAttribute("recording", "true");
    getContent();
    updater = window.setInterval(getContent, 2000);
  }
});
