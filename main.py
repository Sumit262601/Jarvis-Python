import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary as musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = 'NEWS_API_KEY'

def speak(text):
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    
    client = OpenAI(
        api_key="OPENAI_API_KEY",
    )
    
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud."},
        {"role": "user", "content": command}
      ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkdein" in c.lower():
        webbrowser.open("https://linkdein.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for articles in articles:
                speak(articles['title'])

    else:
        # Let OpenAi handle the request
        output = aiProcess(c)
        speak(output)
        # pass


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for the wake word "Jarvis"
        r = sr.Recognizer()

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listening for command
                with sr.Microphone() as source:
                    print("Jarvis ACtive...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
