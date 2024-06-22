from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
import os
import uuid

app = Flask(__name__)
recognizer = sr.Recognizer()
translator = Translator()

LANGUAGES = {
    'English': 'en',
    'Hindi': 'hi',
    'Telugu': 'te',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh-cn',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Urdu': 'ur',
    'Italian': 'it',
    'Russian': 'ru',
    'Portuguese': 'pt',
    'Arabic': 'ar',
    'Bengali': 'bn',
    'Punjabi': 'pa',
    'Turkish': 'tr',
    'Vietnamese': 'vi',
    'Thai': 'th',
    'Swahili': 'sw'
}

def process_audio_file(audio_path, source_lang, target_lang):
    audio = AudioSegment.from_file(audio_path)
    chunks = []
    chunk_length_ms = 30000  # 30 seconds
    for i in range(0, len(audio), chunk_length_ms):
        chunks.append(audio[i:i + chunk_length_ms])
    
    recognized_text = []
    for chunk in chunks:
        chunk_path = f"temp_audio_{uuid.uuid4().hex}.wav"
        chunk.export(chunk_path, format="wav")
        with sr.AudioFile(chunk_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language=source_lang)
                recognized_text.append(text)
            except sr.UnknownValueError:
                recognized_text.append("")
            except sr.RequestError as e:
                recognized_text.append(f"[Error: {e}]")
            os.remove(chunk_path)
    
    full_recognized_text = " ".join(recognized_text)
    translated_text = translator.translate(full_recognized_text, dest=target_lang).text

    tts = gTTS(text=translated_text, lang=target_lang)
    audio_output_path = f"static/{uuid.uuid4().hex}.mp3"
    tts.save(audio_output_path)

    return full_recognized_text, translated_text, audio_output_path

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        source_lang = request.form['source_lang']
        target_lang = request.form['target_lang']
        audio_file = request.files['audio']

        audio_path = f"temp_audio_{uuid.uuid4().hex}.mp3"
        audio_file.save(audio_path)

        recognized_text, translated_text, audio_output_path = process_audio_file(audio_path, source_lang, target_lang)

        os.remove(audio_path)
        return jsonify({
            'recognized_text': recognized_text,
            'translated_text': translated_text,
            'audio_url': audio_output_path
        })
    except sr.RequestError as e:
        return jsonify({'error': f"API request error: {e}"})
    except sr.UnknownValueError:
        return jsonify({'error': "Unable to recognize speech"})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/live_translate', methods=['POST'])
def live_translate():
    try:
        source_lang = request.form['source_lang']
        target_lang = request.form['target_lang']
        
        audio_file = request.files['audio']

        audio_path = f"temp_audio_{uuid.uuid4().hex}.webm"
        audio_file.save(audio_path)

        # Convert WebM to WAV
        wav_audio_path = f"temp_audio_{uuid.uuid4().hex}.wav"
        AudioSegment.from_file(audio_path).export(wav_audio_path, format="wav")

        recognized_text, translated_text, audio_output_path = process_audio_file(wav_audio_path, source_lang, target_lang)

        os.remove(audio_path)
        os.remove(wav_audio_path)
        return jsonify({
            'recognized_text': recognized_text,
            'translated_text': translated_text,
            'audio_url': audio_output_path
        })
    except sr.RequestError as e:
        return jsonify({'error': f"API request error: {e}"})
    except sr.UnknownValueError:
        return jsonify({'error': "Unable to recognize speech"})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
