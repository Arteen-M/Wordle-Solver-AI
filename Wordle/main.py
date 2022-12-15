import wordle

txt = open("Words.txt", 'r')
words = [line.strip('\n') for line in txt.readlines()]
txt.close()


# Generate a list of new parameters with small (0.1) and large (1.0) adjustments
def new_params(p1, p2, p3):
    new = [[p1 + 0.1, p2, p3], [p1 - 0.1, p2, p3], [p1 + 1, p2, p3], [p1 - 1, p2, p3],
           [p1, p2 + 0.1, p3], [p1, p2 - 0.1, p3], [p1, p2 + 1, p3], [p1, p2 - 1, p3],
           [p1, p2, p3 + 0.1], [p1, p2, p3 - 0.1], [p1, p2, p3 + 1], [p1, p2, p3 - 1]]
    return new


# Gets the win rate of a set of parameters
def get_rate(words, vowel, repeat, frequency):
    wins = 0
    for count, word in enumerate(words):
        # word = generator.random_word(words)
        # words.remove(word)
        # print(word)

        # Runs a wordle and if it wins (returns a non None type)
        if wordle.wordle(word, vowel, repeat, frequency) is not None:
            wins += 1  # Add 1 to wins

        if count % 1000 == 0:
            print(count)

    return wins / len(words)  # Returns the win rate


v = 4.9  # 4.9
r = 25.0  # 25.0
f = 0.8  # -0.2

# Amount of times to run adjustments
generations_to_run = 3

new_rates = []
params_tested = []
print("Started first set")
current_rate = get_rate(words, v, r, f)  # Get the rate of the starting set
print("Done first set", current_rate)

for x in range(generations_to_run):
    new_pars = new_params(v, r, f)  # Get all the new parameters based on the current set
    for y in range(len(new_pars)):
        # If that set hasn't been tested yet (over multiple generations,
        # there are some parameter sets that are repeated, which is inefficient
        if not (new_pars[y] in params_tested):
            print("Start next set")
            new_rate = get_rate(words, new_pars[y][0], new_pars[y][1], new_pars[y][2])  # New parameters rate
            new_rates.append((new_rate, new_pars[y]))  # Add it to the new rates list,
            params_tested.append(new_pars[y])
            print("Done set: %s" % str(new_pars[y]), new_rate)
        else:
            print("Already Tested Parameters: " + str(new_pars[y]))

    # Sort the list of rates (in reverse) to put the highest win rate first
    new_rates.sort(reverse=True)

    # If there is no rate better (or equal to) than the original rate, assume the best rate has been found
    if current_rate > new_rates[0][0]:
        break
    # Otherwise, replace the current_rate with the new best
    else:
        current_rate = new_rates[0][0]

    # Replace the parameters
    v = new_rates[0][1][0]
    r = new_rates[0][1][1]
    f = new_rates[0][1][2]

    print("Done Gen %d" % (x + 1))
    print(current_rate, v, r, f)

print(v, r, f)
