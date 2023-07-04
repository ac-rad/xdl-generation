const socketio = io();

const messages = document.getElementById("messages");

convertHTMLString = (msg) => {
    for (char=0; char<msg.length; char++) {
        if (msg[char] == "<") {
            msg = msg.slice(0, char) + "&lt;" + msg.slice(char+1);
        } else if (msg[char] == ">") {
            msg = msg.slice(0, char) + "&gt;" + msg.slice(char+1);
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
    <br>
    `;
    messages.innerHTML += content;
};

createXDLMessage = (msg) => {
    const content = `
    <div class="text">
        <pre style="font-size: 0.7rem;">
            ${convertHTMLString(msg)}
        </pre>
    </div>
    <br>`;
    messages.innerHTML += content;
};

createCorrectXDLMessage = (msg) => {
    document.getElementById("output_xdl").innerHTML = convertHTMLString(msg);
};

socketio.on("message", (msg) => {
    createMessage(msg);
});

socketio.on("message_xdl", (msg) => {
    createXDLMessage(msg);
});

socketio.on("correct_xdl", (msg) => {
    createCorrectXDLMessage(msg);
});