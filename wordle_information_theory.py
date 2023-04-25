import math
import itertools


# generate all possible result orientations (e.g. 'GY_G_')
def generate_possible_orientations():

    possible_orientations = []
    wordle = "_____"
    colors = ["G", "Y", "_"]

    # Get the indices of the blanks ("_") in the wordle
    blanks = [i for i, letter in enumerate(wordle) if letter == "_"]

    # Generate all possible combinations of "G", "Y", and "_"
    combinations = list(itertools.product(colors, repeat=len(blanks)))

    # Replace the blanks with the combinations
    for combo in combinations:
        new_wordle = list(wordle)
        for i, blank in enumerate(blanks):
            new_wordle[blank] = combo[i]
        possible_orientations.append("".join(new_wordle))

    return possible_orientations

def get_expected_entropy(word, words_list):

    # calculate the probability of each orientation occurring
    entropy_sum = 0
    for orientation in possible_orientations:
        current_entropy = math.log(len(words_list), 2)

        new_list = naive_filter(words_list, [orientation], [word])
     #   new_list = words_list

        if len(new_list) != 0:
            prob_orientation = len(new_list)/len(words_list)
            new_entropy = math.log(len(new_list), 2)
            entropy_sum += prob_orientation * (current_entropy - new_entropy)

 #   print(word)
 #   print(entropy_sum)
    return entropy_sum

# choose highest entropy word from potential words
def choose_word(words_list):
    max_entropy = 0
    max_word = ""

    for word in words_list:
        expected_entropy = get_expected_entropy(word, words_list)
        if expected_entropy > max_entropy:
            max_entropy = expected_entropy
            max_word = word

    print(max_word)
    return max_word




def get_word_list(filename):
   words = []
   with open(filename, "r", encoding="UTF-8") as in_file:
           for line in in_file:
               words.append(line.strip())
   return words

def naive_filter(validGuesses, results, guesses):
    result = results[-1]
    lastGuess = guesses[-1]
    guessFilter = validGuesses[:]

    for guess in validGuesses:
        for i in range(5):
            if result[i] == '_':
                if lastGuess[i] in guess:
                    guessFilter.remove(guess)
                    break 
            elif result[i] == 'Y':
                if (lastGuess[i] not in guess) or (guess[i] == lastGuess[i]):
                    guessFilter.remove(guess)
                    break
            elif result[i] == 'G':
                if guess[i] != lastGuess[i]:
                    guessFilter.remove(guess)
                    break

    return guessFilter


words_list = get_word_list("data/words-guess.txt")
possible_orientations = generate_possible_orientations()
choose_word(words_list)