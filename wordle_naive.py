import random


### Taken from the github repo
class Wordle:
   ''' Class representing one wordle game.
   methods include initiating a secret word,
   returning green/yellow/grey results,
   keeping track of guessed letters
   '''


   def __init__(self, words_list, correct_word=None):
       # the word to guess
       self.correct_word = random.choice(words_list)


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



def naive_filter(validGuesses, results, lastGuess):
   greyFails = list()
   for i in range(5):
       if results[i] == '_':
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
       if results[i] == 'Y':
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
       if results[i] == 'G':
           # this location should be this letter
           for guess in yellowGuesses:
               if guess[i] != lastGuess[i]:
                   greenFails.append(guess)
  
   greenFilter = list()
   for guess in yellowGuesses:
       if guess not in greenFails:
           greenFilter.append(guess)


   return greenFilter




def get_word_list(filename):
   words = []
   with open(filename, "r", encoding="UTF-8") as in_file:
           for line in in_file:
               words.append(line.strip())
   return words


words_list = get_word_list("words-guess.txt")

wordle = Wordle(words_list)

wordle.guess('tares')

prevGuess = 'tares'


i = 1
while(not (wordle.guess(prevGuess))):
   nextGuess = random.choice(naive_filter(words_list, wordle.results[i], prevGuess))
   i = i + 1
   prevGuess = nextGuess




print(wordle.guesses)
print(wordle.results)


print(wordle.correct_word)