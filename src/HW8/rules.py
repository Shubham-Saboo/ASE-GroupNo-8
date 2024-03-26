from utils import powerset
from rule import Rule
from config import the

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
        return self._score(t, self.goal, self.LIKE, self.HATE)

    def _score(self, t, goal, LIKE, HATE):
        like = sum([n for klass, n in t.items() if klass == goal])
        hate = sum([n for klass, n in t.items() if klass != goal])
        tiny = 1E-30
        like /= (LIKE + tiny)
        hate /= (HATE + tiny)
        return like ** the["Support"] / (like + hate) if hate <= like else 0

    def _try(self, ranges):
        u = []
        for subset in powerset(ranges):
            if len(subset) > 0:
                rule = Rule(subset)
                y_preds = rule.selectss(self.rowss)
                if(y_preds["LIKE"]==0 and y_preds["HATE"]==0):
                    rule.scored = 0
                else:
                    rule.scored = self.score(y_preds)
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