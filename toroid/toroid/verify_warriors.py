from toroid.warrior import Warrior
from toroid.commands import *


def check_for_name(source):
    # Look through the source, trying to find a ;name
    for line in source.split('\n'):
        if len(line.split()) >= 2 and line.split()[0] == ";name":
            return line.strip(";name")
    # If execution reaches this point, there is no ;name line
    return False


def check_for_author(source):
    # Look through the source, trying to find a ;author
    for line in source.split('\n'):
        if len(line.split()) >= 2 and line.split()[0] == ";author":
            return line.strip(";author")
    # If execution reaches this point, there is not ;author line
    return False


def validate(source):
    import subprocess

    program_data = Warrior("", "", source)

    # First, check if ;name, ;author, and ;assert are all present

    program_data.name = check_for_name(source)
    if not program_data.name:
        return (False, "NAME metaline not found.\nYour program needs to have" +
                       " a line that starts with ;name and includes" +
                       " a program name.",
                       program_data)

    program_data.author = check_for_author(source)
    if not program_data.author:
        return (False, "AUTHOR metaline not found.\nYour program needs to" +
                       " have a line that starts with ;author and includes" +
                       " your name.",
                       program_data)

    # If we've reached this point, the metadata is valid
    # Open a PMARS process process we can communicate with
    p = subprocess.Popen((PMARS_CLI + PMARS_NO_ROUNDS + ' -').split(),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    # Send the program we need to validate, and get the output
    out = str(p.communicate(input=bytes(source, encoding="UTF-8"))[0],
              encoding="UTF-8") + "<br />"

    if p.returncode == 0:
        retval = True
    else:
        retval = False

    return (retval, out, program_data)
