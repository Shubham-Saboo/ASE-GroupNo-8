import sys, ast, math, re

def coerce(s):
    def fun(s2):
        return None if s2 == "null" else s2.lower() == "true" or (s2.lower() != "false" and s2)

    try:
        return float(s)
    except ValueError:
        return fun(re.match(r'^\s*(.*\S)', s).group(1)) if isinstance(s, str) else s
   
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

def settings(s):
    t = {}
    opt_dir = {}
    options = re.findall(r'-(\w+)\s+--(\w+)\s+.*=\s*(\S+)', s)
    for option in options:
        short_form, full_form, default_value = option
        t[full_form] = coerce(default_value)
        opt_dir[short_form] = full_form
    return [t, opt_dir]

def round(n, nPlaces = 2):
    if type(n) == str:
        return n
    mult = 10**nPlaces
    return math.floor(float(n)*mult + 0.5) / mult 