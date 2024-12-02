import webbrowser as wb
import speech_recognition as sr
import pyttsx3
import requests
import pygame
import os
from gtts import gTTS

# Initialize libraries
recognizer = sr.Recognizer()
engine = pyttsx3.init()


def newsapikey(newsapi=None):
    try:
        # Prompt for API key if not provided
        if not newsapi:
            newsapi = "d093053d72bc40248998159804e0e67d"
        # Fetch top news headlines using the API key
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        return response

    except Exception as e:
        return f"Error: {e}. Try again later."



def speak(text):
    engine.say(text)
    engine.runAndWait()


def old_speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the script running while the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()  # Unload the sound after playing
    os.remove("temp.mp3")  # Clean up temp file


def aiProcess(command):
    # Placeholder for OpenAI call
    return "AI response for: " + command


def processCommand(input):
    input = input.lower()

    if "open" in input:
        domain = input.split(" ")[1].lower()
        wb.open(f"https://{domain}.com")

    elif input.startswith("play"):
        song_name = input.replace("play", "").strip()
        choose_music_service(song_name)

    elif "news" in input:
        response = newsapikey("your_api_key_here")
    
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            for article in articles:
                speak(article["title"])

        else:
            speak("Unable to fetch news at the moment.")

    else:
        response = aiProcess(input)
        speak(response)


def choose_music_service(song_name):
    # Ask user to choose between available music services
    speak("Would you like to play on YouTube or Spotify?")

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            service = recognizer.recognize_google(audio).lower()

            if "youtube" in service:
                play_on_youtube(song_name)
            elif "spotify" in service:
                play_on_spotify(song_name)
            else:
                speak(
                    "Sorry, I didn't understand the service. Please say YouTube or Spotify."
                )
    except Exception as e:
        speak("Error detecting service, please try again.")
        print(f"Error: {e}")


def play_on_youtube(song_name):
    query = "+".join(song_name.split())
    url = f"https://www.youtube.com/results?search_query={query}"
    wb.open(url)
    speak(f"Playing {song_name} on YouTube.")


def play_on_spotify(song_name):
    query = "+".join(song_name.split())
    url = f"https://open.spotify.com/search/{query}"
    wb.open(url)
    speak(f"Playing {song_name} on Spotify.")

def main():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'max'...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                word = recognizer.recognize_google(audio)

                if word.lower() == "max":
                    speak("How may I assist you?")

                    # Listen for the actual command
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    speak("Initializing max...")
    main()