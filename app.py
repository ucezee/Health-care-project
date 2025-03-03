from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import speech_recognition as sr
import base64
import requests
from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

audio_buffer = b''
audio_bytes = b''
recognizer = sr.Recognizer()

"""def decode_audio(audio_data):
    audio_bytes = base64.b64decode(audio_data.split(',')[1])
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
    return audio
"""

def decode_audio(audio_data):
    global audio_buffer
    global audio_bytes
    try:
        # Combine audio chunks
        audio_bytes = base64.b64decode(audio_data.split(',')[1])
        audio_buffer += audio_bytes

        # Only process if the buffer is large enough
        if len(audio_buffer) > 4000:  
            audio = AudioSegment.from_file(io.BytesIO(audio_buffer), format="webm")
            audio_buffer = b''  # Clear buffer after successful decode
            audio_bytes = b''
            return audio
    except Exception as e:
        print(f"Audio decoding error: {e}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio_chunk')
def handle_audio_chunk(data):
    try:
        file = "static/temp.wav"
        print("decoading...")
        audio = decode_audio(data)
        audio.export(file, format="wav")
        print("decoaded...")
        
        with sr.AudioFile(file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            
            socketio.emit('transcription', {'text': text})
            print(text)
    except Exception as e:
        socketio.emit('transcription', {'text': f"Error: {str(e)}"})

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language', 'es')

    try:
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": f"en|{target_language}"}
        )
        translation = response.json()['responseData']['translatedText']
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
    socketio.run(app, debug=True)
