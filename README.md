# Wordle-Solver
AI final project

Jackson Shelby, Hannah Storrey, Eric Feng

# Introduction
Wordle is a popular online word guessing game run by the New York Times where players have six attempts to guess a secret five-letter word. The game generates a new random word each round and provides feedback to the player after each guess, indicating which letters are correct and in the right position, and which letters are correct but in the wrong position. The objective of the game is to correctly guess the word within the six attempts provided.

Check out our full write up [HERE](https://docs.google.com/document/d/1h1wElxB7cFXHBVClR7XuDQ84xGeL8lNWLZu6ATLVGYg/edit?usp=sharing)

# Instructions
1. clone the repository to your machine
2. ensure all dependencies are downloaded in requirements.txt
3. To run a wordle game:
    - navigate to wordle_naive.py and scroll to main function
    -  set desired startword
    -  set desired solution word (set as None for random)
    -  run wordle_naive and view output in the terminal window
4. To view the test suite:
    -  navigate to wordle_test.py
    -  choose size of test set in TEST_SIZE variable (max 674)
    -  set list of start words and heuristics which you want to evaluate
    -  run wordle_test to view progress bars, and produce performance plots

# Development
 1. retrieve collections of all possible words
 - List of possible words: https://github.com/tabatkins/wordle-list 
 - Word frequency dataset: https://www.kaggle.com/datasets/rtatman/english-word-frequency?resource=download
 
 2. Design an interface through which heuristics can be implemented and tested
 - inspiration from: https://github.com/gamescomputersplay/wordle
 
 3. Implement naive wordle solver
 
      a.) naïve solver: random choice from possible words
  
      b.) Rank by word frequency (how common words are)
  
      c.) Make min Entropy choice which cuts the search space the most
  
 4. Identify the ideal starting word for each solver
 5. Create visualizations for model performance
