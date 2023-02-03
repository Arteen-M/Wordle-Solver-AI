import wordle
import solver
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

if config_lines[1] == "speed":
    params_list = [2.9, 17.1, 2.1]  # [2.0, 21.0, 1.0]
else:
    params_list = [4.9, 26.0, 0.8]

print("Settings:", config_lines[0], config_lines[1])

txt = open("Word Lists/" + word_list, 'r')
words = [line.strip('\n') for line in txt.readlines()]
txt.close()

v = params_list[0]  # 2.0  # 4.9
r = params_list[1]  # 21.0  # 26.0
f = params_list[2]  # 1.0  # 0.8

if input("Auto-Generate? ").lower() == 'y':
    word = input("Enter the word for the day: ").lower()
    wordle.wordle(word, v, r, f, 6, True)
else:
    info = []
    guess = 'irate'
    new_words = copy.deepcopy(words)
    for x in range(6):
        guess, new_words = solver.next_word(info, guess, x, new_words, v, r, f)
        print(guess)
        info = input("Enter info: ")
        if info == "1 1 1 1 1":
            break

        info = info.split()
        for y in range(len(info)):
            info[y] = int(info[y])
