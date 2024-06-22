from googletrans import Translator

def translate_text(text, dest_language='en'):
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    return translated.text

recognized_text = "Hola, ¿cómo estás?"
translated_text = translate_text(recognized_text, 'en')
print(f"Translated: {translated_text}")
