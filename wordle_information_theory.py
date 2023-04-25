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

    print(word)
    print(entropy_sum)
    return entropy_sum

# choose highest entropy word from potential words
def choose_word(words_list):
    max_entropy = 0
    max_word = ""

    for word in words_list:
        expected_entropy = get_expected_entropy(word, words_list)
        if expected_entropy > max_entropy:
            expected_entropy = max_entropy
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
    # get last result and guess
    result = results[-1]
    lastGuess = guesses[-1]

    greyFails = list()
    for i in range(5):
        if result[i] == '_':
            # this letter should not be in the word
            for guess in validGuesses:
                if lastGuess[i] in guess:
                    greyFails.append(guess)


    greyGuesses = list()
    for guess in validGuesses:
        if guess not in greyFails:
            greyGuesses.append(guess)
    
    # yellow letters
    yellowFails = list()
    for i in range(5):
        if result[i] == 'Y':
            # this location should not be this letter but somewhere else should be
            for guess in greyGuesses:
                if (lastGuess[i] not in guess) or (guess[i] == lastGuess[i]):
                    yellowFails.append(guess)


    yellowGuesses = list()
    for guess in greyGuesses:
        if guess not in yellowFails:
            yellowGuesses.append(guess)


    # put green letters in the right place
    greenFails = list()
    for i in range(5):
        if result[i] == 'G':
            # this location should be this letter
            for guess in yellowGuesses:
                if guess[i] != lastGuess[i]:
                    greenFails.append(guess)
    
    greenFilter = list()
    for guess in yellowGuesses:
        # add check for previous guess?
        if guess not in greenFails:
            greenFilter.append(guess)

    return greenFilter


words_list = get_word_list("data/words-guess.txt")
possible_orientations = generate_possible_orientations()
choose_word(words_list)