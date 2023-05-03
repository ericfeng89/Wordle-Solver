# ok forget about that two word thing bc I don't know what's really going on there but here we will try the partial entropy partial frequency stuff
from wordle_information_theory import get_expected_entropy, choose_word
from wordle_frequency import FREQ_DICT, get_highest_frequency_word
from sklearn import preprocessing # this was for normalizing data but that doesn't seem to be the best
from queue import PriorityQueue

MAX_WORDLE = 6

def choose_best_hybrid(wordlist, num_results):
    # so we are out performing frequency but not entropy
    # alt plan, get the words with the top 5 highest entropy, choose the most freq of that list?
    if num_results < 4:
        return choose_word(wordlist, verbose=False)
    else:
        # return get_highest_frequency_word(wordlist)
        entropy_order = PriorityQueue()

        for word in wordlist:
            entropy_order.put((-(get_expected_entropy(word, wordlist)), word))
        
        # so that is the list of words based on entropy, just take top 5 (arbitrary) and return most popular
        # instead of 5, say if entropy differs by more than 0.3
        best_entry = entropy_order.get()
        best_word = best_entry[1]
        best_freq = FREQ_DICT[best_word]

        for i in range(entropy_order.qsize()):
            next_entry = entropy_order.get()
            if best_entry[0] - next_entry[0] > 0.3 :
                return best_word
            else:
                next_word = next_entry[1]
                next_freq = FREQ_DICT[next_word]
                if next_freq > best_freq:
                    best_word = next_word
                    best_freq = next_freq

        if entropy_order.qsize() > 5:
            num_compare = 5
        else:
            num_compare = entropy_order.qsize()
        for i in range(num_compare):
            word = entropy_order.get()
            word_freq = FREQ_DICT[word[1]]
            print(word)
            if word_freq > best_freq:
                best_word = word[1]
                best_freq = word_freq
        
        return best_word

