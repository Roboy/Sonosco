import azure.cognitiveservices.speech as speechsdk
import librosa
import tempfile


class MicrosoftSTT():

    def __init__(self, key, region, sample_rate):
        self.key = key
        self.region = region
        self.sample_rate = sample_rate

    def speech_recognize_once_from_file(self, audio_path):
        speech_config = speechsdk.SpeechConfig(subscription=self.key, region=self.region)
        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech could be recognized"
        elif result.reason == speechsdk.ResultReason.Canceled:
            return f"Speech Recognition canceled: {result.cancellation_details.reason}"
        else:
            return ""

    def recognize(self, audio):
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
                temp_audio_file.write(audio)
            return self.speech_recognize_once_from_file(temp_audio_file.name)
        except KeyboardInterrupt:
            pass