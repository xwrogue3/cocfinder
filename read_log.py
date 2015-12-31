from argparse import ArgumentParser
import re

from cocfinder.models import Base, TownHallLevel, TrophyLeague


BASE_STATS = '\[G\]\:\s+(\d+)\s+\[E\]\:\s+(\d+)\s+\[D\]\:\s+(\d+)\s+\[T\]\:\s*(\d+)\s+\[TH\]\:\s*(\d+)'

def my_base(line, th):
    try:
        m = re.search('\[T\]\:\s+(\d+)\s*(\d*)', line)
        if len(m.groups()) == 2:
            trophy = 1000 * int(m.group(1)) + int(m.group(2))
        else:
            trophy = int(m.group(1))
        print trophy
        tl = TrophyLeague.objects.get_by_trophy(trophy)
    except:
        print "Couldn't find trophy league or townhall level"
        return None, None
    else:
        print "Found trophy league %s" % tl
        return tl, TownHallLevel.objects.get(th)


def add_base(line, trophyleague, found_th):
    m = re.search(BASE_STATS, line)
    gold = m.group(1)
    elixir = m.group(2)
    de = m.group(3)
    trophyies = m.group(4)
    th = TownHallLevel.objects.get(m.group(5))
    base = Base.objects.create(th, gold, elixir, de, trophyleague, found_th)
    print base


def main(args):
    found_builders = False
    with open(args.filename) as f:
        lines = f.readlines()
        for l in lines:
            if found_builders:
                found_builders = False
                trophyleague, th = my_base(l, args.th)
            elif re.search('Free\/Total Builders', l):
                # Next line has our bases trophy count
                found_builders = True
            if re.search(BASE_STATS, l):
                add_base(l, trophyleague, th)


if __name__ == '__main__':

    parser = ArgumentParser(description='Parse a log and import the base information')
    parser.add_argument('filename', help='log file name')
    parser.add_argument('--th', help='Townhall level of the searching base. Defaults '
                                   'to 9', default=9)
    args = parser.parse_args()

    main(args)
