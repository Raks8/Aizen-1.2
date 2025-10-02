import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import google.generativeai as genai
import datetime
import random
import numpy as np
import requests
import time
import serial

def say(text):
    engine = pyttsx3.init()

    # Set voice (0 = male, 1 = female, depends on your system)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # try 1 if you want a different vibe

    # Set rate (default ~200, slower feels more "Jarvis")
    engine.setProperty('rate', 160)

    # Set volume
    engine.setProperty('volume', 1.0)

    print(f"🗣️ Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

import webbrowser

def play_youtube_video(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")


def get_headlines(api_key, country="in", category=None):
    """Fetch top headlines using NewsAPI"""
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": country,  # e.g., 'us' for USA, 'in' for India
        "apiKey": api_key
    }
    if category:
        params["category"] = category  # e.g., 'technology', 'sports'

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "ok":
            return data["articles"]
        else:
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def show_headlines(api_key, country="in", category=None):
    """Print news headlines"""
    articles = get_headlines(api_key, country, category)

    if articles:
        print(f"📰 Top Headlines ({country.upper()})")
        for i, article in enumerate(articles[:10], start=1):  # show top 10
            tittel = article['title']
            print(f"\n{i}. {tittel}")
            say(tittel)
            if article['description']:
                print(f"   👉 {article['description']}")
            if article['url']:
                print(f"   🔗 {article['url']}")
    else:
        print("No news found or invalid API key.")


def get_weather(city, api_key):
    """Get weather details from OpenWeather API"""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Celsius
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
            "description": data['weather'][0]['description'].title(),
            "city": data['name'],
            "country": data['sys']['country']
        }
    else:
        return None


def show_weather(city, api_key):
    """Fetch weather and print details with conditions"""
    weather = get_weather(city, api_key)
    if weather:  # ✅ Weather data available
        print(f"📍 Location: {weather['city']}, {weather['country']}")
        say(f"LOctaion {weather['city']},{weather['country']}")
        print(f"🌡 Temperature: {weather['temperature']}°C")
        say(f"🌡 Temperature: {weather['temperature']}degree celsius")
        print(f"💧 Humidity: {weather['humidity']}%")
        say(f"💧 Humidity: {weather['humidity']}%")
        print(f"🌬 Wind Speed: {weather['wind_speed']} m/s")
        say(f"🌬 Wind Speed: {weather['wind_speed']} metre per second")
        print(f"☁ Weather: {weather['description']}")
        say(f"☁ Weather: {weather['description']}")

        # Example conditional statements
        if weather['temperature'] > 35:
            print("🔥 It's really hot outside, stay hydrated!")
            say("It is really hot outside, stay hydrated")
        elif weather['temperature'] < 10:
            print("❄ It's quite cold, wear warm clothes!")
            say("It is quite cold wear warm clothes")
        else:
            print("🌤 The weather seems pleasant.")
            say("The weather seems pleasant")

        if "rain" in weather['description'].lower():
            print("☔ Don't forget an umbrella!")
            say("Don't forget an umbrella")
        if "snow" in weather['description'].lower():
            print("⛄ Snowy weather, dress warm!")
            say("Snowy weather, dress warm")
    else:  # ❌ Weather API failed
        print("Could not fetch weather data. Please check your city name or API key.")
        say("Could not fetch weather data. Please check your city name or API key.")

chatStr = ""
# https://youtu.be/Z3ZAJoi4x6Q


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold =  0.6
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

genai.configure(api_key="AIzaSyC6r3JHpurWwmKQMFNwK1Ja8n0JovnDiXQ")

def ai_gemini(prompt):
    text = f"Gemini response for Prompt: {prompt}\n*************************\n\n"
    
    try:
        # Use the latest API without specifying model version
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(f"Answer in under 50 words:\n{prompt}")
        reply = response.text
        text += reply
        print("🤖 Jarvis (Gemini):", reply)
        
    except Exception as e:
        print(f"⚠️ Error with gemini-2.5-flash-latest: {e}")
        
        # Try without version suffix
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(f"Answer in under 50 words:\n{prompt}")
            reply = response.text
            text += reply
            print("🤖 Jarvis (Gemini):", reply)
        except Exception as e2:
            print(f"⚠️ Error with gemini-2.5-flash: {e2}")
            reply = "AI is currently unavailable. Using basic response mode."
            return reply

    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    file_name = f"Gemini/prompt-{random.randint(1,10000)}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text)
    
    say(reply)
    return reply
