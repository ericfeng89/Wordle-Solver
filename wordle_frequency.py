# See notes on original data sourcing at the very bottom of this file

import pandas as pd

# param words_list: list of valid words to be checked against whin importing freq ds
def get_frequency_data(words_list):
    dataset = pd.read_csv('data/unigram_freq.csv')
    # filter for words of length 5 and in our words_list
    def filter_5(row):
        return len(row['word']) == 5 and row['word'] in words_list
    dataset['word'] = dataset['word'].astype(str)
    m = dataset.apply(filter_5, axis=1)
    dataset = dataset[m]
    dataset.sort_values(by=['count'])
    return dataset.reset_index(drop=True)

# this function can be called now that the data is already loaded into a csv
# returns a dictionary of {word: frequency}, where higher frequency means more common
def load_frequency_data():
    freq_data = pd.read_csv('data/filtered_freq_data.csv')
    freq_dict = dict(zip(freq_data['word'], freq_data['count']))
    # idk why this word isn't in the ds, adding to prevent error
    freq_dict['wooer'] = 10000
    return freq_dict

# takes in list of possible words, returns word of max frequency
def get_highest_frequency_word(wordlist):
    bestword = wordlist[0]
    bestfreq = -1
    for word in wordlist:
        if word not in FREQ_DICT: 
            print('ERROR: word ', word, 'not in frequency data')
            continue

        word_freq = FREQ_DICT[word]

        # if this word beats the best, choose this one
        if word_freq > bestfreq:
            bestfreq = word_freq
            bestword = word
    return bestword

# dictionary of {word: frequency}, where higher frequency means more common
FREQ_DICT = load_frequency_data()





################################################################################################
### THIS SHOULD NOT NEED TO BE RUN ON YOUR COMPUTER, IT IS JUST HERE TO PRODUCE THE CSV     ###
###                       "filtered_freq_data.csv"  WHICH IS INCLUDED IN THE REPO           ###
################################################################################################

# obsolete:
# download word frequency dataset from here into repo subdirectory named "/data" and unzip
# https://www.kaggle.com/datasets/rtatman/english-word-frequency?resource=download


# This code was originally used to create the csv file. Now that the csv is in the repo, we dont need to load
# from the whole dataset
'''
words_list = get_word_list("data/words-guess.txt")
# pandas dataframe with columns 'word', 'count', where higher counts mean more frequent words
freq_data = get_frequency_data(words_list)
# get dictionary of words mapped to their frequencies, can scale freq's here if necessary
freq_dict = dict(zip(freq_data['word'], freq_data['count']))
#print(freq_dict)
# maybe reference this var from other files ie: from wordle_frequency import freq_dict

# writing the filtered csv to the data folder so we don't need to repeat process
freq_data.to_csv("data/filtered_freq_data.csv", index=False)
'''