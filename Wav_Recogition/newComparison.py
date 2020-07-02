import difflib
import csv
import re
import Levenshtein

numdict = {"ZERO":'0', "ONE": '1', "TWO":'2', "THREE": '3',
            "FOUR":'4', "FIVE":'5', "SIX":'6',
            "SEVEN":'7', "EIGHT":'8', "NINE": '9'}

def main():
    truth = []
    result = []
    
    with open('recognition_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if(line_count == 0):
                line_count += 1
                continue
            else:
                truth.append(row[1])
                result.append(row[2])

    new_comp = []
    difflib_comp = []
    leven_comp = []
    for t, r, in zip(truth, result):

        truth_formatted = " " + t + " "
        for word in t.split():
            if word in numdict.keys():
                truth_formatted = truth_formatted.replace(" " + word + " ", " " + numdict[word] + " ")
        divide_by = len(re.sub(r"[^\w]" , "", truth_formatted))
        
        new_comp.append(string_comparison(truth_formatted, r) / divide_by)
        difflib_comp.append(difflib_comparison(truth_formatted, r) / divide_by)
        leven_comp.append(leven_comparison(truth_formatted, r) / divide_by)
    write_to_csv(truth, result, new_comp, difflib_comp, leven_comp)

        


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
            if(not word == result_words[result_word][result_char]):
                wrong_count += 1
            if(result_char + 1 == len(result_words[result_word])):
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

    #divide_by_characters = len(re.sub(r"[^\w]" , "", actual_formatted))

    actual_formatted = re.sub(r"[^\w]" , "", actual)
    result_formatted = re.sub(r"[^\w]" , "", result)
    for diff in difflib.ndiff(result_formatted, actual_formatted):
        if (diff[0] == ' '):
            continue
        elif (diff[0] == '-' or diff[0] == '+'):
            wrong_count += 1
    return wrong_count


def leven_comparison(actual, result):
    wrong_count = 0

    if (re.sub(r"[^\w]" , "", actual) == re.sub(r"[^\w]" , "", result)):
        return 0 #strings are the same

    actual_formatted = re.sub(r"[^\w]" , "", actual)
    result_formatted = re.sub(r"[^\w]" , "", result)
    return Levenshtein.distance(actual_formatted, result_formatted)



def write_to_csv(actual, result, comp, diff, leven):
    comp_sum = 0
    diff_sum = 0
    leven_sum = 0
    with open("new_data.csv", mode='w', newline='') as write_file:
        csv_writer = csv.writer(write_file, delimiter=',')
        csv_writer.writerow(["transcript", "result", "comparison", "difflib comparison", "levenshtein comparison"])
        for a, r, c, d, l in zip(actual, result, comp, diff, leven):
            #write to csv
            comp_sum += c
            diff_sum += d
            leven_sum += l
            csv_writer.writerow([a, r, c, d, l])
        csv_writer.writerow(["averages:", "", comp_sum/len(result), diff_sum/len(result), leven_sum/len(result)])
        
        
    


if __name__ == "__main__":
    main()
