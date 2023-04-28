# this is me trying to start on the two word tactics
import string
import random
# from wordle_naive import words_list
from queue import PriorityQueue
  
q = PriorityQueue()

alphabet = list(string.ascii_lowercase)

def get_word_list(filename):
   words = []
   with open(filename, "r", encoding="UTF-8") as in_file:
           for line in in_file:
               words.append(line.strip())
   return words

words_list = get_word_list("data/words-guess.txt")


def two_word_strategy(possible_words):
    # first, should we use a two word strategy
        # if no, second, which two words are that strategy. return two words
        # else if yes, second, return one word

    # should find out how different each of the remaining words are
    firstGuess = possible_words[0]
    maxNumDiff = 0
    for word in possible_words:
        numDiff = 0
        for i in range(5):
            if word[i] != firstGuess[i]:
                numDiff = numDiff + 1
        if numDiff > maxNumDiff:
            maxNumDiff = numDiff

    if maxNumDiff == 1:
        # start with arbitrarily choosing only one letter different bc I am scared and confused
        # ['light', 'night', 'might', 'fight', 'tight']
        # find the word that uses the most of these different letters
        differentLetters = ""
        for word in possible_words:
            for i in range(5):
                if word[i] != firstGuess[i]:
                    differentLetters += word[i]

        secGuess = possible_words[1]
        for i in range(5):
            if secGuess[i] != firstGuess[i]:
                differentLetters += firstGuess[i]
        #ok obvi this is really ugly but we have the different letters
        # now find any word that maximizes these letters
        # lets store the words as a pqueue because I am a pretentious asshole
        for word in words_list:
            numDiff = 0
            for i in range(len(differentLetters)):
                if differentLetters[i] in word:
                    numDiff = numDiff + 1

            q.put((len(differentLetters) - numDiff, word))

        return q.get()[1]

    return random.choice(possible_words)