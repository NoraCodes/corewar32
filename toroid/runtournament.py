#!bin/python3
from toroid import app, database, tournament
from toroid.warrior import Warrior
from sys import exit, stdout
from getpass import getpass
from itertools import combinations
from sys import argv

PREZERO = True
if '--no_prezero' in argv:
    PREZERO = False

# The number of rounds to run each head-to-head for.
ROUNDS = 50
if ROUNDS % 2 != 0:
    print("ROUNDS should be divisible by 2 (ROUNDS={}, consider {}, {})".format(ROUNDS, ROUNDS+1, ROUNDS-1))
    exit(3)

# This is the string used to format the results.
FMT_STRING = "{place:3}. {name:>24}  by {author:32}: {score:8}"

print("This script runs a tournament on a Toroid database.")
print("Scale your terminal so that this line fits on a single line:\n")
print(FMT_STRING.format(place=1,
                        name="Warrior Name",
                        author="Warrior K. Author",
                        score="1024"))
print("\nOnce you are certain that you are ready, enter your password:")

# Authenticate the command line user.
given = getpass("(characters will not appear) ")
#given = "password"
if app.config.get('ADMIN_PASSWORD', '') == given:
    print("Successfully authenticated!")
else:
    print("Access Denied.")
    exit(1)

# Pull everything from the database.
warriors = list(database.list_warriors())

if PREZERO:
    for warrior in warriors:
        warrior.score = 0

for pair in combinations(warriors, r=2):
    (w1score1, w2score1) = tournament.run_battle(pair[1], pair[0], rounds=int(ROUNDS/2))
    stdout.write(".")
    stdout.flush()
    (w1score2, w2score2) = tournament.run_battle(pair[0], pair[1], rounds=int(ROUNDS/2))
    stdout.write("o")
    stdout.flush()

    (w1score, w2score) = (w1score1 + w1score2, w2score1 + w2score2)

    pair[0].score += w1score
    pair[1].score += w2score

# Commit the warriors back to the database
print("\nCommitting the warriors back.")
for warrior in warriors:
    database.change_score_by_name(warrior.name, warrior.score)

print("The tournament is over!\n")
# The tournament has been run; sort the contestees

warriors.sort(key = lambda x: x.score, reverse=True)

# Display the warriors, that have been sorted
place = 1
last_score = 0
tied_so_far = 0
for w in warriors:
    if w.score < last_score:
        place += 1
    else:
        tied_so_far += 1

    last_score = w.score

    print(FMT_STRING.format(place=place,
                            name=w.name,
                            author=w.author,
                            score=w.score))
