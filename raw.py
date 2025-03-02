'''📂 **Project Structure:**

```
healthcare_translation_app/
├── static/
│   └── script.js
├── templates/
│   └── index.html
├── app.py
└── requirements.txt
```

📜 **app.py (Flask Backend):**

```python
from flask import Flask, request, jsonify, render_template
import openai
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = "your-openai-api-key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language', 'es')

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Translate this to {target_language}: {text}",
            max_tokens=100
        )
        translation = response['choices'][0]['text'].strip()
        return jsonify({"translation": translation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/speak', methods=['POST'])
def speak_text():
    data = request.json
    text = data.get('text')

    try:
        tts = gTTS(text)
        tts.save("static/output.mp3")
        return jsonify({"audio_url": "/static/output.mp3"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

🖼️ **index.html (Frontend):**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Healthcare Translator</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container py-5">
    <h1 class="mb-4">Healthcare Translation App</h1>

    <textarea id="inputText" class="form-control mb-3" rows="3" placeholder="Enter text or speak..."></textarea>
    
    <button class="btn btn-primary me-2" onclick="startSpeechRecognition()">🎙️ Speak</button>
    <button class="btn btn-success" onclick="translateText()">🔄 Translate</button>

    <h2 class="mt-4">Translation:</h2>
    <textarea id="translatedText" class="form-control" rows="3" readonly></textarea>
    
    <button class="btn btn-info mt-3" onclick="playAudio()">🔊 Play Translation</button>

    <audio id="audioPlayer" class="mt-3" controls></audio>

    <script src="/static/script.js"></script>
</body>
</html>
```

📜 **script.js (Frontend Logic):**

```javascript
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
```

📂 **requirements.txt:**
```
Flask
openai
SpeechRecognition
gTTS
```

🚀 **Run the Project:**
```bash
pip install -r requirements.txt
flask run
```

Then open `http://127.0.0.1:5000` in your browser! 🎉

Would you like me to guide you through deployment or add error handling? Let me know! 🚀
'''