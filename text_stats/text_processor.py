from array import array

def gen_stats(textchunk):
    """
    Count frequency of chars in text chunk

    Iterates over characters in text chunk,
    finds character code,
    if char is non ascii adds to nonasciidict (if not present), increments freq count and increments non ascii count (asciiarr[128]),
    if char is ascii increments array element at asciiarr[charcode],
    if char is whitespace and previous char is whitespace increment repeated whitespace count (asciiarr[129]) (for use in word count).
    Returns array of ascii char freqs and dictionary of non ascii char freqs

    :param textchunk: chunk of text
    :return: tuple (array of ascii char freqs, dictionary of non ascii char freqs)
    :rtype: (array, dict)
    """
    wscharcodes = [9, 10, 11, 12, 32]

    # array where,
    # 0-127 = ascii char freq,
    # 128 = nonascii char count,
    # and 129 = repeated whitespace count
    asciiarr = array('i', [0] * 130)
    nonasciidict = {}

    inrepeatedwhitespace = False

    prevval = 10
    for nextchar in textchunk:
        charval = ord(nextchar)
        if charval > 127:
            # not an ascii char
            if nextchar not in nonasciidict:
                nonasciidict[nextchar] = 1
            else:
                nonasciidict[nextchar] += 1
            charval = 128
        if charval < 33 and prevval < 33:
            if charval in wscharcodes and prevval < wscharcodes:
                # repeated whitespace, therefore not new word
                asciiarr[129] += 1
        else:
            inrepeatedwhitespace = False
        asciiarr[charval] += 1
        prevval = charval

    return asciiarr, nonasciidict
