async function encrypt() {
    const text = document.getElementById('encryptText').value;
    const response = await fetch(`/api/encryption/?text=${encodeURIComponent(text)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    var values = Object.keys(data[0]).map(function(key){
        return data[0][key];
    });
    document.getElementById('encryptedText').innerHTML = "<span class='label'>Шифротекст:</span><span class='value'>" + values[0] + "</span><br>";
    document.getElementById('encryptedText').innerHTML += "<br>";
    document.getElementById('encryptedText').innerHTML += "<span class='label'>Ключ:</span><span class='value'>" + values[1] + "</span><br>";
    document.getElementById('encryptedText').innerHTML += "<span class='label'>Тег:</span><span class='value'>" + values[2] + "</span><br>";
    document.getElementById('encryptedText').innerHTML += "<span class='label'>Одноразовый код:</span><span class='value'>" + values[3] + "</span>";
}

async function decrypt() {
    const ciphertext = document.getElementById('decryptText').value;
    const key = document.getElementById('decryptKey').value;
    const tag = document.getElementById('decryptTag').value;
    const nonce = document.getElementById('decryptNonce').value;
    const response = await fetch(`/api/decryption/?ciphertext=${encodeURIComponent(ciphertext)}&key=${encodeURIComponent(key)}&tag=${encodeURIComponent(tag)}&nonce=${encodeURIComponent(nonce)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    document.getElementById('decryptedText').innerText = data[0];
}