import speech_recognition as sr
import pyttsx3
import subprocess
import datetime
from googletrans import Translator
import pygame
from gtts import gTTS
import os

# Ініціалізуємо об'єкт для розпізнавання голосу
recognizer = sr.Recognizer()

# Ініціалізуємо об'єкт для синтезу речі
ttsEngine = pyttsx3.init()

# Отримуємо доступні голоси
voices = ttsEngine.getProperty('voices')

# Вибираємо голос, наприклад, перший доступний голос
ttsEngine.setProperty('voice', voices[2].id)

# Ініціалізуємо об'єкт для перекладу
translator = Translator()

active_flag = False

pygame.mixer.init()

# Очистка ресурсів шоб не тупив
def cleanup_resources():
    pygame.mixer.music.stop()
    recognizer.energy_threshold = 4000

# Функція для програвання аудіо глобально
def play_audio_file(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def speak(text):
    ttsEngine.say(text)
    ttsEngine.runAndWait()

def execute_voice_command():
    play_audio_file('jarvis-og\\run.wav')
    global active_flag
    while True:
        command = listen_and_recognize()
        print("Ви сказали:", command)

        if not active_flag and "джарвіс" in command:
            active_flag = True
            cleanup_resources()
            play_audio_file('jarvis-og\\greet2.wav')
        elif "як справи" in command:
            response_text = "У мене все гаразд, дякую!"
            speak(response_text)
            cleanup_resources()
            save_audio_response(response_text, "response.mp3")
        elif "відкрий google" in command:
            play_audio_file("D:\\CodeMaster\\Python\\jarvis\\jarvis-og\\ok2.wav")
            cleanup_resources()
            open_program(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        elif "шукай" in command:
            cleanup_resources()
            play_audio_file('songs\import.wav')
            search_query = listen_and_recognize()
            open_website(f"https://www.google.com/search?q={search_query}")

        elif "відкрий youtube" in command:
            cleanup_resources()
            play_audio_file("D:\\CodeMaster\\Python\\jarvis\\jarvis-og\\ok3.wav")
            open_website('https://www.youtube.com')

        elif "ігровий режим" in command:
            cleanup_resources()
            play_audio_file("jarvis-og\game_mode.wav")
            open_program(r'D:\Game\Steam\steam.exe')

        elif "робочий режим" in command:
            cleanup_resources()
            play_audio_file("songs\perezapusk.wav")
            close_program('steam')


        elif "досить" in command:
            play_audio_file("D:\\CodeMaster\\Python\\jarvis\\jarvis-og\\off.wav")
            exit()

def close_program(program_name):
    try:
        os.system(f"taskkill /f /im {program_name}.exe")
    except Exception as e:
        print(f"Помилка при закритті програми: {e}")


def open_program(program_path):
    try:
        subprocess.Popen(program_path)
    except Exception as e:
        print(f"Помилка відкриття програми: {e}")

def open_website(url):
    subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', url])

def listen_and_recognize():
    with sr.Microphone(device_index=0) as source:  # Задайте індекс мікрофона тут
        print("Скажіть щось...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="uk-UK")
        return text.lower()
    except sr.UnknownValueError:
        return "Не розпізнано"
    except sr.RequestError:
        return "Помилка сервісу розпізнавання"

def save_audio_response(text, filename):
    tts = gTTS(text=text, lang='uk')
    tts.save(filename)

if __name__ == "__main__":
    execute_voice_command()

if __name__ == "__main__":
    program_path = r'D:\Game\Steam\steam.exe'
    open_program(program_path)
