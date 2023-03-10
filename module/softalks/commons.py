def evaluable(**args):
    return {key: value for key, value in args.items() if value is not None}

def startsWith(starting, string):
    return string.startswith(starting)

def endsWith(ending, string):
    return string.endswith(ending)