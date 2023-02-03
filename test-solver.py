import copy

txt = open("Word Lists/Words.txt", 'r')
words = [line.strip('\n') for line in txt.readlines()]
txt.close()


def best_guess(word_list, v=6.0, r=20.0, f=1.0):
    p_guesses = []
    for i in range(len(word_list)):
        w = weightings(word_list[i], v, r, f)
        p_guesses.append([w, word_list[i]])

    p_guesses.sort(reverse=True)
    return p_guesses[0][1]


def weightings(word, v=6.0, r=20.0, f=1.0):
    word_weight = 0.0
    vowels = ['a', 'e', 'i', 'o', 'u']
    freq = {'e': 56.88, 'a': 43.31, 'r': 38.64, 'i': 38.45, 'o': 36.51, 't': 35.43, 'n': 33.92, 's': 29.23,
            'l': 27.98, 'c': 23.13, 'u': 18.51, 'd': 17.25, 'p': 16.14, 'm': 15.36, 'h': 15.31, 'g': 12.59,
            'b': 10.56, 'f': 9.24, 'y': 9.06, 'w': 6.57, 'k': 5.61, 'v': 5.13, 'x': 1.48, 'z': 1.39,
            'j': 1.0, 'q': 1.0}

    for vowel in vowels:
        if word.count(vowel) > 0:
            word_weight += v

    for i in range(5):
        word_weight += repeats(word.count(word[i]), r) + (f * freq[word[i]])

    return word_weight


def repeats(num, modifier):
    return modifier * (-1 * (num - 1) ** 2 + 1)


def next_word(information, prev_guess, game_round, words, vowels=6.0, repeat=20.0, frequency=1.0):
    guess = prev_guess

    if game_round == 0:
        guess = best_guess(words, vowels, repeat, frequency)
    else:
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
                                    print(word, 1)
                                    words.remove(word)
                                    removed = True
                                    break

                    if word.count(req[0]) < req[3] and not removed:
                        print(word, 2)
                        words.remove(word)
                        break

                    if not all([x is None for x in req[2]]) and not removed:
                        for not_pos in req[2]:
                            if not_pos is not None:
                                if word[not_pos] == req[0]:
                                    print(word, 3)
                                    words.remove(word)
                                    removed = True
                                    break
                else:
                    if req[0] in word and not removed:
                        print(word, 4)
                        words.remove(word)
                        break

        guess = best_guess(words, vowels, repeat, frequency)

    return guess, words


"""def other_next_word(information, prev_guess, round, words, vowels=6.0, repeat=20.0, frequency=1.0):
    guess = prev_guess

    if round == 0:
        guess = best_guess(words, vowels, repeat, frequency)
    else:
        if all([x == 1 for x in information]):
            return guess, words

        for x in range(5):
            for y in range(len(words)):
                if guess[x] in words[0] and information[x] == 0:
                    if not (guess[x] in guess[:x] or guess[x] in guess[x + 1:]):
                        words.pop(0)
                    else:
                        zero_equal_letter = 0
                        for a in range(5):
                            if information[a] == 0 and guess[a] == guess[x]:
                                zero_equal_letter += 1

                        if words[0].count(guess[x]) > guess.count(guess[x]) - zero_equal_letter:
                            words.pop(0)
                        else:
                            words.append(words[0])
                            words.pop(0)

                elif (guess[x] not in words[0] or guess[x] == words[0][x]) and information[x] == -1:
                    words.pop(0)
                elif guess[x] != words[0][x] and information[x] == 1:
                    words.pop(0)
                else:
                    words.append(words[0])
                    words.pop(0)

        guess = best_guess(words, vowels, repeat, frequency)

    return guess, words""" # OLD SOLVER