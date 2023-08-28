const socketio = io();

socketio.on("connect", () => {
    document.getElementById("sid_input").value = socketio.id;
});

const messages = document.getElementById("messages");

convertHTMLString = (msg) => {
    for (char = 0; char < msg.length; char++) {
        if (msg[char] == "<") {
            msg = msg.slice(0, char) + "&lt;" + msg.slice(char + 1);
        } else if (msg[char] == ">") {
            msg = msg.slice(0, char) + "&gt;" + msg.slice(char + 1);
        }
    }
    return msg;
}

const createMessage = (msg) => {
    const content = `
    <div class="text">
        <span style="font-size: 0.7rem;">
            ${msg}
        </span>
    </div>
    <lbr>
    `;
    messages.innerHTML += content;
};

createXDLMessage = (msg) => {
    const content = `
    <div class="text">
        <pre class="language-markup" style="background: none; font-size: 0.7rem;"><code class="language-markup">${convertHTMLString(msg)}</code></pre>
    </div>
    <lbr>`;
    messages.innerHTML += content;

    Prism.highlightAll();

};

const output_xdl = document.getElementById("output_xdl")

createCorrectXDLMessage = (msg) => {
    output_xdl.innerHTML = convertHTMLString(msg);
    Prism.highlightAll();
};

socketio.on("message", (msg) => {
    console.log("message " + msg);
    createMessage(msg);
});

socketio.on("message_xdl", (msg) => {
    console.log("message_xdl" + msg);
    createXDLMessage(msg);
});

const tab = document.getElementById("defaultOpen");

socketio.on("correct_xdl", (msg) => {
    console.log("correct_xdl " + msg);
    createCorrectXDLMessage(msg);
    tab.click();
    if (button.value != "Translate") {
        button.value = "Translate";
        button.disabled = false;
    }
});
