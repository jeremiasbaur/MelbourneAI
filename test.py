from search import program, coordinate_system

tests = ['test.csv', 
         #'test2.csv', 
         #'test3.csv',
         'test4.csv', 
         #'test5.csv',
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
    program.search(d, False, True, False, True)
    program.search(d, False, True, True, False)
    program.search(d, False, True, True, True)
    program.search(d, False, True, False, False)
    program.search(d, False, False)