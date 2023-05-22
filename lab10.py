from vosk import Model, KaldiRecognizer
from googlesearch import search
from termcolor import colored
from dotenv import load_dotenv
import speech_recognition
import googletrans
import pyttsx3
import wikipediaapi
import random
import webbrowser
import traceback
import json
import wave
import os


class Translation:
    with open("translations.json", "r", encoding="UTF-8") as file:
        translations = json.load(file)

    def get(self, text: str):
        if text in self.translations:
            return self.translations[text][assistant.speech_language]
        else:
            print(colored("Not translated phrase: {}".format(text), "red"))
            return text


class OwnerPerson:
    name = ""
    native_language = ""
    target_language = ""


class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""


def setup_assistant_voice():
    voices = ttsEngine.getProperty("voices")
    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        if assistant.sex == "female":
            ttsEngine.setProperty("voice", voices[1].id)
        else:
            ttsEngine.setProperty("voice", voices[2].id)
    else:
        assistant.recognition_language = "ru-RU"
        ttsEngine.setProperty("voice", voices[0].id)


def record_and_recognize_audio(*args: tuple):
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)
            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())
        except speech_recognition.WaitTimeoutError:
            play_voice_assistant_speech(translator.get("Can you check if your microphone is on, please?"))
            traceback.print_exc()
            return
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language=assistant.recognition_language).lower()
        except speech_recognition.UnknownValueError:
            play_voice_assistant_speech("What did you say again?")
        except speech_recognition.RequestError:
            print(colored("Trying to use offline recognition...", "cyan"))
            recognized_data = use_offline_recognition()
        return recognized_data


def use_offline_recognition():
    recognized_data = ""
    try:
        if not os.path.exists("models/vosk-model-small-" + assistant.speech_language + "-0.4"):
            print(colored("Oopsie...",
                          "red"))
            exit(1)
        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("models/vosk-model-small-" + assistant.speech_language + "-0.4")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())
        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        traceback.print_exc()
        print(colored("Sorry, speech service is unavailable. Try again later", "red"))
    return recognized_data


def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def play_greetings(*args: tuple):
    greetings = [
        translator.get("Hello, {}! How can I help you today?").format(person.name),
        translator.get("Good day to you {}! How can I help you today?").format(person.name)
    ]
    play_voice_assistant_speech(greetings[random.randint(0, len(greetings) - 1)])


def play_farewell_and_quit(*args: tuple):
    farewells = [
        translator.get("Goodbye, {}! Have a nice day!").format(person.name),
        translator.get("See you soon, {}!").format(person.name)
    ]
    play_voice_assistant_speech(farewells[random.randint(0, len(farewells) - 1)])
    ttsEngine.stop()
    quit()


def search_for_joke_on_google(*args: tuple): #ищет шутку в гугле
    if not args[0]: return
    joke = " ".join(args[0])
    url = "https://google.com/search?q=" + joke
    webbrowser.get().open(url)
    search_results = []
    try:
        for _ in search(joke,
                        tld="com",
                        lang=assistant.speech_language,
                        num=1,
                        start=0,
                        stop=1,
                        pause=1.0,
                        ):
            search_results.append(_)
            webbrowser.get().open(_)


    except:
        play_voice_assistant_speech(translator.get("Oopsie"))
        traceback.print_exc()
        return
    print(search_results)
    play_voice_assistant_speech(translator.get("Here is what I found for {} on google").format(joke))


def search_for_joke_on_site(*args: tuple):#ищет шутку на сайте из условия
    if not args[0]: return
    joke = " ".join(args[0])
    url = "https://v2.jokeapi.dev/joke/Any?safe-mode" + joke
    webbrowser.get().open(url)
    play_voice_assistant_speech(translator.get("Here is what I found for {} on site").format(joke))


def search_for_word_on_wikipedia(*args: tuple):#для незнакомых слов в шутке
    if not args[0]: return
    item = " ".join(args[0])
    wiki = wikipediaapi.Wikipedia(assistant.speech_language)
    wiki_page = wiki.page(item)
    try:
        if wiki_page.exists():
            play_voice_assistant_speech(translator.get("Here is what I found for {} on Wikipedia").format(item))
            webbrowser.get().open(wiki_page.fullurl)
            play_voice_assistant_speech(wiki_page.summary.split(".")[:2])
        else:
            play_voice_assistant_speech(translator.get(
                "Can't find {} on Wikipedia. But here is what I found on google").format(item))
            url = "https://google.com/search?q=" + item
            webbrowser.get().open(url)
    except:
        play_voice_assistant_speech(translator.get("Seems like we have a trouble."))
        traceback.print_exc()
        return


def get_translation(*args: tuple):
    if not args[0]: return
    thing = " ".join(args[0])
    google_translator = googletrans.Translator()
    translation_result = ""
    old_assistant_language = assistant.speech_language
    try:

        if assistant.speech_language != person.native_language:
            translation_result = google_translator.translate(thing,
                                                      src=person.target_language,
                                                      dest=person.native_language)
            play_voice_assistant_speech("The translation for {} in Russian is".format(thing))
            assistant.speech_language = person.native_language
            setup_assistant_voice()


        else:
            translation_result = google_translator.translate(thing,
                                                      src=person.native_language,
                                                      dest=person.target_language)
            play_voice_assistant_speech("По-английски {} будет как".format(thing))
            assistant.speech_language = person.target_language
            setup_assistant_voice()
        play_voice_assistant_speech(translation_result.text)
    except:
        play_voice_assistant_speech(translator.get("Oopsie..."))
        traceback.print_exc()

    finally:
        assistant.speech_language = old_assistant_language
        setup_assistant_voice()

def change_language(*args: tuple):

    assistant.speech_language = "ru" if assistant.speech_language == "en" else "en"
    setup_assistant_voice()
    print(colored("Language switched to " + assistant.speech_language, "cyan"))



def coin(*args: tuple): #бросить монетку
    flips_count, heads, tails = 3, 0, 0

    for flip in range(flips_count):
        if random.randint(0, 1) == 0:
            heads += 1

    tails = flips_count - heads
    winner = "Tails" if tails > heads else "Heads"
    play_voice_assistant_speech(translator.get(winner) + " " + translator.get("won"))


def execute_command_with_name(command_name: str, *args: list):
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            print("Command not found")

commands = {
    ("hello", "hi", "morning", "привет"): play_greetings,
    ("bye", "goodbye", "quit", "exit", "stop", "пока"): play_farewell_and_quit,
    ("search", "joke", "find", "найди"): search_for_joke_on_google,
    ("jokes", "search for", "site", "сайт"): search_for_joke_on_site,
    ("wikipedia", "definition", "about", "определение", "википедия"): search_for_word_on_wikipedia,
    ("translate", "interpretation", "translation", "перевод", "перевести", "переведи"): get_translation,
    ("language", "язык","поменяй"): change_language,
    ("toss", "coin", "монета", "подбрось"): coin,
}

if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    ttsEngine = pyttsx3.init()

    person = OwnerPerson()
    person.name = "Sergey"
    person.native_language = "ru"
    person.target_language = "en"

    assistant = VoiceAssistant()
    assistant.name = "Lisa"
    assistant.sex = "female"
    assistant.speech_language = "en"

    setup_assistant_voice()
    translator = Translation()
    load_dotenv()
    while True:
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        print(colored(voice_input, "blue"))
        voice_input = voice_input.split(" ")
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_name(command, command_options)


