import copy

txt = open("Words.txt", 'r')
words = [line.strip('\n') for line in txt.readlines()]
txt.close()


# Giving a list of words, determine a weight of each one and sort it to put the best guess first
# The best guess is the word with the largest score
def best_guess(word_list, v=6.0, r=20.0, f=1.0):
    p_guesses = []
    # For every word
    for i in range(len(word_list)):
        # Find a weight
        w = weightings(word_list[i], v, r, f)
        p_guesses.append([w, word_list[i]])

    # Sort each word by weight
    p_guesses.sort(reverse=True)
    # Return the word with the highest weight
    return p_guesses[0][1]


# Determine the weight/ score of a word
def weightings(word, v=6.0, r=20.0, f=1.0):
    word_weight = 0.0  # Starting value of 0
    vowels = ['a', 'e', 'i', 'o', 'u']  # List of vowels

    # Dictionary of the frequency of each letter in the english langauge
    # This is ignoring the frequency of word use, and is found from an analysis of the Concise Oxford dictionary
    # https://web.archive.org/web/20111224230632/http://oxforddictionaries.com/words/what-is-the-frequency-of-the-letters-of-the-alphabet-in-english
    # Above is the source for the information
    freq = {'e': 56.88, 'a': 43.31, 'r': 38.64, 'i': 38.45, 'o': 36.51, 't': 35.43, 'n': 33.92, 's': 29.23,
            'l': 27.98, 'c': 23.13, 'u': 18.51, 'd': 17.25, 'p': 16.14, 'm': 15.36, 'h': 15.31, 'g': 12.59,
            'b': 10.56, 'f': 9.24, 'y': 9.06, 'w': 6.57, 'k': 5.61, 'v': 5.13, 'x': 1.48, 'z': 1.39,
            'j': 1.0, 'q': 1.0}

    # Add the vowel bonus (Only give 1 bonus per letter)
    for vowel in vowels:
        if word.count(vowel) > 0:
            word_weight += v

    # for each letter, apply a "repeats" bonus/ penalty
    for i in range(5):
        word_weight += repeats(word.count(word[i]), r) + (f * freq[word[i]])

    # Returns the appropriate weight/ score for the word
    return word_weight


def repeats(num, modifier):
    # This formula applies bonuses/ penalties like this:
    # If there are no repeats, apply a bonus of modifier
    # If there is one repeat, apply no bonus nor penalty
    # If there are two repeats, apply a penalty of -3 * modifier
    # Since this is a parabola, the penalty would get worse the more repeats there are,
    return modifier * (-1 * (num - 1) ** 2 + 1)


def next_word(information, prev_guess, game_round, words, vowels=6.2, repeat=20.0, frequency=1.0):
    guess = prev_guess

    # If it's the first round, guess without information
    if game_round == 0:
        guess = best_guess(words, vowels, repeat, frequency)
    else:
        # If the information returns 1 1 1 1 1, you already have the right word
        if all([x == 1 for x in information]):
            return guess, words

        requirements = []
        all_letters = []

        for count, letter in enumerate(prev_guess):
            all_letters.append(letter)
            position = None
            prev_position = None
            number_of_letter = 0

            if information[count] == 1:
                position = count
                number_of_letter += 1
            elif information[count] == -1:
                prev_position = count
                number_of_letter += 1

            mapped_letters = list(map(lambda x: x[0], requirements))
            if letter in mapped_letters:
                ind = mapped_letters.index(letter)
                requirements[ind][1].append(position)
                requirements[ind][2].append(prev_position)
                if information[count] != 0:
                    requirements[ind][3] += 1
            else:
                letter_info = [letter, [position], [prev_position], number_of_letter]
                requirements.append(letter_info)

        for word in copy.deepcopy(words):
            removed = False
            for req in requirements:
                if req[3] > 0:
                    if not all([x is None for x in req[1]]) and not removed:
                        for position in req[1]:
                            if position is not None:
                                if word[position] != req[0]:
                                    words.remove(word)
                                    removed = True
                                    break

                    if word.count(req[0]) < req[3] and not removed:
                        words.remove(word)
                        break

                    if not all([x is None for x in req[2]]) and not removed:
                        for not_pos in req[2]:
                            if not_pos is not None:
                                if word[not_pos] == req[0]:
                                    words.remove(word)
                                    removed = True
                                    break
                else:
                    if req[0] in word and not removed:
                        words.remove(word)
                        break

        guess = best_guess(words, vowels, repeat, frequency)

    # print(guess)

    return guess, words
