import solver
import generator
import copy

#  Open the word list
txt = open("Words.txt", 'r')
words = [line.strip('\n') for line in txt.readlines()]
txt.close()


def wordle(word, vowels, repeat, freq):
    # print(new)
    # Start with no information
    info = []
    guess = ""

    # Start with a list of all the words in its word bank
    new_words = copy.deepcopy(words)

    # For 6 rounds (Max)
    for r in range(6):
        # Generate a guess and a list of new words based on previous information
        guess, new_words = solver.next_word(info, guess, r, new_words, vowels, repeat, freq)

        # Get the info based on the current guess
        info = generator.information(word, guess)
        # print(guess, info)
        # IF the guess is correct, break and return the rounds it took
        if guess == word:
            # print("Solved %s in %d rounds!" % (word, r+1))
            return r+1

    # print("Failed to solve " + word)
    # If the code gets here, it means it failed to solve in 6 rounds, so return None to indicate a failure
    return None

