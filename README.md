# Wordle-Solver-AI

This is a program that trains itself to beat https://www.wordleunlimited.com/ as consistently as possible.

It uses a basic stratagy and chooses guesses base on several factors:
1. The information provided by previous guesses
2. How many unique letters are in the guess
3. How many vowels are in the guess
4. The frequency of each letter in the guess

It applies a weight to each of those factors, the only exception being (1.), which is absolute.
Then it gives each possible guess a score and picks the one with the highest score.

It starts with some base parameters and adjusts those over time. It does this by:
1. Playing 200 games
2. Calculating its average winrate and associating that winrate with its current set of parameters
3. Sightly adjusting the parameters
4. Repeat

Once it's done that about 12 times, it takes the best parameters, keeps them, and repeats.

Additional Notes:
1. The AI requires the chromedriver to open and access the wordle unlimited website to train.
2. The AI scrapes the https://www.wordleunlimited.com/ website to find the necessary information.
      - Some websites don't allow this, but https://www.wordleunlimited.com/ does
      - You can verfiy this on this site: https://www.wordleunlimited.com/robots.txt
3. There are two programs, AI and Solver. 
      - The AI trains the parameters using https://www.wordleunlimited.com/
      - The Solver takes manual input for use and testing in https://www.nytimes.com/games/wordle/index.html
4. The AI uses simulated key presses to enter things into the wordle, so tabbing out will let the AI loose
5. If the solution is not in the AIs word list (Words.txt), the AI will type "blank" until it loses to indicate that
      - In this case, the loss will not count against (or for) its win rate
 

