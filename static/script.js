function startSpeechRecognition() {
    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('inputText').value = transcript;
    };
}

function translateText() {
    const text = document.getElementById('inputText').value;
    const targetLanguage = 'es';  // Example: Spanish

    fetch('/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, target_language: targetLanguage })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('translatedText').value = data.translation;
    });
}

function playAudio() {
    const text = document.getElementById('translatedText').value;

    fetch('/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    })
    .then(response => response.json())
    .then(data => {
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.src = data.audio_url;
        audioPlayer.play();
    });
}