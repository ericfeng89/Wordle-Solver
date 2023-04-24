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


def get_word_list(filename):
    words = []
    with open(filename, "r", encoding="UTF-8") as in_file:
            for line in in_file:
                words.append(line.strip())
    return words

words_list = get_word_list("words-guess.txt")

wordle = Wordle(words_list)

wordle.guess('tares')
print(wordle.guesses)
print(wordle.results)
print(wordle.correct_word)