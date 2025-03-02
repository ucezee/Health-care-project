from flask import Flask, request, jsonify, render_template
import openai
from openai import OpenAI
import speech_recognition as sr
from gtts import gTTS
import os
import requests

app = Flask(__name__)

# Replace with your OpenAI API key
#openai.api_key = "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"
#client = OpenAI(api_key="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")

@app.route('/')
def index():
    return render_template('index.html')

'''@app.route('/translate', methods=['POST'])
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
'''

'''@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language', 'es')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        print(f"Translating: {text} to {target_language}")

        response = client.chat.completions.create(
            model="gpt-4.5-preview",
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ]
            #prompt=f"Translate this to {target_language}: {text}",
            #max_tokens=100
        )
        
        translation = response['choices'][0]['text'].strip()
        return jsonify({"translation": translation})
    except Exception as e:
        print(f"Translation error: {e}")
        return jsonify({"error": str(e)}), 500
'''

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
    app.run(debug=True)
