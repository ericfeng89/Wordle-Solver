
import random
from wordle_naive import Wordle, words_list
import matplotlib.pyplot as plt


# function to retrieve words for testing from a txt file
# previous_answers sourced from https://www.rockpapershotgun.com/wordle-past-answers 
def get_test_words():
    for line in open('data/previous_answers.txt'):
        mylist = line.split(' ')

    testWords = []
    for word in mylist:
        testWords.append(word.lower())

    # probably unnecessary considering all are used for avg calc
    random.shuffle(testWords)

    # idk why these are not included in our dataset...
    testWords.remove('snafu')
    testWords.remove('guano')
    
    return testWords[:100]

testwords = get_test_words()

# run all testwords given start word seed
# displays progress bar if verbose=true (default)
def run_test(seed, verbose=True):
    #testwords = get_test_words()

    if verbose: print('Testing wordle bot on ', len(testwords), ' previous wordle answers with starting guess: ', seed)

    guess_log = []
    for i, ans in enumerate(testwords):

        # Print the progress bar
        progress = i / (len(testwords) - 1)
        num_bars = int(progress * 40)
        if verbose: print('\r[{}{}] {}'.format('#' * num_bars, '-' * (40 - num_bars), i+1), end='')

        game = Wordle(words_list, correct_word=ans)
        # going to use start word "raise" as recommended here: https://www.tomsguide.com/news/best-wordle-start-words
        # note: startword is standardized to control testing
        guess_log.append(game.play_game(startword=seed, verbose=False))

    avg_guesses = sum(guess_log)/ len(guess_log)

    if verbose: print("\naverage number of guesses for starting word {} is: {:.3f}".format(seed, avg_guesses))

    return avg_guesses


def plot_start_words(start_words, avg_guesses):
    # Create a bar plot of the average guesses for each starting word
    fig, ax = plt.subplots()
    ax.bar(start_words, avg_guesses)
    ax.set_xlabel('Starting Word')
    ax.set_ylabel('Average Guesses')
    ax.set_title('Average Guesses for Different Starting Words')
    ax.set_ylim([0, 6])
    # Rotate the x-axis labels to improve readability
    plt.xticks(rotation=45)
    # Show the plot
    plt.show()

if __name__ == '__main__':

    popular_start_words = ['pzazz', 'risky', 'crate', 'fuzzy', 'raise']
    avg_guesses = []
    for seed in popular_start_words:
        print('testing: \t', seed)
        avg = run_test(seed, verbose=False)
        print('avg guesses: \t', avg)
        avg_guesses.append(avg)
    
    # plot_start_words(popular_start_words, avg_guesses)

    
    