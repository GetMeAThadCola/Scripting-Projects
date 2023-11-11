import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    sound = AudioSegment.from_mp3("output.mp3")
    play(sound)

if __name__ == "__main__":
    while True:
        command = listen().lower()

        if "exit" in command:
            print("Exiting the voice assistant.")
            break

        if command:
            response = f"You said: {command}"
            print(response)
            speak(response)
