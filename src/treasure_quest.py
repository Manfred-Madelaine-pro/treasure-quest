import getopt
import sys

from src.back import TreasureMap

SEPARATOR = " - "


def treasure_quest(input_file=None, random=False):
    if not random:
        if not input_file:
            input_file = pick_config()

        print("Input:", input_file)
        tm = integrate(input_file)
    else:
        tm = random_map()

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

    return TreasureMap(width=w, height=h, mountains=mtn, treasures=tsr, adventurers=plyr)


def random_map():
    import random as rnd

    w, h = 10, 8
    random_elements = {
        "M": rnd.randint(0, max([w, h])),               # mountains
        "T": rnd.randint(1, max([w, h])),               # treasures
        "A": rnd.randint(min([2, w, h]), max([w, h]))   # adventurers
    }

    max_treasures = 5
    directions = ["N", "S", "W", "E"]
    adventurers_names = ["Lara", "James", "Tom", "Sora", "Arthur", "John", "Amande", "Amy", "Loue", "Lupin", "Mendez", "Zain"]

    picked_names = []
    mtn, tsr, adv = [], [], []
    for elem, amount in random_elements.items():
        for _ in range(amount):
            x, y = rnd.randint(0, w - 1), rnd.randint(0, h - 1)
            if elem == "M":
                mtn += [(x, y)]
            elif elem == "T":
                treasures = rnd.randint(1, max_treasures)
                tsr += [(x, y, treasures)]
            elif elem == "A":
                name = rnd.choice(adventurers_names)
                picked_names += [name]
                u_name = name + int_to_roman(picked_names.count(name)) if name in picked_names else ''
                direction = rnd.choice(directions)
                path = ""
                adv += [(u_name, x, y, direction, path)]

    tm = TreasureMap(width=w, height=h, mountains=mtn, treasures=tsr, adventurers=adv)
    tm.turns = 10

    return tm


def int_to_roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num


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
        elif k == "adventurers":
            for plyr in v:
                name, pos, dir, nb = plyr
                x, y = pos
                y, x, nb = str(x), str(y), str(nb)
                txt += SEPARATOR.join(["A", name, x, y, dir, nb])
                txt += "\n"

    return txt


if __name__ == "__main__":
    treasure_quest(random=True)
