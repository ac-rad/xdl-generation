const resizableDiv = document.getElementById('messages_container');
let startY;
let startHeight;

resizableDiv.addEventListener('mousedown', initResize);

function initResize(e) {
  startY = e.clientY;
  startHeight = parseInt(document.defaultView.getComputedStyle(resizableDiv).height, 10);
  document.addEventListener('mousemove', resize);
  document.addEventListener('mouseup', stopResize);
}

function resize(e) {
  const newHeight = startHeight + (startY - e.clientY);
  resizableDiv.style.height =  (newHeight < window.innerHeight) ? newHeight + 'px' : '100%';
}

function stopResize() {
  document.removeEventListener('mousemove', resize);
  document.removeEventListener('mouseup', stopResize);
}
