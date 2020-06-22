import azure.cognitiveservices.speech as speechsdk
import uuid
import os.path

service_host = "ws://localhost:5000"

def main():
    print("type in a value for speech to text")
    speechOption = input("1: Speech from Mic, 2: Speech from File: ")
    
    if(speechOption == "1"):
        results = speech_from_mic()
    elif(speechOption == "2"):
        results = speech_from_file()
    else:
        return

    if results != 0 and results.reason == speechsdk.ResultReason.RecognizedSpeech:
        saveResults = input("save answer to file? (Y/N): ")
        if(saveResults == "Y"):
            saveFile = open(str(uuid.uuid1()) + ".txt", "w")
            saveFile.write(results.text)
            saveFile.close()

            
def speech_from_mic():
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
    return result


def speech_from_file():
    speech_config = speechsdk.SpeechConfig(
        host = service_host)
    audio_filename = input("input the name of the .wav file: ")
    audio_filename = audio_filename + ".wav"
    
    while(!os.path.isfile(audio_filename)):
        print("invalid file name")
        audio_filename = input("try another filename or hit enter to exit:")
        if(audio_filename == ""):
            return 0
        audio_filename = audio_filename + ".wav"
    
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    print("Processing audio file...")
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
    return result


if __name__ == "__main__":
    main()
    
