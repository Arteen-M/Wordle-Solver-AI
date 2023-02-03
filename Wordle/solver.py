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

txt = open("Word Lists/" + word_list, 'r')
words = [line.strip('\n') for line in txt.readlines()]
words_2 = copy.deepcopy(words)
txt.close()


# Giving a list of words, determine a weight of each one and sort it to put the best guess first
# The best guess is the word with the largest score
def best_guess(word_list, game_round, v=6.0, r=20.0, f=1.0):
    p_guesses = []

    freq = mod_freq(word_list)
    #if game_round == 0:
    #    freq = {'e': 9.120831528800347, 'a': 7.847553053269814, 'r': 7.232568211346904, 'i': 5.59549588566479, 'o': 5.820701602425292, 't': 5.77739281074058, 'n': 4.7466435686444335, 's': 5.34430489389346, 'l': 5.5868341273278475, 'c': 3.86314421827631, 'u': 3.949761801645734, 'd': 3.2048505846686877, 'p': 2.9883066262451283, 'm': 2.581203984408835, 'h': 3.2654828930272846, 'g': 2.5898657427457774, 'b': 2.304027717626678, 'f': 1.7843222174101343, 'y': 3.603291468168038, 'w': 1.6717193590298831, 'k': 1.7496751840623646, 'v': 1.281940233867475, 'x': 0.32048505846686876, 'z': 0.303161541792984, 'j': 0.23386747509744477, 'q': 0.2511909917713296}
    #else:
    #    freq = mod_freq(word_list)

    # For every word
    for i in range(len(word_list)):
        # Find a weight
        w = weightings(word_list[i], freq, v, r, f)
        p_guesses.append([w, word_list[i]])

    # Sort each word by weight
    p_guesses.sort(reverse=True)
    # Return the word with the highest weight
    try:
        return p_guesses[0][1]
    except IndexError:
        return None


# Determine the weight/ score of a word
def weightings(word, freq, v=6.0, r=20.0, f=1.0):
    word_weight = 0.0  # Starting value of 0
    vowels = ['a', 'e', 'i', 'o', 'u']  # List of vowels

    # Dictionary of the frequency of each letter in the english langauge
    # This is ignoring the frequency of word use, and is found from an analysis of the Concise Oxford dictionary
    # https://web.archive.org/web/20111224230632/http://oxforddictionaries.com/words/what-is-the-frequency-of-the-letters-of-the-alphabet-in-english
    # Above is the source for the information
    # {'e': 56.88, 'a': 43.31, 'r': 38.64, 'i': 38.45, 'o': 36.51, 't': 35.43, 'n': 33.92, 's': 29.23,
    # 'l': 27.98, 'c': 23.13, 'u': 18.51, 'd': 17.25, 'p': 16.14, 'm': 15.36, 'h': 15.31, 'g': 12.59,
    # 'b': 10.56, 'f': 9.24, 'y': 9.06, 'w': 6.57, 'k': 5.61, 'v': 5.13, 'x': 1.48, 'z': 1.39,
    # 'j': 1.0, 'q': 1.0}

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


def mod_freq(lst):
    total_letters = 0
    freq_dict = {'e': 0, 'a': 0, 'r': 0, 'i': 0, 'o': 0, 't': 0, 'n': 0, 's': 0,
                 'l': 0, 'c': 0, 'u': 0, 'd': 0, 'p': 0, 'm': 0, 'h': 0, 'g': 0,
                 'b': 0, 'f': 0, 'y': 0, 'w': 0, 'k': 0, 'v': 0, 'x': 0, 'z': 0,
                 'j': 0, 'q': 0}
    for word in lst:
        total_letters += 5
        for letter in word:
            freq_dict[letter] += 1 / word.count(letter)

    for letter in freq_dict:
        freq_dict[letter] /= (total_letters / 100)

    # print(freq_dict)
    return freq_dict


def next_word(information, prev_guess, game_round, words, vowels=6.2, repeat=20.0, frequency=1.0):
    guess = prev_guess

    # If it's the first round, guess without information
    if game_round == 0:
        guess = best_guess(words, game_round, vowels, repeat, frequency)
    else:
        # If the information returns 1 1 1 1 1, you already have the right word
        if all([x == 1 for x in information]):
            return guess, words

        requirements = []
        all_letters = []

        for count, letter in enumerate(prev_guess):
            all_letters.append(letter)
            position = 'Zero'
            prev_position = None
            number_of_letter = 0

            if information[count] == 1:
                position = count
                number_of_letter += 1
            elif information[count] == -1:
                position = 'Neg'
                prev_position = count
                number_of_letter += 1
            else:
                prev_position = count

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
                    if not all([isinstance(x, str) for x in req[1]]) and not removed:
                        for position in req[1]:
                            if not isinstance(position, str):
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

        guess = best_guess(words, game_round, vowels, repeat, frequency)

    # print(guess)

    return guess, words

# print(next_word([0, 0, -1, 0, -1], 'irate', 1, words_2, 4.8, 26.0, 0.8))
# print(next_word([-1, -1, 0, 0, 1], 'aeons', 1, words_2, 4.8, 26.0, 0.8))
# print(next_word([0, 1, 0, 1, 1], 'laces', 1, words_2, 4.8, 26.0, 0.8))
# print(next_word([0, 1, 0, 1, 1], 'dames', 1, words_2, 4.8, 26.0, 0.8))
# print(next_word([0, 1, 0, 1, 1], 'pages', 1, words_2, 4.8, 26.0, 0.8))
# print(next_word([0, 1, 0, 1, 1], 'haves', 1, words_2, 4.8, 26.0, 0.8))
# print(next_word([1, 1, 0, 1, 1], 'bakes', 1, words_2, 4.8, 26.0, 0.8))
# print(next_word([1, 1, 0, 1, 1], 'bases', 1, words_2, 4.8, 26.0, 0.8))
