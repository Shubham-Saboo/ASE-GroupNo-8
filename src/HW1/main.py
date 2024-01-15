from utils import *
from data import DATA
from num import NUM
from sym import SYM

def stats(data):
    for col in data.cols.all:
        if isinstance(col, NUM):
            mean = col.mid()
            print(f"Mean for numerical class '{col.txt}': {mean:.2f}")
        elif isinstance(col, SYM):
            mode = col.mid()
            print(f"Mode for symbolic class '{col.txt}': {mode}")

if __name__ == "__main__":
    file_path = "data/auto93.csv"
    data = DATA(file_path)
    stats(data)

