# Wordle-Solver
AI final project

Jackson Shelby, Hannah Storrey, Eric Feng

# Introduction
Wordle is a popular online word guessing game run by the New York Times where players have six attempts to guess a secret five-letter word. The game generates a new random word each round and provides feedback to the player after each guess, indicating which letters are correct and in the right position, and which letters are correct but in the wrong position. The objective of the game is to correctly guess the word within the six attempts provided.

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
 6. Develop clean UI for users to play
