import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import pygame
import tempfile
import os
import time
import uuid

class SpeechHandler:
    def __init__(self):
        self.r = sr.Recognizer()

        self.engine = pyttsx3.init()

        voices = self.engine.getProperty('voices')

        for idx,voice in enumerate(voices):
            print(f"Voice {idx}: {voice.name}")

        self.engine.setProperty('voice', voices[0].id)

        self.engine.setProperty('rate', 170)
        self.engine.setProperty('volume', 0.8)
        self._is_speaking = False

    def listen(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=0.5)
            print("getting input..")
            try:
                audio = self.r.listen(source)
                try:
                    q = self.r.recognize_google(audio, language='en-in')
                    print(q.lower())
                    print('input complete')
                    return q.lower()
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    return None
                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))
                    return None
            except sr.WaitTimeoutError:
                print("Speech timeout - no input detected")
                return None
    def speak(self, text):
        if not text:
            print("No text to speak")
            return
        
        print("Speaking response...")
        self._is_speaking = True

        def onEnd(name, completed):
            self._is_speaking = False
        
        self.engine.connect('finished-utterance', onEnd)
        self.engine.say(text)
        self.engine.runAndWait()

        # temp_dir = tempfile.gettempdir()
        # unique_id = str(uuid.uuid4())
        # temp_file = os.path.join(temp_dir, f"speech_{unique_id}.mp3")

        # try:
        #     print("Generating speech...")
        #     tts = gTTS(text=text, lang='en-uk', slow=False)
        #     tts.save(temp_file)
            
        #     if os.path.exists(temp_file):
        #         print("Speaking response...")
        #         pygame.mixer.music.load(temp_file)
        #         pygame.mixer.music.play()
        #         while pygame.mixer.music.get_busy():
        #             pygame.time.Clock().tick(10)
        #     else:
        #         print(f"Failed to create speech file: {temp_file}")
        # except Exception as e:
        #     print(f"Error in speech synthesis: {e}")
        # finally:
        #     try:
        #         if os.path.exists(temp_file):
        #             time.sleep(0.1)
        #             os.remove(temp_file)
        #     except Exception as e:
        #         print(f"Error cleaning up temporary file: {e}")
    

    def is_speaking(self):
        return self._is_speaking