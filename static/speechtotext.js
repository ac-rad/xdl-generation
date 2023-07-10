const s2t_button = document.getElementById("speech_to_text");
const textarea = document.getElementById("input_field");

function SpeechToText() {
    s2t_button.addEventListener("click", {once: true}, (e) => {
        e.preventDefault();
        s2t_button.firstElementChild.style = "filter: invert(75%) sepia(17%) saturate(7001%) hue-rotate(297deg) brightness(102%) contrast(101%);"
        const recognition = new webkitSpeechRecognition();

        s2t_button.addEventListener("click", {once: true}, (e) => {
            s2t_button.firstElementChild.style = "none";
            recognition.stop();
            return SpeechToText();
        });

        recognition.onresult = function(event) {
            s2t_button.firstElementChild.style = "none";
            const transcript = event.results[event.results.length - 1][0].transcript.trim();
            textarea.value += transcript;
        };

        recognition.onend = (event) => {
            s2t_button.firstElementChild.style = "none";
        }

        recognition.start();
    });
}

SpeechToText();