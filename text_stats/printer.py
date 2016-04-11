def output_stdout(sumwords, sumlines, meanlnword, modeletters, modeletterscs):
    print('Sum words: {:d}'.format(sumwords))
    print('Sum lines: {:d}'.format(sumlines))
    print('Mean word length: {:.1f}'.format(round(meanlnword, 1)))
    print('Modal letters:'),
    for char in modeletters:
        print char,
    print
    print('Modal letters (case sens):'),
    for char in modeletterscs:
        print char,
    print