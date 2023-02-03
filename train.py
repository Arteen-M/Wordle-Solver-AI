import wordle
import copy
import file


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


# Generate a list of new parameters with small (0.1) and large (1.0) adjustments
def new_params(p1, p2, p3):
    new = [[round(p1 + 0.1, 1), p2, p3], [round(p1 - 0.1, 1), p2, p3], [round(p1 + 1, 1), p2, p3],
           [round(p1 - 1, 1), p2, p3],
           [p1, round(p2 + 0.1, 1), p3], [p1, round(p2 - 0.1, 1), p3], [p1, round(p2 + 1, 1), p3],
           [p1, round(p2 - 1, 1), p3],
           [p1, p2, round(p3 + 0.1, 1)], [p1, p2, round(p3 - 0.1, 1)], [p1, p2, round(p3 + 1, 1)],
           [p1, p2, round(p3 - 1, 1)]]
    return new


# Gets the win rate of a set of parameters
def get_rate(words, vowel, repeat, frequency):
    wins = 0
    for count, word in enumerate(words):
        # Runs a wordle and if it wins (returns a non None type)
        if wordle.wordle(word, vowel, repeat, frequency) is not None:
            wins += 1  # Add 1 to wins

        # Print out the progress
        if count % 500 == 0:
            print(count)

    return wins / len(words)  # Returns the win rate


def get_speed(words, vowel, repeat, frequency):
    # total rounds it took to win all the wordles
    total_per_game = 0
    for count, word in enumerate(words):
        # Number of rounds for the specified word
        num_rounds = wordle.wordle(word, vowel, repeat, frequency, 'inf')

        # If it crashes or errors before solving the word, default to 7 rounds
        if num_rounds is None:
            num_rounds = 7

        # Add the current rounds to the total
        total_per_game += num_rounds

        # Print out the progress
        if count % 500 == 0:
            print(count)

    # Find the average rounds per game
    return total_per_game / len(words)


def train(objective, generations, starting_params=[6.0, 20.0, 1.0]):
    if objective == 'speed':
        rev = False
        fi = 'Automatic Records/speed.txt'
    else:
        rev = True
        fi = 'Automatic Records/accuracy.txt'

    # Amount of times to run adjustments
    generations_to_run = generations

    output_rates = file.read(fi)
    params_tested = []
    for gen in output_rates:
        for rates in gen:
            params_tested.append(rates[0])

    print("Started first set")
    try:
        rates = sorted(output_rates[-1], key=lambda x: x[1], reverse=rev)[0]
        current_rate = rates[1]
        v = rates[0][0]
        r = rates[0][1]
        f = rates[0][2]

    except IndexError:
        v = starting_params[0]  # 6.0  # 4.8
        r = starting_params[1]  # 20.0  # 26.0
        f = starting_params[2]  # 1.0  # 0.8

        # Get the objective stat of the starting set
        if objective == 'speed':
            current_rate = get_speed(words, v, r, f)
        else:
            current_rate = get_rate(words, v, r, f)

    print("Done first set: [%.1f, %.1f, %.1f]" % (v, r, f), current_rate)

    for x in range(generations_to_run):
        new_pars = new_params(v, r, f)  # Get all the new parameters based on the current set
        new_rates = []

        for y in range(len(new_pars)):
            # If that set hasn't been tested yet (over multiple generations,
            # there are some parameter sets that are repeated, which is inefficient
            if not (new_pars[y] in params_tested):
                print("Start next set: ", new_pars[y])
                # new_rate = get_rate(words, new_pars[y][0], new_pars[y][1], new_pars[y][2])  # New parameters rate
                if objective == 'speed':
                    new_rate = get_speed(words, new_pars[y][0], new_pars[y][1], new_pars[y][2])
                else:
                    new_rate = get_rate(words, new_pars[y][0], new_pars[y][1], new_pars[y][2])

                new_rates.append([new_pars[y], new_rate])  # Add it to the new rates list,
                params_tested.append(new_pars[y])

                print("Done set: %s" % str(new_pars[y]), new_rate)
            else:
                found = False

                for gen in output_rates:
                    for rates in gen:
                        if rates[0] == new_pars[y]:
                            new_rates.append([new_pars[y], rates[1]])
                            found = True
                            break

                    if found:
                        break

                print("Already Tested Parameters: " + str(new_pars[y]))

            #    # Sort the list of rates (in reverse) to put the highest win rate first
            #    # new_rates.sort(key=lambda e: e[1], reverse=True)
            adding = copy.deepcopy(new_rates)
            adding.insert(0, [[v, r, f], current_rate])

            if len(output_rates) > 0:
                if len(output_rates[-1]) == 13:
                    output_rates.append(adding)
                else:
                    output_rates[-1] = adding
            else:
                output_rates.append(adding)

            file.write(fi, output_rates)
            new_rates.sort(key=lambda e: e[1], reverse=rev)
        #

        # If there is no rate better (or equal to) than the original rate, assume the best rate has been found
        if current_rate < new_rates[0][1]:
            # if current_rate > new_rates[0][0]:
            break
        # Otherwise, replace the current_rate with the new best
        else:
            current_rate = new_rates[0][1]

        # Replace the parameters
        v = new_rates[0][0][0]
        r = new_rates[0][0][1]
        f = new_rates[0][0][2]

        print("Done Gen %d" % (x + 1))
        print(current_rate, v, r, f)

    print(v, r, f)


# train('speed', 10)
# print(get_rate(words, 4.9, 26.0, 0.8))
