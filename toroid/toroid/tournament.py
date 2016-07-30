from toroid.database import list_warriors, list_warriors_raw
from toroid.commands import *
from math import floor
import subprocess
from tempfile import NamedTemporaryFile
from os import unlink


def num_permutations():
    "Report the number of possible permutations."
    n = len(list_warriors_raw())
    return floor((n * (n-1)) / 2)


def run_battle(warrior_1, warrior_2, rounds):
    "Have warrior_1 fight warrior_2, reporting the number of points each got."
    # Write both warriors out to temporary files
    t1 = NamedTemporaryFile(delete=False)
    t2 = NamedTemporaryFile(delete=False)


    t1.write(bytes(warrior_1.source, encoding="UTF-8"))
    t2.write(bytes(warrior_1.source, encoding="UTF-8"))

    t1.close()
    t2.close()

    # Open a PMARS process process we can communicate with
    p = subprocess.Popen((PMARS_T_CLI + ' -r {} {} {}'
                                      .format(rounds, t1.name, t2.name)).split(),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    # Send the first program
    out = p.communicate()

    # Output is in KotH format: WON TIED\nWON TIED
    results = out[0].split()
    w1points = int(results[0]) + floor(int(results[1])/4)
    w2points = int(results[2]) + floor(int(results[3])/4)

    # Delete the files.
    unlink(t1.name)
    unlink(t2.name)

    return (w1points, w2points)
