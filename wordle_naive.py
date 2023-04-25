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


def get_word_list(filename):
   words = []
   with open(filename, "r", encoding="UTF-8") as in_file:
           for line in in_file:
               words.append(line.strip())
   return words

# play a wordle game with naive strat, given startword
# returns i, the number of guesses to find the word
def play_game(game, startword, verbose=True):
    if verbose: print('GUESSING: ', startword)
    game.guess(startword)
    prevGuess = startword
    # simulate one game
    num_guesses = 1
    possible_words = words_list
    while(not (game.guess(prevGuess))):
        if verbose: print('RESULT: ', game.results[num_guesses])
        possible_words = naive_filter(possible_words, game.results, game.guesses)
        if verbose: print('POSSIBLE ANSWERS: (', str(len(possible_words)), ') ' , possible_words)

        nextGuess = random.choice(possible_words)
        if verbose: print('GUESSING: ', nextGuess)
        num_guesses = num_guesses + 1
        prevGuess = nextGuess
    
    if verbose: 
        if num_guesses > 6: print(colored('Guess max (6) exceded', 'red'))
        strout = 'correct word: '+ game.correct_word + ' found in ' + str(num_guesses) + ' guesses!'
        print(colored(strout, 'green'))
    
    return num_guesses


words_list = get_word_list("data/words-guess.txt")

if __name__ == '__main__':

    wordle = Wordle(words_list)

    play_game(wordle, 'tares')