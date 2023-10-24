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

async function encryptFile() {
    const fileInput = document.getElementById('encryptFile');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch('/api/encryption/encrypt_file', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    document.getElementById('encryptedFileKey').textContent = 'Ключ: ' + result[0]['Ключ: '];
    document.getElementById('encryptedFileTag').textContent = 'Тег: ' + result[0]['Тег: '];
    document.getElementById('encryptedFileNonce').textContent = 'Одноразовый код: ' + result[0]['Одноразовый код: '];
}

async function downloadEncryptedFile() {
    const filename = document.getElementById('downloadFileName').value;
    const response = await fetch('/api/encryption/download_encrypted_file/' + filename);
    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'download';
    a.click();
}

async function getFiles() {
    const input = document.getElementById('downloadFileName');
    const response = await fetch('/api/encryption/get_encrypted_files');
    const files = await response.json();

    let fileList = '';
    let count = 0;
    
    for (let file of files) {
        if (file.startsWith(input.value)) {
            fileList += '<div>' + file + '</div>';
            count++;
        }
        if (count >= 5) break;
    }

    document.getElementById('fileList').innerHTML = fileList;
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


async function decryptAndDownloadFile() {
    const fileInput = document.getElementById('decryptFile');
    const key = document.getElementById('key').value;
    const tag = document.getElementById('tag').value;
    const nonce = document.getElementById('nonce').value;
    
    if (!fileInput.files.length) {
        return;
    }
    
    const file = fileInput.files[0];
    const filename = file.name;
    let formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`/api/decryption/decrypt_file/?key=${encodeURIComponent(key)}&tag=${encodeURIComponent(tag)}&nonce=${encodeURIComponent(nonce)}`, {
        method: 'POST',
        body: formData
    });
    if (response.ok) {

        // Скачивание расшифрованного файла
        const downloadResponse = await fetch(`/api/decryption/download_decrypted_file/${filename}`);
        if (downloadResponse.ok) {
            const blob = await downloadResponse.blob();
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
        }
    }
}



async function computeFileHash() {

    var filepath = document.getElementById("file-browse").value;
    var hash_algo = document.getElementById("choose-hashes-algo").value;
    let response = await fetch(`/api/hashing/?filepath=${filepath}&hash_algo=${hash_algo}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(function(response){

	return response.text()
    });
    var obj = JSON.parse(response);
    var json_hashes = JSON.stringify(obj, undefined, 4);
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
// https://web.dev/articles/read-files
// https://stackoverflow.com/questions/12942436/how-to-get-folder-directory-from-html-input-type-file-or-any-other-way
