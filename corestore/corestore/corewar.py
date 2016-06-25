# This is the default command line for PMARS, with the settings we've specified
PMARS_CLI = "pmars -k -p 8000 -c 80000 -p 8000 -l 100 -d 100"
# This addition to the command line makes PMARS run with just validation
PMARS_NO_GRAPHICS = " -r 0 -v 000"

def check_for_name(source):
    # Look through the source, trying to find a ;name
    found = False
    for line in source.split('\n'):
        if len(line.split()) >= 2 and line.split()[0] == ";name":
            found = True
            break
    return found

def check_for_author(source):
    # Look through the source, trying to find a ;author
    found = False
    for line in source.split('\n'):
        if len(line.split()) >= 2 and line.split()[0] == ";author":
            found = True
            break
    return found

def validate(source):
    import subprocess

    # First, check if ;name, ;author, and ;assert are all present
    if not check_for_name(source):
        return (-1, "NAME metaline not found.\nYour program needs to have a line" +
                    " that starts with ;name and includes a program name.")
    if not check_for_author(source):
        return (-1, "AUTHOR metaline not found.\nYour program needs to have a " +
                    "line that starts with ;author and includes your name.")


    # Open a PMARS process process we can communicate with
    p = subprocess.Popen((PMARS_CLI + PMARS_NO_GRAPHICS + ' -').split(),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
    # Send the program we need to validate, and get the output
    out = str(p.communicate(input=bytes(source, encoding="UTF-8"))[0], encoding="UTF-8") + "<br />"
    retval = p.returncode
    return (retval, out)
