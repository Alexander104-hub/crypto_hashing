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
    let response = await fetch(`/api/hashing/?filepath=${filepath}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(function(response){

	return response.text()
    });
    var obj = JSON.parse(response);
    var json_hashes = JSON.stringify(obj, undefined, 4);
    console.log(json_hashes)
    document.getElementById("json-hashes-text-area").value = json_hashes;
}


async function download_hashes() {
    var json = document.getElementById("json-hashes-text-area").value;
    var downloadableLink = document.createElement('a');
    downloadableLink.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(json));
    downloadableLink.download = "hashes" + ".json";
    document.body.appendChild(downloadableLink);
    downloadableLink.click();
    document.body.removeChild(downloadableLink);
}


async function computeFileDiff() {
    var path1 = document.getElementById('file-path-diff-1').value;
    var path2 = document.getElementById('file-path-diff-2').value;
    let response = await fetch(`/api/hashing/compute_diff/?path1=${path1}&path2=${path2}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(function(response){

	return response.text()
    });
    var obj = JSON.parse(response);
    var json_hashes = JSON.stringify(obj, undefined, 4);
    document.getElementById("json-hashes-diff-text-area").value = json_hashes;
}

