
def filter_source(source):
    ' Remove unneeded things from the source '
    source = source.strip()
    source = source.replace('\r', '')
    return source
