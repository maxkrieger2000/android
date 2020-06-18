import azure.cognitiveservices.speech as speechsdk

service_host = "ws://localhost:5000"

speech_config = speechsdk.SpeechConfig(
    host = service_host)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)


print("Say something to convert it to text")

result = speech_recognizer.recognize_once()



if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized by Azure: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))

