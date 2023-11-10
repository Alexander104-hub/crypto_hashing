async function addEncryptionOutputFields(mode, values, postfix='') {
    id = 'encryptedText' + postfix
    // spans with class label and class value are needed for style.css. Alse class value is needed for copyToClipboard. DO NOT delete them
	document.getElementById(id).innerHTML += "<span class=\"label\"> Ключ: </span><span class='value'>" + values[1] + "</span><br>";
	if(mode == "EAX"){
	    document.getElementById(id).innerHTML += "<span class=\"label\"> Тег: </span><span class='value'>" + values[2] + "</span><br>";
	    document.getElementById(id).innerHTML += "<span class=\"label\"> Одноразовый код: </span><span class='value'>" + values[3] + "</span><br>";
	}
	else if(mode == "CBC"){
	    document.getElementById('encryptedText').innerHTML += "<span class=\"label\"> IV: </span><span class='value'>" + values[2] + "</span><br>";
	}
}

async function encrypt() {
    const text = document.getElementById('encryptText').value;
    const mode = document.getElementById("choose-encryption-algo").value;
    const key = document.getElementById("encryptionKey").value;
    const iv = document.getElementById("encryptionIV").value;
    const response = await fetch(`/api/encryption/?text=${encodeURIComponent(text)}&mode=${mode}&key=${key}&iv=${iv}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    if(!response.ok){
	if(response.status == 400){
	    document.getElementById('encryptedText').innerHTML = "<p>Ошибка: " + data + "</p>";
	}
    }
    else{
	    var values = Object.keys(data[0]).map(function(key){
	        return data[0][key];
	    });
	    document.getElementById('encryptedText').innerHTML = "<span class=\"label\"> Шифротекст: </span><span class='value'>" + values[0] + "</span><br>";
        addEncryptionOutputFields(mode, values);
    }
} 

async function encryptFile() {
    const fileInput = document.getElementById('encryptFile');
    const key = document.getElementById('en-file-key').value;
    const mode = document.getElementById('choose-encryption-algoFile').value;
    const iv = document.getElementById("encryptionIVFile").value;
    const file = fileInput.files[0];
    if (file.size > 100 * 1024 * 1024) {
        alert('Размер файла на шифрование превышает 100 МБ');
        return;
    }
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`/api/encryption/encrypt_file/?mode=${encodeURIComponent(mode)}&key=${encodeURIComponent(key)}`, {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    var values = Object.keys(result[0]).map(function(key){
        return result[0][key];
    });
    document.getElementById('encryptedTextFile').innerText = "";
    addEncryptionOutputFields(mode, values, 'File');
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
    const mode = document.getElementById("choose_decryption-algo").value;
    const ciphertext = document.getElementById('decryptText').value;
    const key = document.getElementById('decryptKey').value;
    const tag = document.getElementById('decryptTag').value;
    const nonce = document.getElementById('decryptNonce').value;
    const iv = document.getElementById('decryptIV').value;
    let routerPath = '';
    if (mode == 'CBC') {
        routerPath = `/api/decryption/decrypt_cbc/?ciphertext=${encodeURIComponent(ciphertext)}&key=${encodeURIComponent(key)}&iv=${encodeURIComponent(iv)}`
    } else if (mode == 'ECB') {
        routerPath = `/api/decryption/decrypt_ebc/?ciphertext=${encodeURIComponent(ciphertext)}&key=${encodeURIComponent(key)}`
    } else {
        routerPath = `/api/decryption/decrypt_eax/?ciphertext=${encodeURIComponent(ciphertext)}&key=${encodeURIComponent(key)}&tag=${encodeURIComponent(tag)}&nonce=${encodeURIComponent(nonce)}`
    }
    const response = await fetch(routerPath, {
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
    const key = document.getElementById('decryptKeyFile').value;
    const tag = document.getElementById('decryptTagFile').value;
    const nonce = document.getElementById('decryptNonceFile').value;
    const iv = document.getElementById('decryptIVFile').value;
    const mode = document.getElementById('choose_decryption-algoFile').value;
    if (!fileInput.files.length) {
        return;
    }
    
    const file = fileInput.files[0];
    if (file.size > 100 * 1024 * 1024) {
        alert('Размер файла на расшифровку превышает 100 МБ');
        return;
    }
    const filename = file.name;
    let formData = new FormData();
    formData.append("file", file);
    // async def upload_encrypted_file(mode: str, key: str, iv: str = None, tag: str = None, nonce: str = None, file: UploadFile=File(...)):
    const response = await fetch(`/api/decryption/decrypt_file/?mode=${encodeURIComponent(mode)}&key=${encodeURIComponent(key)}&iv=${encodeURIComponent(iv)}&tag=${encodeURIComponent(tag)}&nonce=${encodeURIComponent(nonce)}`, {
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
    var folders = document.getElementById("file-browse").files;
    var uploaded_files = document.getElementById("file-browse-2").files;
    var hash_algo = document.getElementById("choose-hashes-algo").value;
    const files = new FormData();
    for(let i = 0; i < folders.length; i++) {
	files.append("files", folders[i]);
    }
    for(let i = 0; i < uploaded_files.length; i++){
	files.append("files", uploaded_files[i]);
    }
    //
    let response = await fetch(`/api/hashing/?hash_algo=${hash_algo}`, {
        method: 'POST',
	body: files,
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
    var file1 = document.getElementById('file-path-diff-1').files[0];
    var file2 = document.getElementById('file-path-diff-2').files[0];
    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);
    let response = await fetch(`/api/hashing/compute_diff/`, {
        method: 'POST',
	body: formData

    }).then(function(response){
	return response.text()
    });
    let parser = new DOMParser();
    let doc = parser.parseFromString(response, 'text/html');
    // document.getElementById("json-hashes-diff-text-area").innerHTML = doc;;
    document.getElementById("hashes-textarea").innerHTML = doc.body.outerHTML;
}

async function addNewFieldOnAlgoChange(postfix=''){
    var x = document.getElementById("choose-encryption-algo" + postfix).value;
    if(x != "CBC"){
	document.getElementById("encryptionIV" + postfix).style.display = "none";
    }
    else{
	document.getElementById("encryptionIV" + postfix).style.display = "";
    }
}

async function addNewFieldOnDecryptAlgoChange(postfix=''){
    var x = document.getElementById("choose_decryption-algo" + postfix).value;
    const iv = 'decryptIV' + postfix;
    const tag = 'decryptTag' + postfix;
    const nonce = 'decryptNonce' + postfix;
    if(x == "CBC"){
	document.getElementById(iv).style.display = "";
    document.getElementById(tag).style.display = "none";
    document.getElementById(nonce).style.display = "none";
    }
    else if(x == "EAX"){
	document.getElementById(tag).style.display = "";
    document.getElementById(nonce).style.display = "";
    document.getElementById(iv).style.display = "none";
    }
    else {
        document.getElementById(iv).style.display = "none";
        document.getElementById(tag).style.display = "none";
        document.getElementById(nonce).style.display = "none";
    }
}
// https://web.dev/articles/read-files
// https://stackoverflow.com/questions/12942436/how-to-get-folder-directory-from-html-input-type-file-or-any-other-way
