from utils import *
from data import DATA
from num import NUM
from sym import SYM


if __name__ == "__main__":
    file_path = "data/auto93.csv"
    data = DATA(file_path)
    print(data.stats())
