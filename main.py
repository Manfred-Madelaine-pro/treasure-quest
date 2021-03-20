import argparse

import src.treasure_quest as tq


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        help="define the input file")
    parser.add_argument("-r", "--random", action="store_true",
                        help="add randomness in the quest")
    args = parser.parse_args()

    return args.file, args.random


if __name__ == "__main__":
    input_f, randomized = main()

    if input_f:
        with open(input_f, "r") as file:
            input_file_arg = file.read()

        res = tq.treasure_quest(input_file_arg)

        with open("results.txt", "w") as file:
            file.write(res)
    else:
        tq.treasure_quest(random=randomized)
