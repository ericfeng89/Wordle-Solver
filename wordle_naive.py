import random
from termcolor import colored
from wordle_frequency import get_highest_frequency_word
from wordle_information_theory import choose_word
from two_word import two_word_strategy


### Source: gamescomputersplay (https://github.com/gamescomputersplay)
# The original wordle class is lifted from this repo, however
# significant changes have been made to every aspect of the class
# to support our functionality and design
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
   
   # returns a list of possible guesses, preserving information gained from previous
   # param validGuesses: list of possible words to choose from
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


    # play a wordle game with [heuristic] strat, given startword
    # returns i, the number of guesses to find the word
    # uses naive (random) word choice approach by default
    # set verbose to false for faster evaluation
   def play_game(self, startword, verbose=True, heuristic='naive'):
        if verbose: print('GUESSING: ', startword)
            
        prevGuess = startword
        # simulate one game
        possible_words = words_list
        while(not(self.guess(prevGuess))):
            if verbose: print('RESULT: ', self.results[len(self.guesses) - 1])
            possible_words = self.naive_filter(possible_words)
            if verbose: print('POSSIBLE ANSWERS: (', str(len(possible_words)), ') ' , possible_words)

            # here is where we choose the next word, based on the possible options
            nextGuess = ''
            if heuristic == 'frequency': nextGuess = get_highest_frequency_word(possible_words) # imported from wordle_frequency file
            elif heuristic == 'entropy': nextGuess = choose_word(possible_words, verbose=False)   # imported from wordle_info_theory
            elif heuristic == 'two_word': nextGuess = two_word_strategy(possible_words, len(self.results), self.guesses) # imported from two_word
            else: nextGuess = random.choice(possible_words)


            if verbose: print('GUESSING: ', nextGuess)
            prevGuess = nextGuess

        if verbose: 
            if len(self.guesses) > 6: print(colored('Guess max (6) exceded', 'red'))
            strout = 'correct word: '+ self.correct_word + ' found in ' + str(len(self.guesses)) + ' guesses!'
            print(colored(strout, 'green'))

        return len(self.guesses)



# fetches the word list from a given file
# can be used to load alternate word data, 
# like for n letters or all 5-letter words
def get_word_list(filename):
   words = []
   with open(filename, "r", encoding="UTF-8") as in_file:
           for line in in_file:
               words.append(line.strip())
   return words

# global to store word list (can be imported in others)
words_list = get_word_list("data/words-guess.txt")


'''
Run one or wordle game using each strategy
to evaluate on all three,  change 'solution'
to provide your own start, change 'startword'
'''
if __name__ == '__main__':

    startWord = 'raise'
    solution   = 'arrow'

    wordle = Wordle(words_list, correct_word=solution)
    wordle2 = Wordle(words_list, correct_word=wordle.correct_word)
    wordle3 = Wordle(words_list, correct_word=wordle.correct_word)
    wordle4 = Wordle(words_list, correct_word=wordle.correct_word)
    # cinch, catch, foyer, wooer, craze, parer, droll, chill, conic, jaunt
    print('correct word: ', wordle4.correct_word)

    num_guesses = wordle.play_game(startWord, verbose=False, heuristic='naive')
    num_guesses2 = wordle2.play_game(startWord, verbose=False, heuristic='frequency')
    num_guesses3 = wordle3.play_game(startWord, verbose=False, heuristic='entropy')
    num_guesses4 = wordle4.play_game(startWord, verbose=False, heuristic='two_word')

    print('Solved with naive heuristic in     ', num_guesses, ' guesses')
    print('solved with frequency heuristic in ', num_guesses2, ' guesses')
    print('solved with entropy heuristic in   ', num_guesses3, ' guesses')
    print('solved with two word heuristic in   ', num_guesses4, ' guesses')
