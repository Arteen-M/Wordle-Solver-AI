p = open("../Wordle/Parameters.txt", 'r')
parameters = p.readline().split()

for i in range(len(parameters)):
    parameters[i] = float(parameters[i].strip(','))

p.close()

vowels = parameters[0]
repeat = parameters[1]
frequency = parameters[2]


def best_guess(word_list, v=6, r=20, f=1):
    p_guesses = []
    for i in range(len(word_list)):
        w = weightings(word_list[i], v, r, f)
        p_guesses.append([w, word_list[i]])

    p_guesses.sort(reverse=True)
    return p_guesses[0][1]


def weightings(word, v=6, r=20, f=1):
    word_weight = 0
    vowels = ['a', 'e', 'i', 'o', 'u']
    freq = {'e': 56.88, 'a': 43.31, 'r': 38.64, 'i': 38.45, 'o': 36.51, 't': 35.43, 'n': 33.92, 's': 29.23,
            'l': 27.98, 'c': 23.13, 'u': 18.51, 'd': 17.25, 'p': 16.14, 'm': 15.36, 'h': 15.31, 'g': 12.59,
            'b': 10.56, 'f': 9.24, 'y': 9.06, 'w': 6.57, 'k': 5.61, 'v': 5.13, 'x': 1.48, 'z': 1.39,
            'j': 1, 'q': 1}

    for vowel in vowels:
        if word.count(vowel) > 0:
            word_weight += v

    for i in range(5):
        word_weight += repeats(word.count(word[i]), r) + (f * freq[word[i]])

    return word_weight


def repeats(num, modifier):
    return modifier * (-1 * (num - 1) ** 2 + 1)


txt = open("Words.txt", 'r')
words = [line.strip('\n') for line in txt.readlines()]

information = []
guess = []
potential_guesses = []
weight = 0

while True:
    if not guess:
        guess = best_guess(words, vowels, repeat, frequency)
    else:
        information = input("Enter Information from last guess (0, 1, -1): ").split()
        for x in range(5):
            for y in range(len(words)):
                if guess[x] in words[0] and information[x] == '0':
                    if not (guess[x] in guess[:x] or guess[x] in guess[x + 1:]):
                        words.pop(0)
                    else:
                        zero_equal_letter = 0
                        for a in range(5):
                            if information[a] == '0' and guess[a] == guess[x]:
                                zero_equal_letter += 1

                        if words[0].count(guess[x]) > guess.count(guess[x]) - zero_equal_letter:
                            words.pop(0)
                        else:
                            words.append(words[0])
                            words.pop(0)

                elif (guess[x] not in words[0] or guess[x] == words[0][x]) and information[x] == '-1':
                    words.pop(0)
                elif guess[x] != words[0][x] and information[x] == '1':
                    words.pop(0)
                else:
                    words.append(words[0])
                    words.pop(0)

        guess = best_guess(words, vowels, repeat, frequency)

    print('Guess %s' % str(guess))



