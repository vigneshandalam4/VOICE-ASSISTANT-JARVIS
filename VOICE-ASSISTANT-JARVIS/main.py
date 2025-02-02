import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from groq import Groq
from gtts import gTTS
import pygame
import os

recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi="a5e9a58599a24f40a578f3a21f8a19be"

#microsoft text to speech
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the script running while the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    #removing the mp3 file after every usage
    os.remove("temp.mp3")


def aiProcess(command):
    client = Groq(api_key="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")
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system","content": "you are a virtual assitant named jarvis skilled in general tasks like alexa,please give short responses",},
            {"role":"user","content":command}
        ],
        model="llama3-8b-8192",
    )
    return (chat_completion.choices[0].message.content)



def processCommand(c):
    print(c)
    if("open google" in c.lower()):
        speak("opening google")
        webbrowser.open("https://google.com")
    elif("open facebook" in c.lower()):
        speak("opening facebook")
        webbrowser.open("http://facebook.com")
    elif("open youtube" in c.lower()):
        speak("opening youtube")
        webbrowser.open("https://youtube.com")
    elif("open linkedin" in c.lower()):
        webbrowser.open("https://linkedin.com")
    elif(c.lower().startswith("play")):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)
    elif("news" in c.lower()):
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if (r.status_code==200):
            #parse the JSON response
            data=r.json()

            #Extract the articles
            articles=data.get('articles',[])

            #print the headlines
            for article in articles:
                speak(article['title'])
        else:
            speak("Sorry, I coudn't fetch the news")
    else:
        #let GroqAI handle the requests
        output=aiProcess(c)
        speak(output)

if __name__=="__main__":
    speak("Initializing Jarvis.....")

    while True:
        # Listen for wake word jarvis
        # obtain audio from the microphone
        r = sr.Recognizer()
        

        print("Recognizing...")
        # recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Ya")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
    
        except Exception as e:
            print("error; {0}".format(e))