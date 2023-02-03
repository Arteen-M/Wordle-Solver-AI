import json


def read(name):
    f = open(name, 'r')
    lines = []
    gen = []

    for line in f.readlines():
        if line[0] == '[':
            gen.append(line.strip('\n'))

        if line[0] == 'G' and gen:
            lines.append(gen)
            gen = []

    if gen:
        lines.append(gen)

    new_gen = []

    for gen in lines:
        new_lines = []
        for line in gen:
            line = line.strip('[').replace(']', '').split(', ')
            line[0] = '[' + line[0] + ']'
            new_lines.append(line)

        new_gen.append(new_lines)

    new_gen = [[[json.loads(line[0]), float(line[1])] for line in new] for new in new_gen]

    return new_gen


def write(name, list_of_gens):
    f = open(name, 'w+')

    f.write('Generation 1\n')

    for count, list_of_rates in enumerate(list_of_gens):
        f.writelines(['\n' + str(line).replace(" ", "").replace("],", "], ") for line in list_of_rates])
        if count + 2 <= len(list_of_gens):
            f.write('\nGeneration %d\n' % (count + 2))

    f.close()

