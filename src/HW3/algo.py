from data import DATA
from config import the

def learn(data, row, my):
    my['n'] += 1
    kl = row.cells[data.cols.klass.at]
    if my['n'] > 10:
        my['tries'] += 1
        my['acc'] += 1 if kl == row.likes(my['datas'])[0] else 0
    my['datas'][kl] = my['datas'].get(kl, DATA(data.cols.names))
    my['datas'][kl].add(row)


def bayes(t):
    wme = {'acc': 0, 'datas': {}, 'tries': 0, 'n': 0}
    # n_hypotheses, most, tmp, out = 0, None, None, None  # Add these variables
    DATA(t['file'], lambda data, t: learn(data, t, wme))
    accuracy = (wme['acc'] / wme['tries'])*100
    print(f'The bayes function accuracy for the dataset {t["file"].split("/")[2]} is {accuracy:.2f}%')

def km(t):
    best_accuracy = 0
    best_k, best_m = None, None

    for k in range(4):
        for m in range(4):
            if m == 0:
                print(f'For k = {k} and m = {m}, accuracy is N/A')
            else:
                the['k'] = k
                the['m'] = m
                wme = {"acc": 0, "datas": {}, "tries": 0, "n": 0}
                DATA(t['file'], lambda data, t: learn(data, t, wme))
                accuracy = (wme['acc'] / wme['tries']) * 100
                print(f'For k = {k} and m = {m}, accuracy is {accuracy:.2f}%')


                    # Update best combination if the current accuracy is higher
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_k, best_m = k, m

    print(f'The best combination is: k = {best_k}, m = {best_m}, with accuracy {best_accuracy:.2f}%')
