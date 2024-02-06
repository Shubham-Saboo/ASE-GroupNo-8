from config import the
import math
class ROW:
    def __init__(self, t):
        self.cells = t

    def d2h(self, data):
        d, n, p = 0, 0, 2
        for col in data.cols.y:
            n += 1
            d += abs(col.heaven - col.norm(self.cells[col.at])) ** p
        return math.sqrt(d) / math.sqrt(n)

    def dist(self, other, data, p):
        d, n, p = 0, 0, 2
        for col in data.cols.x:
            n += 1
            d += data.cols.all[col.at].dist(self.cells[col.at], other.cells[col.at]) ** p
        return (d / n) ** (1 / p)

    def neighbor_key(self, row, data):
        return row.dist(self, data, 2)

    def neighbors(self, data, rows=None):
        if rows is None:
            rows = data.rows
        return sorted(rows, key=lambda row: self.neighbor_key(row, data))