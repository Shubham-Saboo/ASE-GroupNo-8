import sys

def coerce(s1):
    def fun(s2):
        return None if s2 == "nil" else s2 == "true" or (s2 != "false" and s2) 
    return math.tointeger(s1) or float(s1) or fun(s1.strip())

def cells(s):
    t = [coerce(s1) for s1 in s.split(",")]
    return t

def csv(src):
    i = 0
    try:
        src = sys.stdin if src == "-" else open(src, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"File is either not CSV or given path does not exist: {src}")

    s = src.readline().strip()
    while s:
        i += 1
        yield i, cells(s)
        s = src.readline().strip()
    src.close()
    return