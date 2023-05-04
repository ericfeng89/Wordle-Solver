from queue import PriorityQueue
from wordle_information_theory import get_expected_entropy, choose_word

def get_word_list(filename):
   words = []
   with open(filename, "r", encoding="UTF-8") as in_file:
           for line in in_file:
               words.append(line.strip())
   return words

words_list = get_word_list("data/words-guess.txt")


# # works for every word
# def two_word_strategy_best(possible_words, num_guesses_made, guesses_made):
#     if len(possible_words) == 1:
#         return possible_words[0]
#     # count different letters left
#     firstGuess = possible_words[0]
#     maxNumDiff = 0
#     diff_let_internal = list()
#     for word in possible_words:
#         numDiff = 0
#         for i in range(5):
#             if word[i] != firstGuess[i]:
#                 diff_let_internal.append(word[i])
#                 numDiff = numDiff + 1
#         if numDiff > maxNumDiff:
#             maxNumDiff = numDiff

#     overlap = 0
#     for letter in diff_let_internal:
#         if letter in firstGuess:
#             overlap += 1
    
#     if overlap == len(diff_let_internal):
#         maxNumDiff = 0

#     if (maxNumDiff == 1 or maxNumDiff == 2) and num_guesses_made < 6:
#         word_choice = PriorityQueue()
#         # start with arbitrarily choosing only one letter different bc I am scared and confused
#         # ['light', 'night', 'might', 'fight', 'tight']
#         # find the word that uses the most of these different letters
#         differentLetters = list()
#         for word in possible_words:
#             for i in range(5):
#                 if word[i] != firstGuess[i]:
#                     differentLetters.append(word[i])

#         secGuess = possible_words[1]
#         for i in range(5):
#             if secGuess[i] != firstGuess[i]:
#                 differentLetters.append(firstGuess[i])
#         #ok obvi this is really ugly but we have the different letters
#         # now find any word that maximizes these letters
#         # lets store the words as a pqueue because I am a pretentious asshole
#         reallyDifferentLetters = list()
#         for letter in differentLetters:
#             for word in possible_words:
#                 if letter not in word:
#                     reallyDifferentLetters.append(letter)
#         for word in words_list:
#             numDiff = 0
#             for i in range(len(reallyDifferentLetters)):
#                 if reallyDifferentLetters[i] in word:
#                     numDiff = numDiff + 1

#             word_choice.put((- numDiff, word))

#         return word_choice.get()[1]

#     elif num_guesses_made < 3:
#         used_letters = list()
#         for guess in guesses_made:
#             for letter in guess:
#                 used_letters.append(letter)

#         differentletters = words_list[:]
#         for word in words_list:
#             for letter in used_letters:
#                 if letter in word:
#                     differentletters.remove(word)
#                     break
        
#         entropy_order = PriorityQueue()
#         for word in differentletters:
#             entropy_order.put((-(get_expected_entropy(word, differentletters)), word))
#         if not entropy_order.empty():
#             return entropy_order.get()[1]

#     else: return choose_best_hybrid(possible_words, num_guesses_made)



def unique_letters_left(possible_words):
    # count different letters left
    firstGuess = possible_words[0]
    maxNumDiff = 0
    diff_let_internal = list()
    for word in possible_words:
        numDiff = 0
        for i in range(5):
            if word[i] != firstGuess[i]:
                diff_let_internal.append(word[i])
                numDiff = numDiff + 1
        if numDiff > maxNumDiff:
            maxNumDiff = numDiff

    # if the different letters occur in other places in the word they don't really help us
    overlap = 0
    for letter in diff_let_internal:
        if letter in firstGuess:
            overlap += 1
    
    if overlap == len(diff_let_internal):
        maxNumDiff = 0

    return maxNumDiff

# works for every word time to make it better
def two_word_strategy(possible_words, num_guesses_made, guesses_made):
    # only one option
    if len(possible_words) == 1:
        return possible_words[0]
    
    maxNumDiff = unique_letters_left(possible_words)
    if (maxNumDiff == 1 or maxNumDiff == 2) and (num_guesses_made < 6 or len(possible_words) < 6):
        firstGuess = possible_words[0]
        word_choice = PriorityQueue()
        # find the word that uses the most of these different letters
        differentLetters = list()
        for word in possible_words:
            for i in range(5):
                if word[i] != firstGuess[i]:
                    differentLetters.append(word[i])
        # because we missed the first word in the above loop
        for letter in firstGuess: differentLetters.append(letter)
        # makes sure we only have unique letters (inspired by parer vs paper issue i ran into)
        reallyDifferentLetters = list()
        for letter in differentLetters:
            for word in possible_words:
                if letter not in word:
                    reallyDifferentLetters.append(letter)
        # now find any word that maximizes these letters
        for word in words_list:
            numDiff = 0
            for i in range(len(reallyDifferentLetters)):
                if reallyDifferentLetters[i] in word:
                    numDiff = numDiff + 1
            word_choice.put((- numDiff, word))
        # return the word that will maximize the unique letters because this will tell us the most about the remaining words
        return word_choice.get()[1]
    elif num_guesses_made < 3:
        # less than 3 guesses and not a lot of overlap between words? then choose a word with no 
        #   crossover to any letters in a previously guessed word. Eliminates the most words. 
        used_letters = list()
        for guess in guesses_made:
            for letter in guess:
                used_letters.append(letter)
        # collect letters not used in previous guesses
        not_used_letters = words_list[:]
        for word in words_list:
            for letter in used_letters:
                if letter in word:
                    not_used_letters.remove(word)
                    break
        # get word with not yet used letters that maximizes entropy
        entropy_order = PriorityQueue()
        for word in not_used_letters:
            entropy_order.put((-(get_expected_entropy(word, not_used_letters)), word))
        if not entropy_order.empty():
            return entropy_order.get()[1]

    else: 
        return choose_word(possible_words, verbose=False)




