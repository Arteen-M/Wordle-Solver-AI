from selenium import webdriver
from bs4 import BeautifulSoup
from pynput.keyboard import Key, Controller
import random

keyboard = Controller()
driver = webdriver.Chrome("../Wordle/chromedriver_win32/chromedriver.exe")
driver.get('https://www.wordleunlimited.com/')
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

absent = []
elsewhere = []
present = []

p = open("../Wordle/Parameters.txt", 'r')
parameters = p.readline().split()

for i in range(len(parameters)):
    parameters[i] = float(parameters[i].strip(','))

p.close()


def best_guess(word_list, vowels=6, repeat=20, frequency=1):
    p_guesses = []
    for i in range(len(word_list)):
        w = weightings(word_list[i], vowels, repeat, frequency)
        p_guesses.append([w, word_list[i]])

    p_guesses.sort(reverse=True)
    return p_guesses[0][1]


def weightings(word, vowel_mod=6, repeat_mod=20, frequency_mod=1):
    word_weight = 0
    vowels = ['a', 'e', 'i', 'o', 'u']
    freq = {'e': 56.88, 'a': 43.31, 'r': 38.64, 'i': 38.45, 'o': 36.51, 't': 35.43, 'n': 33.92, 's': 29.23,
            'l': 27.98, 'c': 23.13, 'u': 18.51, 'd': 17.25, 'p': 16.14, 'm': 15.36, 'h': 15.31, 'g': 12.59,
            'b': 10.56, 'f': 9.24, 'y': 9.06, 'w': 6.57, 'k': 5.61, 'v': 5.13, 'x': 1.48, 'z': 1.39,
            'j': 1, 'q': 1}

    for vowel in vowels:
        if word.count(vowel) > 0:
            word_weight += vowel_mod

    for d in range(5):
        word_weight += repeats(word.count(word[d]), repeat_mod) + (frequency_mod * freq[word[d]])

    return word_weight


def repeats(num, modifier=20):
    return modifier * (-1 * (num - 1) ** 2 + 1)


def clear():
    global information
    global guess
    global txt
    global words
    global keyboard

    txt.close()
    information = []
    guess = []

    txt = open("Words.txt", 'r')
    words = [line.strip('\n') for line in txt.readlines()]


def argument_adjustment(rate, vowels=6, repeat=20, frequency=1):
    list_to_return = []
    v = vowels
    r = repeat
    f = frequency

    if rate > 90:
        list_to_return.append([v, r, f+0.1].copy())
        list_to_return.append([v, r, f-0.1].copy())
        list_to_return.append([v, r+0.1, f].copy())
        list_to_return.append([v, r-0.1, f].copy())
        list_to_return.append([v+0.1, r, f].copy())
        list_to_return.append([v-0.1, r, f].copy())

        list_to_return.append([v, r, f+1].copy())
        list_to_return.append([v, r, 0.1].copy())
        list_to_return.append([v, r+1, f].copy())
        list_to_return.append([v, r-1, f].copy())
        list_to_return.append([v+1, r, f].copy())
        list_to_return.append([v-1, r, f].copy())
    else:
        list_to_return = [random.uniform(1, 20), random.uniform(1, 50), random.uniform(0.1, 1.1)]

    return list_to_return


txt = open("Words.txt", 'r')
words = [line.strip('\n') for line in txt.readlines()]

information = []
guess = []
potential_guesses = []

test_args = [parameters]
all_args = []
current_args = test_args[0]

win_rate = 0

wins = 0
losses = 0

generation_number = 0

while True:
    generation_number += 1
    for it in range(len(test_args)):
        current_args = test_args[it]
        print(test_args[it], generation_number)
        while True:
            for b in range(6):
                if not guess:
                    guess = best_guess(words, current_args[0], current_args[1], current_args[2])
                elif information:
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

                    try:
                        guess = best_guess(words, current_args[0], current_args[1], current_args[2])
                    except IndexError:
                        guess = 'trash'

                for n in guess:
                    keyboard.press(n)
                    keyboard.release(n)

                if guess:
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)

                information = []

                content = driver.page_source
                soup = BeautifulSoup(content, features="html.parser")

                for a in soup.findAll('div', attrs={'class': 'RowL RowL-locked-in'}):
                    a = a.findAll('div')

                for i in a:
                    if 'absent' in str(i):
                        information.append('0')
                    elif 'elsewhere' in str(i):
                        information.append('-1')
                    else:
                        information.append('1')

                if information == ['1', '1', '1', '1', '1']:
                    clear()
                    wins += 1
                    break
                elif b == 5:
                    a = str(soup.find('div', attrs={'class': 'feedback'}).find('b'))
                    a = a[3:-4]
                    if a in words:
                        print("Lost to " + a)
                        losses += 1
                    else:
                        txt.close()
                        txt = open("Words.txt", 'a')
                        txt.write(('\n' + a).rstrip('\n'))
                        txt.close()

            if not information == ['1', '1', '1', '1', '1']:
                clear()

            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

            try:
                win_rate = (wins / (wins + losses)) * 100
                print(round(win_rate, 2), wins+losses, test_args[it], generation_number, it+1)

            except ZeroDivisionError:
                print(test_args, it, all_args)

            if wins+losses >= 200:
                wins = 0
                losses = 0
                all_args.append([win_rate, test_args[it]])
                break

    all_args.sort(reverse=True)
    print(all_args, generation_number)

    p = open("../Wordle/Parameters.txt", 'w')
    p.write(str(all_args[0][1]).lstrip('[').rstrip(']'))
    p.close()

    test_args = argument_adjustment(all_args[0][0], all_args[0][1][0], all_args[0][1][1], all_args[0][1][2])
    print(test_args)
    all_args = []

