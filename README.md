# Wordle-Solver-AI

This is a program that trains itself to beat wordles as consistently as possible or as quickly as possible.

It uses a basic stratagy and chooses guesses base on these factors:
1. The information provided by previous guesses
2. How many unique letters are in the guess
3. How many vowels are in the guess
4. The frequency of each letter in the guess

It applies a weight to each of those factors, the only exception being #1, which is absolute.
Then it gives each possible guess a score and picks the one with the highest score.

It starts with some base parameters and adjusts those over time. It does this by:
1. Playing 2000-15000 words (based on the chosen word list)
2. Calculating its average winrate/ rounds per game and associating that with its current set of parameters
3. Sightly adjusting the parameters
4. Repeat

Once it's done that, it will repeat with sightly adjusted parameters until it's tested every set, then choose the best set and repeat for however long it was set.
