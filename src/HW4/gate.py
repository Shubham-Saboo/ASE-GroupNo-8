from utils import *
from data import DATA
from config import help_str, the
from test import Test

if __name__ == "__main__":
    the = settings(help_str)

    if the['help']:
        print(help_str)
    else:
        ts = Test()
        tests = {
            'coerce': ts.test_coerce_with_loop,
            'cells': ts.test_cells_random_data,
            'round': ts.test_round_various_numbers,
            'num_mid': ts.test_add_and_mid_num,
            'sym_mid': ts.test_add_and_mid_sym
        }
        if(the['run_tc'] == "" or the['run_tc'] is None):
            pass
        elif the['run_tc'] == "all":
            print("Running all test cases!")
            ts.run_tests()
        elif the['run_tc'] != "None":
            print(f"Running test {the['run_tc']}")
            try:
                tests[the['run_tc']]()
                print(f"Test {the['run_tc']} passed.")
            except AssertionError as e:
                print(f"Test {the['run_tc']} failed: {e}")

        data = DATA(the['file'])
        # print(data.stats())
        file_path = the['file']

        def learn(data, row, my):
            my['n'] += 1
            kl = row.cells[data.cols.klass.at]
            if my['n'] > 10:
                my['tries'] += 1
                my['acc'] += 1 if kl == row.likes(my['datas'])[0] else 0
            my['datas'][kl] = my['datas'].get(kl, DATA(data.cols.names))
            my['datas'][kl].add(row)


        def bayes():
            wme = {'acc': 0, 'datas': {}, 'tries': 0, 'n': 0}
            # n_hypotheses, most, tmp, out = 0, None, None, None  # Add these variables
            DATA(the['file'], lambda data, the: learn(data, the, wme))
            accuracy = (wme['acc'] / wme['tries'])*100
            print(f'The bayes function accuracy for the dataset {the["file"].split("/")[2]} is {accuracy:.2f}%')

        def km():
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
                        DATA(the['file'], lambda data, the: learn(data, the, wme))
                        accuracy = (wme['acc'] / wme['tries']) * 100
                        print(f'For k = {k} and m = {m}, accuracy is {accuracy:.2f}%')


                    # Update best combination if the current accuracy is higher
                        if accuracy > best_accuracy:
                            best_accuracy = accuracy
                            best_k, best_m = k, m

            print(f'The best combination is: k = {best_k}, m = {best_m}, with accuracy {best_accuracy:.2f}%')
        
        def gate():
            budget0, budget, some = 4, 10, 0.5        
            randomSeeds = random.sample(range(15000),20)
            for randomSeed in randomSeeds:
                d = DATA(file_path) #loads the data
                d.gate(budget0, budget, some)

            print('\n'.join(map(str, DATA.list_1)))
            print('\n')
            print('\n'.join(map(str, DATA.list_2)))
            print('\n')
            print('\n'.join(map(str, DATA.list_3)))
            print('\n')
            print('\n'.join(map(str, DATA.list_4)))
            print('\n')
            print('\n'.join(map(str, DATA.list_5)))
            print('\n')
            print('\n'.join(map(str, DATA.list_6)))

            # with open('../w4.out', 'w') as file:
            #     for sublist in DATA.list_1:
            #         file.write(sublist + '\n')
            #     for sublist in DATA.list_2:
            #         file.write(sublist + '\n')
            #     for sublist in DATA.list_3:
            #         file.write(sublist + '\n')
            #     for sublist in DATA.list_4:
            #         file.write(sublist + '\n')
            #     for sublist in DATA.list_5:
            #         file.write(sublist + '\n')
            #     for sublist in DATA.list_6:
            #         file.write(sublist + '\n')
        # bayes()
        # print("\nThe accuracies calculated using different values of k and m are:")
        gate()
        # km()
        