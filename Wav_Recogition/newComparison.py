import difflib
import csv
import re
import Levenshtein

numdict = {"ZERO":'0', "ONE": '1', "TWO":'2', "THREE": '3',
            "FOUR":'4', "FIVE":'5', "SIX":'6',
            "SEVEN":'7', "EIGHT":'8', "NINE": '9'}

def main():
    truths = []
    results = []
    
    with open('recognition_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            truths.append(row[1])
            results.append(row[2])

    new_comp = []
    difflib_comp = []
    leven_comp = []
    for truth, result, in zip(truths, results):

        truth_formatted = truth.split()
        for i in range(len(truth_formatted)):
            if truth_formatted[i] in numdict.keys():
                truth_formatted[i] = numdict[truth_formatted[i]]
        truth_formatted = " ".join(truth_formatted)
                
        truth_len = len(re.sub(r"[^\w]" , "", truth_formatted))
        #re.sub used to remove whitespace from the calculation of length
        #   of the string
        
        new_comp.append(string_comparison(truth_formatted, result) / truth_len)
        difflib_comp.append(difflib_comparison(truth_formatted, result) / truth_len)
        leven_comp.append(leven_comparison(truth_formatted, result) / truth_len)
    write_to_csv(truths, results, new_comp, difflib_comp, leven_comp)

        


def string_comparison(actual, result):
    wrong_count = 0

    if (re.sub(r"[^\w]" , "", actual) == re.sub(r"[^\w]" , "", result)):
        return 0 #strings are the same

    result_words = result.split()
    result_word = 0
    result_char = 0
    
    for word in actual.split():

        if (result_word >= len(result_words)):
            #add # of characters left in actual
            wrong_count += len(word)
            continue
        
        if (len(word) == 1):
            #word is a character/number
            if (word != result_words[result_word][result_char]):
                wrong_count += 1
            if (result_char + 1 == len(result_words[result_word])):
               #character is the last in the result word
               result_word += 1
               result_char = 0
            else:
                result_char += 1
        else:
            #word is a word
            result_char = 0

            for diff in difflib.ndiff(word, result_words[result_word]):
                if (diff[0] == ' '):
                    continue
                elif (diff[0] == '-' or diff[0] == '+'):
                    wrong_count += 1
            
            result_word += 1

    if (result_word < len(result_words)):
        #look through words left in result
        for i in range(result_word, len(result_words)):
            wrong_count += len(result_words[i])
    return wrong_count


def difflib_comparison(actual, result):
    wrong_count = 0

    if (re.sub(r"[^\w]" , "", actual) == re.sub(r"[^\w]" , "", result)):
        return 0 #strings are the same

    actual_formatted = re.sub(r"[^\w]" , "", actual)
    result_formatted = re.sub(r"[^\w]" , "", result)
    for diff in difflib.ndiff(result_formatted, actual_formatted):
        if (diff[0] == ' '):
            continue
        elif (diff[0] == '-' or diff[0] == '+'):
            wrong_count += 1
    return wrong_count


def leven_comparison(actual, result):
    actual_formatted = re.sub(r"[^\w]" , "", actual)
    result_formatted = re.sub(r"[^\w]" , "", result)
    if (actual_formatted == result_formatted):
        return 0 #strings are the same
    return Levenshtein.distance(actual_formatted, result_formatted)


def write_to_csv(truths, results, comparisons, diff_comparisons, leven_comparisons):
    comp_sum = 0
    diff_sum = 0
    leven_sum = 0
    list_len = len(results)
    with open("new_data.csv", mode='w', newline='') as write_file:
        csv_writer = csv.writer(write_file, delimiter=',')
        csv_writer.writerow(["transcript", "result", "comparison", "difflib comparison", "levenshtein comparison"])
        for truth, result, comp, diff_comp, leven_comp in zip(truths, results, comparisons, diff_comparisons, leven_comparisons):
            #write to csv
            comp_sum += comp
            diff_sum += diff_comp
            leven_sum += leven_comp
            csv_writer.writerow([truth, result, comp, diff_comp, leven_comp])
        csv_writer.writerow(["averages:", "", comp_sum / list_len, diff_sum / list_len, leven_sum / list_len])
        
        
    


if __name__ == "__main__":
    main()
