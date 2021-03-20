import getopt
import sys

import src.treasure_quest as tq


def main(argv):
    input_file = ''

    try:
        opts, args = getopt.getopt(argv, "f:", ["file="])
    except getopt.GetoptError:
        print('Error.\nTry : main.py [-f <inputfile>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            input_file = arg
    return input_file


if __name__ == "__main__":
    input_f = main(sys.argv[1:])

    if input_f:
        with open(input_f, "r") as file:
            input_file_arg = file.read()

        res = tq.treasure_quest(input_file_arg)

        with open("results.txt", "w") as file:
            file.write(res)
    else:
        tq.treasure_quest()
