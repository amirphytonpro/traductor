import time
import speech_recognition as sr
from googletrans import Translator
from textblob import TextBlob

# Variable para almacenar la mayor puntuación
mayor_puntuacion = 0

# Función para mostrar las frases de aprendizaje en el idioma seleccionado


def learning_mode(language_code, japanese_dialect=None):
    translator = Translator()
    phrases = {
        'en': {
            'hello': 'Hello',
            'goodbye': 'Goodbye',
            'thank you': 'Thank you',
            'yes': 'Yes',
            'no': 'No'
        },
        'es': {
            'hello': 'Hola',
            'goodbye': 'Adiós',
            'thank you': 'Gracias',
            'yes': 'Sí',
            'no': 'No'
        },
        'fr': {
            'hello': 'Bonjour',
            'goodbye': 'Au revoir',
            'thank you': 'Merci',
            'yes': 'Oui',
            'no': 'Non'
        },
        'it': {
            'hello': 'Ciao',
            'goodbye': 'Arrivederci',
            'thank you': 'Grazie',
            'yes': 'Sì',
            'no': 'No'
        },
        'ja': {
            'tokyo': {
                'hello': 'こんにちは - konnichiwa',
                'goodbye': 'さようなら - sayōnara',
                'thank you': 'ありがとう - arigatō',
                'yes': 'はい - hai',
                'no': 'いいえ - iie'
            },
            'kyushu': {
                'hello': 'おっす - ossu',
                'goodbye': 'じゃあね - jā ne',
                'thank you': 'おおきに - ōkini',
                'yes': 'うん - un',
                'no': 'いや - iya'
            },
            'kansai': {
                'hello': 'おっはよう - ohayō',
                'goodbye': 'せやな - seyana',
                'thank you': 'おおきに - ōkini',
                'yes': 'うん - un',
                'no': 'いや - iya'
            }
        }
    }

    print(f"Learning mode for {translator.translate(
        'Learning Mode', dest=language_code).text}:")
    print("Here are some basic phrases in your selected language:")

    if language_code == 'ja' and japanese_dialect:
        for english_phrase, japanese_phrase in phrases['ja'][japanese_dialect].items():
            print(f"{japanese_phrase} - {phrases['en'][english_phrase]}")
    else:
        for english_phrase, translation in phrases[language_code].items():
            print(f"{translation} - {phrases['en'][english_phrase]}")

# Función para reconocer el discurso desde el micrófono


def recognize_speech():
    global mayor_puntuacion
    recognizer = sr.Recognizer()
    start_time = time.time()  # Obtener el tiempo de inicio
    word_count = 0  # Inicializar el conteo de palabras
    puntos = 0  # Inicializar los puntos

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(
            source)  # Ajustar al ruido ambiental
        audio_data = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(
                audio_data, language='en-US')  # Reconocer discurso en inglés
            print("You said:", text)
            word_count += len(text.split())  # Incrementar conteo de palabras

            # Actualizar puntos basados en el conteo de palabras u otros criterios
            puntos += word_count  # Ejemplo: Incrementar puntos por conteo de palabras

            # Actualizar la mayor puntuación si la puntuación actual es mayor
            if puntos > mayor_puntuacion:
                mayor_puntuacion = puntos

            # Verificar el tiempo y el conteo de palabras
            elapsed_time = time.time() - start_time
            # Si han pasado más de 15 segundos o se han dicho 10 palabras, detener
            if elapsed_time > 15 or word_count >= 10:
                print("Time's up or word limit reached. Stopping...")
                # Mostrar puntuación y mayor puntuación
                print("Your score:", puntos)
                print("Highest Score:", mayor_puntuacion)

                # Incrementar el tiempo si todo está bien
                if puntos > 0:  # Si se han dicho palabras
                    print("Congratulations! You've earned extra time.")
                    # Incrementar el tiempo en 5 segundos
                    elapsed_time += 5
                    print("Time elapsed:", elapsed_time, "seconds")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error making request; {0}".format(e))

# Preguntar al usuario por el idioma de aprendizaje y el modo de juego al inicio del programa


def start_game():
    while True:
        print("Select your learning language:")
        print("1. English")
        print("2. Spanish")
        print("3. French")
        print("4. Italian")
        print("5. Japanese")
        choice = input(
            "Enter the number of your preferred learning language: ")
        if choice == "1":
            language_code = "en"
            break
        elif choice == "2":
            language_code = "es"
            break
        elif choice == "3":
            language_code = "fr"
            break
        elif choice == "4":
            language_code = "it"
            break
        elif choice == "5":
            language_code = "ja"
            japanese_dialect = None
            while not japanese_dialect:
                print("Select Japanese dialect:")
                print("1. Tokyo")
                print("2. Kyushu")
                print("3. Kansai")
                dialect_choice = input(
                    "Enter the number of your preferred Japanese dialect: ")
                if dialect_choice == "1":
                    japanese_dialect = "tokyo"
                elif dialect_choice == "2":
                    japanese_dialect = "kyushu"
                elif dialect_choice == "3":
                    japanese_dialect = "kansai"
                else:
                    print("Invalid choice. Please try again.")
            break
        else:
            print("Invalid choice. Please try again.")

    while True:
        print("Select mode:")
        print("1. Learning Mode")
        print("2. Voice Mode")
        mode_choice = input("Enter the number of your preferred mode: ")
        if mode_choice == "1":
            learning_mode(language_code, japanese_dialect)
            break
        elif mode_choice == "2":
            recognize_speech()
            break
        else:
            print("Invalid choice. Please try again.")


start_game()
