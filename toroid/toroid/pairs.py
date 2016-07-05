def make_pairings(warriors):
    if len(warriors) == 0:
        return False, False
    pairings = []
    for (warrior1, warrior2) in zip(warriors[0::2], warriors[1::2]):
        pairings.append((warrior1, warrior2))
    if len(warriors) % 2 == 0:
        odd_one_out = False
    else:
        odd_one_out = warriors[-1]
    return pairings, odd_one_out
