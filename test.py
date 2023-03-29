from search import program, coordinate_system

if __name__=='__main__':

    tests = ['test.csv', 
            'test9.csv',
            #'test2.csv', 
            #'test3.csv',
            'test4.csv', 
            'test5.csv',
            'test6.csv',
            #'test7.csv',
            'test8.csv',
            'test22.csv']

    for files in tests:
        with open(files, 'r') as f:
            d={(int(r), int(q)): (p.strip(), int(k))
            for r, q, p, k in [
                line.split(',') for line in f.readlines() 
                if len(line.strip()) > 0
            ]}

        print(f'Test {files}:')
        # print(1, end=' ')
        # program.search(d, print_moves=False, heuristic=True, sixdiv=False, bluecounts=True)
        # print(2, end=' ')
        # program.search(d, print_moves=False, heuristic=True, sixdiv=False, bluecounts=True, perc=True)
        # print(3, end=' ')
        # program.search(d, False, True, True, False, True)
        # print(4, end=' ')
        # program.search(d, False, True, False, True, False)
        print(5, end=' ')
        program.search(d, False, True, True, False)
        #print(6, end=' ')
        #program.search(d, False, True, True, False, False)
        # print(7, end=' ')
        # program.search(d, False, True, True, True)
        # print(8, end=' ')
        # program.search(d, False, True, False, False)
        print(9, end=' ')
        program.search(d, False, False)