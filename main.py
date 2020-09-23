import pyttsx3
import speech_recognition as sr
import time
import wikipedia
import webbrowser
import os
import subprocess
from PyDictionary import PyDictionary
import requests
import datetime
from countryinfo import CountryInfo
import pyperclip
import random
from win10toast import ToastNotifier

master = "Aromal"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

shopping_list = []


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
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-ca')
        print(f"user said: {query}\n")

    except Exception as e:
        error = "Didn't catch you there", "Sorry, I don't understand"
        speak(random.choice(error))
        query = None
    return query

# This function will open or tell the user different things


def main():

    # Main Program
    greeting()
    query = takecommand().lower()

    # Execution of basic tasks

    if 'wikipedia' in query:
        speak('Searching wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        print(results)
        speak("According to wikipedia" + results)

    elif "directions" in query or "map" in query or "direction" in query:
        speak("Ok, what is the starting location?")
        start = takecommand()
        speak("Thanks, what is the destination?")
        end = takecommand()
        webbrowser.open_new_tab(
            "https://www.google.ca/maps/dir/" + start + "/" + end)

    elif "emoji" in query:
        emoji = input('Write emoji: ')
        a = emoji.split()
        emojis = {
            ':)': '😀',
            ':(': '😟',
            ';)': '😉',
            '<3': '♥',
            '¯\_( ͡❛ ͜ʖ ͡❛)_/¯': '🤷‍♂️'
        }

        output = ""

        speak("Please write emoji to convert")

        for words in a:
            output += emojis.get(words, words) + ' '
            pyperclip.copy(output)
        print("Emoji Copied!")

    elif "search google" in query or "google search" in query:
        query = query.replace("search", "")
        query = query.replace("google", "")
        query = query.replace("for", "")
        webbrowser.open("https://google.com/search?q=%s" % query)

    elif "search youtube" in query or "youtube search" in query:
        query = query.replace("search", "")
        query = query.replace("youtube", "")
        query = query.replace("for", "")
        webbrowser.open("https://www.youtubekids.com/search?q=%s" % query)

    elif "+" in query:
        words = query.lower().split()
        num1 = int(words[words.index('+')-1])
        num2 = int(words[words.index('+')+1])
        print(str(num1) + " + " + str(num2) + " = " + str(num1+num2))

    elif "-" in query:
        words = query.lower().split()
        num1 = int(words[words.index('-')-1])
        num2 = int(words[words.index('-')+1])
        print(str(num1) + " - " + str(num2) + " = " + str(num1-num2))

    elif "*" in query:
        words = query.lower().split()
        num1 = int(words[words.index('*')-1])
        num2 = int(words[words.index('*')+1])
        print(str(num1) + " x " + str(num2) + " = " + str(num1*num2))

    elif "/" in query:
        words = query.lower().split()
        num1 = int(words[words.index('/')-1])
        num2 = int(words[words.index('/')+1])
        print(str(num1) + " ÷ " + str(num2) + " = " + str(num1/num2))

    elif "password" in query:
        speak("Are special charecters allowed?")
        special_chars = takecommand()
        if special_chars == "yes":
            chars = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*"

        else:
            chars = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        speak("What is the length of the password?")
        length = int(takecommand())
        password = ''
        for c in range(length):
            password += random.choice(chars)
        pyperclip.copy(password)
        print(password + " is Copied!")

    elif "shopping list" in query:
        print("This is your current shopping list: " + str(shopping_list))
        question = takecommand()
        if question == "yes" or question == "y":
            new_item = str(takecommand())
            new_item = new_item.split(" and ")
            shopping_list.append(new_item)
            print("This is your new shopping list: " + str(shopping_list))

        else:
            speak("ok")

    elif "weather" in query or "what's the weather" in query:
        api_key = "http://api.openweathermap.org/data/2.5/weather?q=Brampton&appid=8ac80f9a96e20266674ae577d21d29ed"
        json_data = requests.get(api_key).json()
        description = json_data['weather'][0]['description']
        temperature = int(json_data['main']['temp'])
        cel = str(int(temperature - 273.15))
        if description == "broken clouds":
            print("it is " + cel + " degrees celsius with " + description)
            speak("it is " + cel + " degrees celsius with " + description)

        else:
            print("it is " + cel + " degrees celsius with a " + description)
            speak("it is " + cel + " degrees celsius with a " + description)

    elif "capital of" in query:
        word_list = query.split()
        country = CountryInfo(word_list[-1])
        capital_city = str(country.capital())
        print(capital_city)
        speak("It's capital is" + capital_city)

    elif "synonym" in query:
        query = query.replace("synonym", "")
        query = query.replace("what is", "")
        query = query.replace("the", "")
        query = query.replace("of", "")
        dictionary = PyDictionary()
        print(dictionary.synonym(query))
        speak(dictionary.synonym(query))

    elif "define" in query or "definition" in query:
        query = query.replace("definition", "")
        query = query.replace("define", "")
        query = query.replace("what is", "")
        query = query.replace("the", "")
        query = query.replace("of", "")
        dictionary = PyDictionary()
        print(dictionary.meaning(query))
        speak(dictionary.meaning(query))

    elif "what is your name" in query:
        speak("My name is Jarvis, sir")

    elif 'open youtube' in query:
        url = "www.youtube.com"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        speak("Opening youtube")
        webbrowser.get(chrome_path).open(url)

    elif 'open google' in query:
        url = "chrome://newtab/"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        speak("Opening google")
        webbrowser.get(chrome_path).open_new_tab(url)

    elif 'time' in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        formatted_time = datetime.datetime.now().strftime("%H %M")
        print(current_time)
        speak(master + "the time is" + formatted_time)

    elif 'hey jarvis' in query or 'hey' in query:
        speak("Hello" + master + ", I am here if you need me.")

    elif 'how are you' in query:
        speak("I am great, how about you?")

    elif "i'm good" in query or "i'm great" in query:
        speak("That's great I'm doing fine too.")

    elif "i'm doing bad" in query:
        speak("What happened, sir")

    elif "open calculator" in query:
        subprocess.Popen('C:\\Windows\\System32\\calc.exe')

    else:
        speak("Sorry I can't do that yet")


main()
