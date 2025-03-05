// static/script.js
const socket = io.connect('http://localhost:5000');

let mediaRecorder;
let audioChunks = [];

/*function startSpeechRecognition() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        
        
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        mediaRecorder.ondataavailable = event => {
            console.log('Audio chunk available:', event.data);
            if (event.data.size > 0) {
                const reader = new FileReader();
                reader.readAsDataURL(event.data);
                reader.onloadend = () => {
                    console.log('Sending audio chunk to server...');
                    socket.emit('audio_chunk', reader.result);
                };
            }
        };
    
        mediaRecorder.start(10000); // Send chunks every 500ms
        
        

        socket.on('transcription', data => {
            document.getElementById('inputText').value = data.text;
        });
    }).catch(err => {
        console.error('Error accessing microphone:', err);
    });
    
}*/

/*-----------------------------------------*/



function startSpeechRecognition() {
    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    recognition.start();
    

    var finaltranscript = '';

    recognition.onresult = function(event) {
        var intertranscript = '';
        
        for (var i = event.resultIndex ; i < event.results.length; i++){
            var transcript = event.results[i][0].transcript;
            
            if(event.results[i].isFinal){
                finaltranscript += transcript + " "
            }else{
                intertranscript += transcript
            }
            //var result = finaltranscript + intertranscript
            document.getElementById('inputText').innerHTML = finaltranscript + " " + '<span style="color:#999">' + intertranscript + '</span>';
        }
        

    };
}
    
    

function translateText() {
    const text = document.getElementById('inputText').innerText;
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