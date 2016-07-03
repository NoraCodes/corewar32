# This is the default command line for PMARS, with the settings we've specified
PMARS_CLI = "pmars -k -p 8000 -c 80000 -p 8000 -l 100 -d 100"
# This addition to the command line makes PMARS run with just validation
PMARS_NO_GRAPHICS = " -r 0 -v 000"


class MetadataNotFoundException (Exception):
    pass

def check_for_name(source):
    # Look through the source, trying to find a ;name
    for line in source.split('\n'):
        if len(line.split()) >= 2 and line.split()[0] == ";name":
            return line.strip(";name")
    # If execution reaches this point, there is no ;name line
    raise MetadataNotFoundException


def check_for_author(source):
    # Look through the source, trying to find a ;author
    for line in source.split('\n'):
        if len(line.split()) >= 2 and line.split()[0] == ";author":
            return line.strip(";author")
    # If execution reaches this point, there is not ;author line
    raise MetadataNotFoundException


def validate(source):
    import subprocess

    program_data = {'name': "",
                    'author': "",
                    'source': source}

    # First, check if ;name, ;author, and ;assert are all present
    try:
        name = check_for_name(source)
    except MetadataNotFoundException:
        return (False, "NAME metaline not found.\nYour program needs to have a" +
                    " line that starts with ;name and includes" +
                    " a program name.",
                    program_data)
    try:
        author = check_for_author(source)
    except MetadataNotFoundException:
        return (False, "AUTHOR metaline not found.\nYour program needs to have" +
                    "a line that starts with ;author and includes your name.",
                    program_data)

    # If we've reached this point, the program is valid
    program_data['name'] = name
    program_data['author'] = author

    # Open a PMARS process process we can communicate with
    p = subprocess.Popen((PMARS_CLI + PMARS_NO_GRAPHICS + ' -').split(),
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
