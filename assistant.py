import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import re


# ========================= VOICE ENGINE =========================

engine = pyttsx3.init()

engine.setProperty("rate", 180)
engine.setProperty("volume", 1)


def speak(text):

    print(f"\nNova: {text}")

    engine.say(text)
    engine.runAndWait()


# ========================= VOICE RECOGNITION =========================

recognizer = sr.Recognizer()


# ====================== BETTER NOISE HANDLING ======================

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True


def listen():

    try:

        with sr.Microphone() as source:

            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        print("Recognizing...")

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        command = command.lower()

        print(f"\nYou Said: {command}")

        return command


    except sr.WaitTimeoutError:

        print("Listening timeout")

        return ""


    except sr.UnknownValueError:

        print("Could not understand audio")

        return ""


    except sr.RequestError:

        print("Internet connection issue")

        return ""


    except Exception as e:

        print("Error:", e)

        return ""


# ========================= MATH SOLVER =========================

def solve_math(command):

    expression = command

    replacements = {

        "calculate": "",
        "plus": "+",
        "minus": "-",
        "multiply": "*",
        "into": "*",
        "divide": "/",
        "x": "*"

    }

    for word, symbol in replacements.items():

        expression = expression.replace(
            word,
            symbol
        )

    expression = re.sub(
        r"[^0-9\+\-\*\/\.\(\)]",
        "",
        expression
    )

    try:

        return eval(expression)

    except:

        return None


# ========================= COMMAND EXECUTOR =========================

def execute_command(command):


    # ================= TIME =================

    if "time" in command:

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        speak(f"The time is {current_time}")


    # ================= DATE =================

    elif "date" in command:

        current_date = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        speak(f"Today's date is {current_date}")


    # ================= OPEN GOOGLE =================

    elif "open google" in command:

        webbrowser.open(
            "https://www.google.com"
        )

        speak("Google opened")


    # ================= OPEN YOUTUBE =================

    elif "open youtube" in command:

        webbrowser.open(
            "https://www.youtube.com"
        )

        speak("YouTube opened")


    # ================= OPEN CHATGPT =================

    elif "open chatgpt" in command:

        webbrowser.open(
            "https://chatgpt.com"
        )

        speak("ChatGPT opened")


    # ================= OPEN APPS =================

    elif "open notepad" in command:

        os.system("notepad")

        speak("Notepad opened")


    elif "open calculator" in command:

        os.system("calc")

        speak("Calculator opened")


    elif "open command prompt" in command:

        os.system("start cmd")

        speak("Command Prompt opened")


    # ================= CALCULATE =================

    elif "calculate" in command:

        result = solve_math(command)

        if result is not None:

            speak(f"The answer is {result}")

        else:

            speak("Calculation failed")


    # ================= PLAY SONG =================

    elif "play" in command:

        song = command.replace(
            "play",
            ""
        ).strip()

        if song:

            speak(f"Playing {song}")

            import pywhatkit

            pywhatkit.playonyt(song)

        else:

            speak("Please tell me the song name")


    # ================= GOOGLE SEARCH =================

    elif "search" in command:

        query = command.replace(
            "search",
            ""
        ).strip()

        if query:

            speak(f"Searching {query}")

            import pywhatkit

            pywhatkit.search(query)

        else:

            speak("Please tell me what to search")


    # ================= SHUTDOWN =================

    elif "shutdown" in command:

        speak("Shutting down computer")

        os.system("shutdown /s /t 5")


    # ================= RESTART =================

    elif "restart" in command:

        speak("Restarting computer")

        os.system("shutdown /r /t 5")


    # ================= EXIT =================

    elif (
        "stop nova" in command
        or "sleep nova" in command
    ):

        speak("Going to sleep mode")

        return False


    # ================= UNKNOWN COMMAND =================

    else:

        speak(
            "Sorry, this command is not available."
        )


    return True


# ========================= START MESSAGE =========================

speak(
    "Hey Ashish, Nova is activated. "
    "Say Hello Nova."
)


# ========================= WAKE WORD SYSTEM =========================

while True:

    wake = listen()


    if (
        "hello nova" in wake
        or "hey nova" in wake
    ):

        speak(
            "Yes Ashish, I am listening."
        )

        active = True


        while active:

            command = listen()


            if command == "":

                continue


            active = execute_command(
                command
            )