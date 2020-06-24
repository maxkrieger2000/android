import csv
import os
import azure.cognitiveservices.speech as speechsdk
import re

#run with wav_files folder, transcriptions.txt, and recognition.csv in same directory
service_host = "ws://localhost:5000"
wav_folder = "wav_files"
transcription_file = "transcriptions.txt"
write_file = "recognition_data.csv"


def main():
    if (not os.path.isdir(wav_folder)):
        return
    if (not os.path.isfile(transcription_file)):
        return
    if (not os.path.isfile(write_file)):
        return

    transcript = open(transcription_file)
    transcript_string = transcript.read()
    transcript.close()
    file_names = re.findall(r"(?<=\().*(?=\))", transcript_string)
    actual = re.findall(r".+?(?=\ \()", transcript_string)
    
    results = []
    match = []

    speech_config = speechsdk.SpeechConfig(
        host=service_host)

    print(file_names)
    print(actual)
    
    for i in range(len(file_names)):
        if not os.path.isfile(wav_folder + "/" + file_names[i] + ".wav"):
            results.append("file not found")
            match.append(False)
            continue
        
        #run speech recognition
        result = speech_from_file(wav_folder + "/" + file_names[i] + ".wav", speech_config)

        if result.reason == speechsdk.ResultReason.NoMatch:
            results.append("no match")
            match.append(False)
            continue
        elif result.reason == speechsdk.ResultReason.Canceled:
            results.append("recognition cancelled")
            match.append(False)
            continue
        elif (not result.reason == speechsdk.ResultReason.RecognizedSpeech):
            results.append("recognition error")
            match.append(False)
            continue
        formatted_result = re.sub(r"[^\w\s]" , "", result.text)
        formatted_result.upper()
        results.append(formatted_result)
        match.append(formatted_result == actual[i])
        print("finished")
    write_to_csv(file_names, actual, results, match)


def speech_from_file(file_name, speech_config):
    audio_input = speechsdk.audio.AudioConfig(filename = file_name)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once()
    return result


def write_to_csv(file_names, actual, results, match):
    with open(write_file, mode='w') as recognition_data:
        recognition_writer = csv.writer(recognition_data, delimiter=',')

        for i in range(len(results)):
            recognition_writer.writerow([file_names[i], actual[i], results[i], match[i]])
    
    
if __name__ == "__main__":
    main()
