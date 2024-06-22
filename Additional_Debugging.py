import pyttsx3

try:
    engine = pyttsx3.init(driverName='nsss')
    engine.say("Hello, world!")
    engine.runAndWait()
    print("pyttsx3 with nsss driver is working correctly.")
except Exception as e:
    print(f"Error initializing pyttsx3 with nsss driver: {e}")
