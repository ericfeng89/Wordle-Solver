
import random
from wordle_naive import Wordle, words_list
import matplotlib.pyplot as plt

# number of test puzzles to validate on
# max is 674 previous wordle answers, takes about 2 min
TEST_SIZE = 100


# function to retrieve words for testing from a txt file
# previous_answers sourced from https://www.rockpapershotgun.com/wordle-past-answers 
def get_test_words():
    for line in open('data/previous_answers.txt'):
        mylist = line.split(' ')

    testWords = []
    for word in mylist:
        testWords.append(word.lower())

    # shuffle the test set
    random.shuffle(testWords)

    # these are not included in our other datasets
    testWords.remove('snafu')
    testWords.remove('guano')
    
    return testWords[:TEST_SIZE]      # 674 total
testwords = get_test_words()

# run all testwords given start word seed
# displays progress bar if verbose=true (default)
def run_test(seed, verbose=True, heuristic='naive'):
    #testwords = get_test_words()

    if verbose: print('Testing wordle bot on ', len(testwords), ' previous wordle answers with starting guess: ', seed)

    guess_log = []
    for i, ans in enumerate(testwords):

        # Print the progress bar
        progress = i / (len(testwords) - 1)
        num_bars = int(progress * 40)
        if verbose: print('\r[{}{}] {}/{}'.format('#' * num_bars, '-' * (40 - num_bars), i+1, len(testwords)), end='')

        game = Wordle(words_list, correct_word=ans)
        # note: startword is standardized to control testing
        guess_log.append(game.play_game(startword=seed, verbose=False, heuristic=heuristic))
        if guess_log[len(guess_log) - 1] > 6: print('\t failure for word {}'.format(ans))
        
    plot_guess_log(seed + '_' + heuristic, guess_log)

    avg_guesses = sum(guess_log)/ len(guess_log)

    if verbose: print("\naverage number of guesses for starting word {} is: {:.3f}".format(seed, avg_guesses))

    return avg_guesses

def plot_guess_log(seed, guess_log):
    fig, ax = plt.subplots()
    ax.set_xlabel('Number until correct for starting word ' + seed)
    ax.set_ylabel('Frequency of number of guesses')
    ax.hist(guess_log, bins=range(10), linewidth=0.5, edgecolor="white")

    mean_guesses = sum(guess_log)/len(guess_log)
    plt.axvline(x=mean_guesses, color='r', linestyle='--')

    plt.text(mean_guesses+0.1, 0.9*ax.get_ylim()[1], 'Mean: {:.2f}'.format(mean_guesses), color='r', fontsize=14)


    plt.savefig('histograms/'+ seed + '.png')

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
    
    # add other starting words you want to assess to this list
    popular_start_words = ['raise']
    avg_guesses = []
    
    for seed in popular_start_words:
        print('testing: \t', seed)
        # try for each heuristic
        ### NOTE: second try of entropy does not work for some reason
        for h in ['two_word']:
            avg = run_test(seed, verbose=True, heuristic=h)
            print('\navg guesses for ', h, ': \t', avg)
        
        avg_guesses.append(avg)
    
    # can use below to display plt plots to compare starting words
    # plot_start_words(popular_start_words, avg_guesses)

    
    