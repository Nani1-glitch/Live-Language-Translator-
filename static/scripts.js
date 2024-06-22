document.getElementById('translate-button').addEventListener('click', function () {
    const sourceLang = document.getElementById('source-language').value;
    const targetLang = document.getElementById('target-language').value;
    const audioInput = document.getElementById('audio-input').files[0];

    if (!audioInput) {
        alert('Please upload an audio file.');
        return;
    }

    const formData = new FormData();
    formData.append('source_lang', sourceLang);
    formData.append('target_lang', targetLang);
    formData.append('audio', audioInput);

    showPopup('Processing...');

    fetch('/translate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hidePopup();
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            document.getElementById('recognized-text').innerText = data.recognized_text;
            document.getElementById('translated-text').innerText = data.translated_text;
            document.getElementById('translated-audio').src = data.audio_url;
        }
    })
    .catch(error => {
        hidePopup();
        alert('Error: ' + error.message);
    });
});

document.getElementById('listen-button').addEventListener('click', function () {
    const sourceLang = document.getElementById('source-language').value;
    const targetLang = document.getElementById('target-language').value;

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Your browser does not support audio recording.');
        return;
    }

    showPopup('Listening...');

    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        const audioChunks = [];
        mediaRecorder.ondataavailable = function (event) {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = function () {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('source_lang', sourceLang);
            formData.append('target_lang', targetLang);
            formData.append('audio', audioBlob);

            fetch('/live_translate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                hidePopup();
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    document.getElementById('recognized-text').innerText = data.recognized_text;
                    document.getElementById('translated-text').innerText = data.translated_text;
                    document.getElementById('translated-audio').src = data.audio_url;
                }
            })
            .catch(error => {
                hidePopup();
                alert('Error: ' + error.message);
            });
        };

        setTimeout(() => {
            mediaRecorder.stop();
        }, 5000); // Stop recording after 5 seconds
    })
    .catch(error => {
        hidePopup();
        alert('Error accessing microphone: ' + error.message);
    });
});

function showPopup(message) {
    const popup = document.getElementById('popup');
    popup.innerText = message;
    popup.style.display = 'block';
}

function hidePopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'none';
}
