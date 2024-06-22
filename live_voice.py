import speech_recognition as sr
from googletrans import Translator
import tkinter as tk
from tkinter import ttk
import threading
from gtts import gTTS
from playsound import playsound
import os

# Dictionary to map language names to language codes
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
    # Add more languages as needed
}

class LiveTranslator:
    def __init__(self, root):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.translator = Translator()
        self.running = False
        self.translated_text = ""
        self.root = root
        self.root.title("Live Translation")
        
        # Language selection
        self.source_language_label = tk.Label(root, text="Select Source Language:")
        self.source_language_label.pack()
        self.source_language_var = tk.StringVar(root)
        self.source_language_menu = ttk.Combobox(root, textvariable=self.source_language_var)
        self.source_language_menu['values'] = list(LANGUAGES.keys())
        self.source_language_menu.pack()
        
        self.target_language_label = tk.Label(root, text="Select Target Language:")
        self.target_language_label.pack()
        self.target_language_var = tk.StringVar(root)
        self.target_language_menu = ttk.Combobox(root, textvariable=self.target_language_var)
        self.target_language_menu['values'] = list(LANGUAGES.keys())
        self.target_language_menu.pack()
        
        # Text display area
        self.text_widget = tk.Text(root, height=10, width=50)
        self.text_widget.pack()
        
        # Start and stop buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_translation)
        self.start_button.pack()
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_translation)
        self.stop_button.pack()
    
    def recognize_and_translate(self):
        source_language_code = LANGUAGES[self.source_language_var.get()]
        target_language_code = LANGUAGES[self.target_language_var.get()]
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.running:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    recognized_text = self.recognizer.recognize_google(audio, language=source_language_code)
                    translated_text = self.translator.translate(recognized_text, dest=target_language_code).text
                    self.update_text(translated_text)
                    self.speak_text(translated_text, target_language_code)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    self.update_text("Unable to recognize speech. Please try again.")
                except sr.RequestError:
                    self.update_text("API unavailable")
                    break

    def update_text(self, text):
        self.text_widget.insert(tk.END, text + "\n")
        self.text_widget.see(tk.END)

    def speak_text(self, text, lang):
        try:
            tts = gTTS(text=text, lang=lang)
            audio_file = "translated_audio.mp3"
            tts.save(audio_file)
            playsound(audio_file)
            os.remove(audio_file)
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")

    def start_translation(self):
        self.running = True
        self.translation_thread = threading.Thread(target=self.recognize_and_translate)
        self.translation_thread.start()

    def stop_translation(self):
        self.running = False
        if hasattr(self, 'translation_thread'):
            self.translation_thread.join()
        self.root.quit()  # Close the Tkinter window

def main():
    root = tk.Tk()
    app = LiveTranslator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
