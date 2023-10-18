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

async function saveText() {
    const text = document.getElementById('textToSave').value;
    const filename = document.getElementById('filename').value;
    const response = await fetch(`/api/hashing/save_text`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: text,
            filename: filename
        })
    });
    const data = await response.json();
    document.getElementById('saveTextResponse').innerText = data[0]['Сообщение: '];
}

async function computeFileHash() {

    var filepath = document.getElementById("file-browse").value;
    console.log(filepath)
    const response = await fetch(`/api/hashing/?filepath=${filepath}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    // const data = await response.json();
    // document.getElementById('hashes').innerText = JSON.stringify(data, null, 2);
}
