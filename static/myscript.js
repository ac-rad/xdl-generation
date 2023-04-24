const textarea = document.getElementById('input_field');
const outputcontainer = document.getElementById('output_container_pre');
const translateButton = document.querySelector('input[name="submit_button"]');
let userId = localStorage.getItem('userId');
let isCreatingTextArea = false;
let apiKeyTextarea = null;
let submitButton = null;

textarea.addEventListener('input', () => {
  const oldHeight = outputcontainer.clientHeight;
  textarea.style.height = 'auto';
  textarea.style.height = `${textarea.scrollHeight}px`;

  outputcontainer.style.height = 'auto';
  outputcontainer.style.height = `${textarea.scrollHeight - 10}px`;

  const newHeight = outputcontainer.clientHeight;
  if (newHeight < oldHeight) {
    outputcontainer.style.height = `${newHeight}px`;
  }
});

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