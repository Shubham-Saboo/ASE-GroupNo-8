import sys, ast, math, re, random, time

def coerce(s):
    def fun(s2):
        return None if s2 == "null" else s2.lower() == "true" or (s2.lower() != "false" and s2)
    try:
        return float(s) if s is not None else None
    except ValueError:
        return fun(re.match(r'^\s*(.*\S)', s).group(1)) if isinstance(s, str) else s

def cells(s):
    t = [coerce(s1) for s1 in s.split(",")]
    return t

def csv(src):
    try:
        src = sys.stdin if src == "-" else open(src, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {src}")
    with src:
        for i, line in enumerate(src, start=1):
            yield i, cells(line.strip())

def settings(s):
    t = {}
    opt_dir = {}
    opts = re.findall(r'-(\w+)\s+--(\w+)\s+.*=\s*(\S+)', s)
    for short_form, full_form, default_value in opts:
        t[full_form] = coerce(default_value)
        opt_dir[short_form] = full_form

    options = sys.argv[1:]
    if "--help" in options or "-h" in options:
        t["help"] = True
        return t

    options_dict = {}
    for i in range(0, len(options), 2):
        opt = options[i]
        val = options[i + 1] if i + 1 < len(options) else None
        options_dict[opt] = val

    for opt, val in options_dict.items():
        key = opt[2:] if opt.startswith('--') else opt_dir[opt[1:]]
        t[key] = coerce(val)

    return t

def round(n, nPlaces = 2):
    if type(n) == str or n is None:
        return n
    mult = 10**nPlaces
    return math.floor(float(n)*mult + 0.5) / mult 

def set_random_seed():
        seed = int(re.sub(r'[^0-9]', '', str(time.time())[-7:]))
        return seed