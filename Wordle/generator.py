# Get the information in the EXACT same way the wordle website would.
# Its important that it's the exact same so that it can be used to solve actual wordles
def information(word, guess):
    info = []
    covered = []

    for count, letter in enumerate(guess):
        # If the letter is the exact same position
        if letter == word[count]:
            info.append(1)
            covered.append(letter)

        # If it isn't in at all
        elif letter not in word:
            info.append(0)
            covered.append(letter)

        # Otherwise, use None as a placeholder
        else:
            info.append(None)

    for count, element in enumerate(info):
        # If element is a placeholder, some letter hasn't been covered yet
        if element is None:
            # This code is to handle cases when the guess has repeat letters,
            # then how many -1s are placed in the info list
            # Say, for example, the word is knock, and the guess is kazoo, then info should be
            # [1, 0, 0, -1, 0], so one o is -1, and the other o is 0
            if word.count(guess[count]) <= covered.count(guess[count]):
                info[count] = 0
                covered.append(guess[count])
            else:
                info[count] = -1
                covered.append(guess[count])

    # Return the list of info
    return info
