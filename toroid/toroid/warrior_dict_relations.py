from toroid import warrior

def dict_to_warrior(dictionary):
    ' Convert a warrior\'s data from a dict into a Warrior object '
    return warrior.Warrior(
        dictionary.get("name", ""),
        dictionary.get("author", ""),
        dictionary.get("source", "")
    )


def warrior_to_dict(warrior):
    ' Convert a Warrior object into a dict '
    return {
        'name': warrior.name,
        'author': warrior.author,
        'source': warrior.source
    }
