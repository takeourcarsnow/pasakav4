from flask import Flask, render_template, request, jsonify
from google.cloud import texttospeech
import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64

load_dotenv()

app = Flask(__name__)

# Configure Google API credentials
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini
model = genai.GenerativeModel('gemini-pro')

# Initialize Text-to-Speech client
client = texttospeech.TextToSpeechClient()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-story', methods=['POST'])
def generate_story():
    data = request.json
    age = data.get('age')
    theme = data.get('theme')
    length = data.get('length')

    # Prompt for Gemini in Lithuanian
    prompt = f"""Sukurk {length} pastraipų ilgio pasaką vaikams ({age} metų amžiaus) 
                tema: {theme}. Pasaka turi būti edukacinė ir įtraukianti."""

    # Generate story using Gemini
    response = model.generate_content(prompt)
    story = response.text

    # Configure text-to-speech
    synthesis_input = texttospeech.SynthesisInput(text=story)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="lt-LT",
        name="lt-LT-Standard-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Generate audio
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Convert audio to base64
    audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')

    return jsonify({
        'story': story,
        'audio': audio_base64
    })

if __name__ == '__main__':
    app.run(debug=True)