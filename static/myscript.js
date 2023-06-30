<<<<<<< HEAD
let userId = localStorage.getItem('userId');
let isCreatingTextArea = false;
let apiKeyTextarea = null;
let submitButton = null;

if (!userId) {
  userId = Math.floor(Math.random() * 1000000000000000000000000);
  localStorage.setItem('userId', userId);

  const expires = new Date();
  expires.setFullYear(expires.getFullYear() + 1);
  document.cookie = "userId=" + userId + ";expires=" + expires.toUTCString() + ";path=/";
}

console.log("User ID: " + userId);

function createTextArea() {
  const plus_button = document.getElementById("plus-button");
  if (plus_button.getAttribute("class") != null) {
    plus_button.removeAttribute("class", "rotated");
  } else {
    plus_button.setAttribute("class", "rotated");
  }

  if (isCreatingTextArea) {
    const container = document.getElementById("content");
    container.removeChild(apiKeyTextarea);
    container.removeChild(submitButton);

    isCreatingTextArea = false;
    return;
  }

  isCreatingTextArea = true;

  if (!apiKeyTextarea) {
    apiKeyTextarea = document.createElement("textarea");
    apiKeyTextarea.setAttribute("id", "api-key-textarea");
    apiKeyTextarea.setAttribute("name", "api-key-textarea");
    apiKeyTextarea.setAttribute("value", "api-key-textarea");
    apiKeyTextarea.setAttribute("placeholder", "Enter API key");
  }

  if (!submitButton) {
    submitButton = document.createElement("button");
    submitButton.setAttribute("id", "save-api-key");
    submitButton.setAttribute("name", "submit_button");
    submitButton.setAttribute("value", "Save API Key");
    submitButton.innerHTML = "Save API key";
    submitButton.onclick = function() {
      alert("Textarea content: " + apiKeyTextarea.value);
      fetch('/send-string', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });

      const container = document.getElementById("content");
      container.removeChild(apiKeyTextarea);
      container.removeChild(submitButton);

      apiKeyTextarea = null;
      submitButton = null;
      isCreatingTextArea = false;
    };
  }

  const container = document.getElementById("content");
  container.appendChild(apiKeyTextarea);
  container.appendChild(submitButton);
}

function confirmReagents(alert_message) {
  const confirmed = confirm(alert_message);
}

=======
>>>>>>> 956871d6df986011866afb467bdf7ba253e6595a
async function getConfig() {
  try {
    const response = await fetch('static/config.json');
    const data = await response.json();
    const openai_api_key = data["OPENAI_API_KEY"];
    if (openai_api_key == "") {
      alert("Set up your OpenAI API key in config.json");
    }
  } catch (error) {
    console.error('Error with config.json:', error);
  }
}

getConfig();

const button = document.getElementById("submit_button");
button.addEventListener("click", (event) => {
  button.value = "Loading...";
});



function copyClipboard() {
  const copyText = document.getElementsByTagName("code")[0].innerText;
  navigator.clipboard.writeText(copyText);
}
