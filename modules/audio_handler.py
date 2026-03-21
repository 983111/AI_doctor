import speech_recognition as sr

class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def record_and_transcribe(self):
        """Captures audio from the microphone and transcribes it to text."""
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening for symptoms...")
            
            try:
                audio_data = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                print("Processing audio...")
                # Using Google's free Web Speech API for the prototype
                text = self.recognizer.recognize_google(audio_data)
                return text
            except sr.WaitTimeoutError:
                return "Error: Listening timed out. No speech detected."
            except sr.UnknownValueError:
                return "Error: Could not understand the audio."
            except sr.RequestError as e:
                return f"Error: Speech recognition service unavailable; {e}"