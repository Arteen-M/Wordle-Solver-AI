import solver
import generator
import copy

config = open("config.txt", 'r')
config_lines = config.readlines()

for x in range(0, len(config_lines)):
    config_lines[x] = config_lines[x].strip('\n')

if config_lines[0] == "long":
    word_list = "Words.txt"
elif config_lines[0] == "short":
    word_list = "Word Shortlist.txt"
else:
    word_list = "Tested Words.txt"

#  Open the word list
txt = open("Word Lists/" + word_list, 'r')
words = [line.strip('\n') for line in txt.readlines()]
txt.close()


def wordle(word, vowels, repeat, freq, max_rounds=6, p=False):
    # print(new)
    # Start with no information
    info = []
    guess = ""

    # Start with a list of all the words in its word bank
    new_words = copy.deepcopy(words)

    # For an N number of rounds
    if max_rounds == 'inf':
        rounds = 0
        while True:
            guess, new_words = solver.next_word(info, guess, rounds, new_words, vowels, repeat, freq)
            # print("\t" + guess)

            # Get the info based on the current guess
            info = generator.information(word, guess)
            # print(guess, info)
            # IF the guess is correct, break and return the rounds it took
            if guess == word:
                # print("Solved %s in %d rounds!" % (word, r+1))
                return rounds + 1

            rounds += 1
    else:
        for r in range(max_rounds):
            # Generate a guess and a list of new words based on previous information
            guess, new_words = solver.next_word(info, guess, r, new_words, vowels, repeat, freq)

            # Get the info based on the current guess
            info = generator.information(word, guess)
            if p:
                print(guess, info)
            # IF the guess is correct, break and return the rounds it took
            if guess == word:
                if p:
                    print("Solved %s in %d rounds!" % (word, r+1))
                return r+1

    # print("Failed to solve " + word)
    # If the code gets here, it means it failed to solve in 6 rounds, so return None to indicate a failure
    return None

