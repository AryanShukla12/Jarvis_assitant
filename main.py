import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi="3be239a11be74fc5a04b7a647dfb27a4"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts=gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()

    # Load your MP3 file
    pygame.mixer.music.load("temp.mp3")  # Replace with your MP3 file path

    # Play the music
    pygame.mixer.music.play()

    # Keep the program running until the music finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()

    os.remove('temp.mp3')  

def aiprocess(command):
    client=OpenAI(
    api_key="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"
    )

    completion=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are a virtual assitant named jarvis skilled in general tasks like alexa and google cloud . give short responses please"},
            {"role":"user","content":"command"}
        ]
    )

    return completion.choices[0].message.content

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musiclibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r= requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code==200:
            data = r.json()

            # Extract the articles
            articles = data.get('articles',[])

            #print the headlines
            for article in articles:
                speak(article['title'])
        
    
    else:
        output=aiprocess(c)
        speak(output)

        




if __name__ == "__main__":
    speak("Initializing Jarvis ........")
    while True:
        # Listen for the wake up word Jarvis
        #obtaion audio from the micro phone
        r=sr.Recognizer()
        print("Recognizing....")
        #recognize speech using sphinx
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio=r.listen(source,timeout=2,phrase_time_limit=1)
            word=r.recognize_google(audio)
            if (word.lower()=="jarvis"):
                speak("Ya")
                r=sr.Recognizer()
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio=r.listen(source)
                    command=r.recognize_google(audio)

                    processcommand(command)

        except Exception as e:
            print("Error; {0}".format(e))

