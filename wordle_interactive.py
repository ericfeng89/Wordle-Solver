from wordle_naive import *

class Wordle_Interactive(Wordle):

    # override
    def play_game(self, startword=None, verbose=True, heuristic=None):
        print('*****************************************************')
        print('            Welcome to the Wordle Solver!            ')
        print('*****************************************************')

        possible_words = words_list
        # guess returns true when word is found
        while(not self.guess()):
            #if verbose: print('RESULT: ', self.results[len(self.guesses) - 1])
            possible_words = self.naive_filter(possible_words)
            if verbose: print('POSSIBLE ANSWERS: (', str(len(possible_words)), ') ' , possible_words)

            naive_nextGuess = random.choice(possible_words)
            freq_nextGuess = get_highest_frequency_word(possible_words) # imported from wordle_frequency file
            entropy_nextGuess = choose_word(possible_words, verbose=False)   # imported from wordle_info_theory
            two_nextGuess = two_word_strategy(possible_words, len(self.results), self.guesses) # imported from two_word

            print("SOLVER RECOMMENDATIONS:")
            print("naive:\t\t", naive_nextGuess)
            print("frequency:\t", freq_nextGuess)
            print("entropy:\t", entropy_nextGuess)
            print("two word:\t", two_nextGuess, '\n')

        if verbose: 
            strout = 'correct word: '+ self.guesses[-1] + ' found in ' + str(len(self.guesses)) + ' guesses!'
            print(colored(strout, 'green'))

        return len(self.guesses)


    # override
    def guess(self):
        guess = self.get_guess()
        result = self.get_result()

        self.guesses.append(guess)
        self.results.append(result)
        # done when result is fully correct
        return result == 'GGGGG'



    # retrieve and validate guess
    def get_guess(self):
        guess = ''
        while True:
            if(len(self.guesses) == 0): print('Enter your starting word below, we recommend \'raise\'')
            else: print("Input your chosen guess below")
            guess = input('GUESS: \t')
            # add other validation here and break
            if len(guess) == 5 and guess in words_list: break

            print("invalid guess entry, try again")
        
        return guess

    def get_result(self):
        result = ''
        while True:
            print("Input your result from the last guess below, using chars G, Y, _")
            result = input('RESULT: ')
            # add other validation here and break
            if len(result) == 5: break

            print("invalid result entry, try again")
        
        return result
    

if __name__ == '__main__':
    game = Wordle_Interactive(words_list=words_list)
    game.play_game()