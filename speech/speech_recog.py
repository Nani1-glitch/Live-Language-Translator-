import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_google(audio)
    except sr.RequestError:
        response = "API unavailable"
    except sr.UnknownValueError:
        response = "Unable to recognize speech"
    return response

recognizer = sr.Recognizer()
microphone = sr.Microphone()

print("Say something...")
recognized_text = recognize_speech_from_mic(recognizer, microphone)
print(f"Recognized: {recognized_text}")
