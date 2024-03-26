from utils import powerset

class Rules:
    def __init__(self, ranges, goal, rowss):
        self.goal = goal
        self.rowss = rowss
        self.LIKE = 0
        self.HATE = 0
        self.sorted = []
        self.like_hate()

        for range in ranges:
            range.scored = self.score(range.y)
        self.sorted = self.top(self._try(self.top(ranges)))

    def like_hate(self):
        for y, rows in self.rowss.items():
            if y == self.goal:
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        return l.score(t, self.goal, self.LIKE, self.HATE)

    def _try(self, ranges):
        u = []
        for subset in powerset(ranges):
            if len(subset) > 0:
                rule = Rule(subset)
                rule.scored = self.score(rule.selectss(self.rowss))
                if rule.scored > 0.01:
                    u.append(rule)
        return u

    def top(self, t):
        t.sort(key=lambda x: x.scored, reverse=True)
        u = []
        for x in t:
            if x.scored >= t[0].scored * the['Cut']:
                u.append(x)
        return u[:int(the['Beam'])]
