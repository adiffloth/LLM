import speech_recognition as sr


def listen_to_microphone():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)            # Capture the audio

    try:
        text = recognizer.recognize_google(audio)    # Recognize speech using Google Web Speech API
        print(f"Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from the service; {e}")
        return ""

listen_to_microphone()
