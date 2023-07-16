const button = document.getElementById("submit_button");
const tab2 = document.getElementById("secondaryOpen");
if (button.value == "Translate") {
  button.addEventListener("click", (event) => {
    button.value = "Running Translation...";
    tab2.click();
    output_xdl.innerHTML = "";
  });
  
}


function copyClipboard() {
  const copyText = document.getElementsByTagName("code")[0].innerText;
  navigator.clipboard.writeText(copyText);
}


const formContainer = document.getElementById('input');
const tabContainer = document.querySelector('.tab-container');

if (window.innerWidth < 750) {
  document.getElementById("tertiaryOpen").hidden = false;

  tabContainer.insertBefore(formContainer, tabContainer.children[1]);
} else {
  formContainer.className = "";
}
