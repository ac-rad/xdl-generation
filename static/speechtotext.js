const s2t_button = document.getElementById("speech_to_text");
const textarea = document.getElementById("input_field");
let isActive = false;
let recognition;

function activateSpeechToText() {
  isActive = true;
  s2t_button.firstElementChild.style = "filter: invert(75%) sepia(17%) saturate(7001%) hue-rotate(297deg) brightness(102%) contrast(101%);";
  recognition = new webkitSpeechRecognition();

  recognition.onresult = function(event) {
    const transcript = event.results[event.results.length - 1][0].transcript.trim();
    textarea.value += transcript;
    s2t_button.firstElementChild.style = "none";
  };
  
  recognition.start();
}

function deactivateSpeechToText() {
  isActive = false;
  s2t_button.firstElementChild.style = "none";
  recognition.stop();
}

s2t_button.addEventListener("click", function(e) {
  e.preventDefault();
  if (isActive) {
    deactivateSpeechToText();
  } else {
    activateSpeechToText();
  }
});
