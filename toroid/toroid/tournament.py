from toroid.database import list_warriors, list_warriors_raw
from math import floor


def num_permutations():
    "Report the number of possible permutations."
    n = len(list_warriors_raw())
    return floor((n * (n-1)) / 2)
