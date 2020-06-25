import csv
import os
import azure.cognitiveservices.speech as speechsdk
import re

#run with wav_files folder, transcriptions.txt, and recognition.csv in same directory
service_host = "ws://localhost:5000"
wav_folder = "wav_files"
transcription_file = "transcriptions.txt"
write_file = "recognition_data.csv"
wav_file_name = 2
actual = 1


def main():
    assert os.path.isdir(wav_folder),"folder named 'wav_files' not found"
    assert os.path.isfile(transcription_file),"transcription file named 'transcriptions.txt' not found"
    assert os.path.isfile(write_file),"output file named 'recognition_data.csv' not found"

    regex_matches = []
    regex = re.compile(r"(.+) \((.+)\)")
    transcript = open(transcription_file)
    for line in transcript:
        m = regex.match(line)
        regex_matches.append(m)
    transcript.close()
    results = []
    comparison = []

    speech_config = speechsdk.SpeechConfig(
        host=service_host)


    for match in regex_matches:
        if not os.path.isfile(wav_folder + "/" + match.group(wav_file_name) + ".wav"):
            results.append("file not found")
            comparison.append(False)
            continue
        
        #run speech recognition
        result = speech_from_file(wav_folder + "/" + match.group(wav_file_name) + ".wav", speech_config)

        if result.reason == speechsdk.ResultReason.NoMatch:
            results.append("no match")
            comparison.append(False)
            continue
        elif result.reason == speechsdk.ResultReason.Canceled:
            results.append("recognition cancelled")
            comparison.append(False)
            continue
        elif (not result.reason == speechsdk.ResultReason.RecognizedSpeech):
            results.append("recognition error")
            comparison.append(False)
            continue
        formatted_result = re.sub(r"[^\w\s]" , "", result.text)
        formatted_result = formatted_result.upper()
        results.append(formatted_result)
        comparison.append(formatted_result == match.group(actual))
        print("finished")
    write_to_csv(regex_matches, results, comparison)


def speech_from_file(file_name, speech_config):
    audio_input = speechsdk.audio.AudioConfig(filename = file_name)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once()
    return result


def write_to_csv(regex_matches, results, comparison):
    with open(write_file, mode='w') as recognition_data:
        recognition_writer = csv.writer(recognition_data, delimiter=',')
        for m, r, c in zip(regex_matches, results, comparison):
            recognition_writer.writerow([m.group(wav_file_name), m.group(actual), r, c])
    
    
if __name__ == "__main__":
    main()
