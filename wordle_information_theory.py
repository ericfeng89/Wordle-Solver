import math
import itertools


def get_expected_entropy(word, words_list):
    current_entropy = math.log(len(words_list), 2)

    new_list = naive_filter(words_list, ['_____'], [word])
    all_grey = len(new_list)
    print(all_grey)
    print(new_list)
    prob_orientation = len(new_list)/len(words_list)

    print(prob_orientation)




    # generate all possible result orientations (e.g. 'GY_G_')
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

    print(possible_orientations)




    # calculate the probability of each orientation occurring
  #  for orientation in possible_orientations
    




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


# def choose_word(words_list):


words_list = get_word_list("data/words-guess.txt")
get_expected_entropy('tares', words_list)