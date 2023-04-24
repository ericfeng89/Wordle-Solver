# download word frequency dataset from here into repo subdirectory named "/data" and unzip
# https://www.kaggle.com/datasets/rtatman/english-word-frequency?resource=download

import pandas as pd

# replace this by importing from other file once the dash is removed from filename
def get_word_list(filename):
    words = []
    with open(filename, "r", encoding="UTF-8") as in_file:
            for line in in_file:
                words.append(line.strip())
    return words
words_list = get_word_list("words-guess.txt")

def get_frequency_data():
    dataset = pd.read_csv('data/unigram_freq.csv')
    # filter for words of length 5 and in our words_list
    def filter_5(row):
        return len(row['word']) == 5 and row['word'] in words_list
    dataset['word'] = dataset['word'].astype(str)
    m = dataset.apply(filter_5, axis=1)
    dataset = dataset[m]
    dataset.sort_values(by=['count'])
    # return the first 10K sorted by frequency
    return dataset.reset_index(drop=True)


freq_data = get_frequency_data()

# writing the filtered csv to the data folder so we don't need to repeat process
freq_data.to_csv("data/filtered_freq_data.csv", index=False)