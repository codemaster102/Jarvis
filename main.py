import pyttsx3 # pip install pyttsx3
import speech_recognition as sr #pip install SpeechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import sys
import subprocess #pip install subprocess
from PyDictionary import PyDictionary #pip install PyDictionary
import requests #pip install requests

print("Initializing Jarvis")

master = "Your name"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #0 for a man's voice, 1 for a woman's voice


def speak(text):
    engine.say(text)
    engine.runAndWait()

# This function will greet user according to current time


def greeting():
    hour = int(datetime.datetime.now().hour)
    minute = int(datetime.datetime.now().minute)
    time = ("The time is", hour, minute)
    print("The time is", hour, minute)

    if hour >= 0 and hour < 12:
        speak("Good Morning" + master)

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon" + master)

    else:
        speak("Good Evening" + master)

    speak(time)
    speak("How may I help you today?")

# This function will take command from the mic


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-ca')
        print(f"user said: {query}\n")

    except Exception as e:
        print("Say that again please")
        speak("Didn't catch you there")
        query = None
        sys.exit()
    return query

# This function will open or tell the user different things

def main():

    # Main Program
    speak("Initializing Jarvis")
    greeting()
    query = takecommand().lower()

    # Execution of basic tasks

    if 'wikipedia' in query:
        speak('Searching wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        print(results)
        speak("According to wikipedia" + results)

    elif "search google" in query or "google search" in query:
        query = query.replace("search", "")
        query = query.replace("google", "")
        query = query.replace("for", "")
        webbrowser.open("https://google.com/search?q=%s" % query)

    elif "search youtube" in query or "youtube search" in query:
        query = query.replace("search", "")
        query = query.replace("youtube", "")
        query = query.replace("for", "")
        webbrowser.open("https://www.youtube.com/search?q=%s" % query)

    elif "what is the weather" in query or "what's the weather" in query:
        api_key = "http://api.openweathermap.org/data/2.5/weather?q=" + your_city + "&appid=" + your_api_key
        json_data = requests.get(api_key).json()
        description = json_data['weather'][0]['description']
        temperature = int(json_data['main']['temp'])
        cel = str(int(temperature - 273.15)) #for fahrenheit str(int((temperature - 273.15)*9/5+32)) 
        print("it is " + cel + " degrees celsius with " + description)

    elif "synonym" in query:
        query = query.replace("synonym", "")
        query = query.replace("what is", "")
        query = query.replace("the", "")
        query = query.replace("of", "")
        dictionary=PyDictionary()
        print(dictionary.synonym(query))
        speak(dictionary.synonym(query))

    elif "define" in query or "definition" in query:
        query = query.replace("definition", "")
        query = query.replace("define", "")
        query = query.replace("what is", "")
        query = query.replace("the", "")
        query = query.replace("of", "")
        dictionary=PyDictionary()
        print(dictionary.meaning(query))
        speak(dictionary.meaning(query))

    elif "what is my name" in query:
        speak("Your name is" + master + "sir")

    elif 'open youtube' in query:
        url = "www.youtube.com"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s' #different for mac and linux
        webbrowser.get(chrome_path).open(url)

    elif 'open google' in query:
        url = "www.google.com"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s' #different for mac and linux
        webbrowser.get(chrome_path).open(url)

    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(strTime)
        speak(master + "the time is" + strTime)

    elif 'hey jarvis' in query or 'hey' in query:
        speak("Hello" + master + ", I am here if you need me.")

    elif 'how are you' in query:
        speak("I am great, how about you?")

    elif "i'm good" in query or "i'm great" in query:
        speak("That's great I'm doing fine too.")

    elif query == "i'm doing bad":
        speak("What happened, sir")

    elif "open calculator" in query:
        subprocess.Popen('C:\\Windows\\System32\\calc.exe') #different for mac and linux

main()