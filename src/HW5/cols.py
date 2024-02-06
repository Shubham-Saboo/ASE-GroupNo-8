from sym import SYM
from num import NUM
from row import ROW

class COLS:
    def __init__(self, row):
        self.x, self.y, self.all = [], [], []
        self.klass, self.names = None, row.cells

        for at, txt in enumerate(row.cells):
            # print(f"Column Name: {txt}, Is Numeric: {txt[0].isalpha() and txt[0].isupper()}")
            col = (NUM if txt[0].isalpha() and txt[0].isupper() else SYM)(txt, at)
            self.all.append(col)

            if not txt.endswith("X"):
                if txt.endswith("!"):
                    self.klass = col
                (self.y if txt.endswith(("!", "-", "+")) else self.x).append(col)

    def add(self, row):
        # print("Adding row:", row.cells)
        for cols in [self.x, self.y]:
            for col in cols:
                col.add(row.cells[col.at])
        return row