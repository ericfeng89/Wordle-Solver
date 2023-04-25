import math
import itertools
from wordle_naive import words_list
import random
from termcolor import colored


### Taken from the github repo
class Wordle:
    ''' Class representing one wordle game.
    methods include initiating a secret word,
    returning green/yellow/grey results,
    keeping track of guessed letters
    '''

    def __init__(self, words_list, correct_word=None):
        # the word to guess
        self.correct_word = random.choice(words_list) if correct_word == None else correct_word


        # list of guesses so far
        self.guesses = []
        self.results = []


    def __str__(self):
        out = f"::{self.correct_word}::"
        for i, guess in enumerate(self.guesses):
            out += f"\n{i+1}. {guess}"
        return out


    def guess(self, word):
        ''' One turn of the game
        get guessed word, add new Guess in guesses list
        if guessed correctly, return True, else False
        '''
        self.guesses.append(word)
        out = ""
        for guess_letter, correct_letter in zip(word, self.correct_word):
            if guess_letter == correct_letter:
                out += "G"
            elif guess_letter in self.correct_word:
                out += "Y"
            else:
                out += "_"
        self.results.append(out)
        # Return True/False if you got the word right
        return word ==  self.correct_word
    
    # works well, I think we could use the old possible guess list rather than regenerating for future scaling
    def naive_filter(self, validGuesses):
        # get last result and guess
        result = self.results[-1]
        lastGuess = self.guesses[-1]
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


        # play a wordle game with naive strat, given startword
        # returns i, the number of guesses to find the word
    def play_game(self, verbose=True):
        startword = choose_word(words_list)

        if verbose: print('GUESSING: ', startword)
            
        prevGuess = startword
        # simulate one game
        possible_words = words_list
        while(not (self.guess(prevGuess))):
            if verbose: print('RESULT: ', self.results[len(self.guesses) - 1])
            possible_words = self.naive_filter(possible_words)
            if verbose: print('POSSIBLE ANSWERS: (', str(len(possible_words)), ') ' , possible_words)

            nextGuess = choose_word(possible_words)
            if verbose: print('GUESSING: ', nextGuess)
            prevGuess = nextGuess

        if verbose: 
            if len(self.guesses) > 6: print(colored('Guess max (6) exceded', 'red'))
            strout = 'correct word: '+ self.correct_word + ' found in ' + str(len(self.guesses)) + ' guesses!'
            print(colored(strout, 'green'))

        return len(self.guesses)


    

# choose highest entropy word from potential words
def choose_word(words_list):
    max_entropy = 0
    max_word = ""

    for i, word in enumerate(words_list):
        # Print the progress bar
        if len(words_list) > 1:
            progress = i / (len(words_list) - 1)
            num_bars = int(progress * 40)
            print('\r[{}{}] words tested: {}/{}'.format('#' * num_bars, '-' * (40 - num_bars), i+1, len(words_list)), end='')

        expected_entropy = get_expected_entropy(word, words_list)
        if expected_entropy > max_entropy:
            max_entropy = expected_entropy
            max_word = word

    print(max_word)
    return max_word

def get_expected_entropy(word, words_list):

        # calculate the probability of each orientation occurring
        entropy_sum = 0
        for orientation in possible_orientations:
            current_entropy = math.log(len(words_list), 2)

            new_list = filter(words_list, [orientation], [word])
        #   new_list = words_list

            if len(new_list) != 0:
                prob_orientation = len(new_list)/len(words_list)
                new_entropy = math.log(len(new_list), 2)
                entropy_sum += prob_orientation * (current_entropy - new_entropy)

    #   print(word)
    #   print(entropy_sum)
        return entropy_sum

def filter(validGuesses, results, guesses):
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

def get_word_list(filename):
    words = []
    with open(filename, "r", encoding="UTF-8") as in_file:
            for line in in_file:
                words.append(line.strip())
    return words


words_list = get_word_list("data/words-guess.txt")

if __name__ == '__main__':
    
    possible_orientations = generate_possible_orientations()

    wordle = Wordle(words_list)

    wordle.play_game()