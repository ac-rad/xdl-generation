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
  // event.preventDefault();
  button.value = "Loading...";
});
