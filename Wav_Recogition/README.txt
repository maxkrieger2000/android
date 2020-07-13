3 different ways of comparison were used to evaluate the accuracy of the speech recognition
services.
One comparison used the levenshtein distance between the result and ground truth. The 
number of mistakes are found by counting the number of single character replacements,
additions, and subtractions required to change one string to the other.

Another comparison used the difflib python library. This library counts the number of additions and subtractions of single characters needed to turn one string into the other.

The last comparison went through every individual word or character in the ground truth. If
the word was a single character, the character would be compared to the character in the
result. If the word was more than a character, then the difflib library would be used to
calculate the difference of the result word from the word in the ground truth.

Each of these numbers were then divided by the amount of alpha-numeric characters in the
ground truth string to get the outputted percentage.