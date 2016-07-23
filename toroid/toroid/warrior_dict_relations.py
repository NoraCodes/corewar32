from toroid import warrior


def dict_to_warrior(dictionary):
    ' Convert a warrior\'s data from a dict into a Warrior object '
    return warrior.Warrior(
        dictionary.get("name", ""),
        dictionary.get("author", ""),
        dictionary.get("source", ""),
        dictionary.get("score", 0)
    )


def warrior_to_dict(warrior):
    ' Convert a Warrior object into a dict '
    return {
        'name': warrior.name,
        'author': warrior.author,
        'source': warrior.source,
        'score': warrior.score
    }


def dictpair_to_warriorpair(dictpair):
    ' Convert a pair of dicts to a pair of warriors'
    return (dict_to_warrior(dictpair[0]),
            dict_to_warrior(dictpair[1]))


def dictlist_to_warriorlist(dictlist):
    ' Convert a list of dicts into a list of Warriors '
    return list(map(dict_to_warrior, dictlist))


def dictpairlist_to_warriorpairlist(dictpairlist):
    ' Convert a list of pairs of dicts to a list of pairs of Warriors'
    return list(map(dictpair_to_warriorpair, dictpairlist))
