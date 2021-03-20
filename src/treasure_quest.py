import getopt
import sys

from src.back import TreasureMap

SEPARATOR = " - "


def treasure_quest(input_file=None):
    if not input_file:
        input_file = pick_config()

    print("Input:", input_file)
    tm = integrate(input_file)
    tm.play()

    print(tm)
    res = format_result(tm.get_data())
    print("Output:")
    print("".join(["\t" + l + "\n" for l in res.split("\n")]))
    print("Total turns:", tm.iteration)
    return res


def pick_config():
    input_file_2 = """
    C - 3 - 4
    M - 1 - 0
    M - 2 - 1
    T - 0 - 3 - 2
    T - 1 - 3 - 3
    A - Lara - 1 - 1 - S - AADADAGGA
    """
    input_file = """
    C - 10 - 8
    M - 1 - 0
    M - 2 - 1
    M - 2 - 4
    M - 5 - 7
    T - 0 - 3 - 2
    T - 1 - 7 - 3
    T - 6 - 0 - 3
    T - 6 - 4 - 6
    T - 5 - 2 - 2
    T - 4 - 6 - 5
    T - 1 - 3 - 3
    A - Lara - 1 - 1 - S - AADADAGGAGGAAGGAGAGA
    A - Indiana - 2 - 1 - S - AADDAGADADAGGAAA
    A - Yves - 5 - 3 - E - AADDAGADADAGGAAA
    A - Tom - 5 - 7 - W - DAADADAGAGADAGAADAGGA
    A - Amande - 4 - 6 - W - AADAADADAGAGADAGAADAGGA
    """
    return input_file


def integrate(file):
    w, h = 0, 0
    mtn, tsr, plyr = [], [], []

    for line in file.split("\n"):
        fields = line.strip().split(SEPARATOR)

        if not fields or fields[0] == "#":
            continue

        if fields[0] == "C":
            w, h = int(fields[2]), int(fields[1])
        elif fields[0] == "M":
            mtn += ((int(fields[2]), int(fields[1])),)
        elif fields[0] == "T":
            tsr += ((int(fields[2]), int(fields[1]), int(fields[3])),)
        elif fields[0] == "A":
            plyr += ((fields[1], int(fields[2]), int(fields[3]), fields[4], fields[5]),)

    return TreasureMap(width=w, height=h, mountains=mtn, treasures=tsr, players=plyr)


def format_result(data):
    txt = ""
    for k, v in data.items():
        if k == "Map":
            x, y = v
            y, x = str(x), str(y)
            txt += SEPARATOR.join(["C", x, y])
            txt += "\n"
        elif k == "Mountains":
            for mtn in v:
                x, y = mtn
                y, x = str(x), str(y)
                txt += SEPARATOR.join(["M", x, y])
                txt += "\n"
        elif k == "Treasures":
            for tsr in v:
                pos, nb = tsr
                x, y = pos
                y, x, nb = str(x), str(y), str(nb)
                txt += SEPARATOR.join(["T", x, y, nb])
                txt += "\n"
        elif k == "Players":
            for plyr in v:
                name, pos, dir, nb = plyr
                x, y = pos
                y, x, nb = str(x), str(y), str(nb)
                txt += SEPARATOR.join(["A", name, x, y, dir, nb])
                txt += "\n"

    return txt
