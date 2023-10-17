function copyToClipboard() {
    var textToCopy = document.querySelector('.value').innerText;
    var tempInput = document.createElement('input');
    tempInput.value = textToCopy;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
  }