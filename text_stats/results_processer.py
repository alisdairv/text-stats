import operator

asciinonprintable = [0,1,2,3,4,5,6,7,8,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,127]
asciiwhitespace = [9,10,11,12,32]
asciipunc = [33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,58,59,60,61,62,63,64,91,92,93,94,95,96,123,124,125,126]
asciinum = [48,49,50,51,52,53,54,55,56,57]

def zero_ascii_chars(asciiarr, zerocharlist):
    """
    Zeros asciiarr values for all values in zerocharlist

    :param asciiarr: list of ascii char freqs
    :param zerocharlist: list of ascii arr indices to zero
    :return: list of ascii char freqs with zerocharlist chars zeroed
    """
    for i in zerocharlist:
        asciiarr[i] = 0

    # zero any non ascii char indices
    asciiarr[128:] = [0] * (len(asciiarr) - 128)

    return asciiarr

def get_ascii_printable(asciiarr):
    """
    Zeros non printable ascii char counts in asciiarr

    :param asciiarr: list of ascii char freqs
    :return: list of ascii char freqs with non printable chars zeroed
    :rtype: list
    """
    return zero_ascii_chars(asciiarr, asciinonprintable)

def get_ascii_nonwhitespace(asciiarr):
    """
    Zeros whitespace ascii char counts in asciiarr

    :param asciiarr: list of ascii char freqs
    :return: list of ascii char freqs with whitespace chars zeroed
    :rtype: list
    """
    return zero_ascii_chars(asciiarr, asciiwhitespace)

def get_ascii_nonpunc(asciiarr):
    """
    Zeros punctuation ascii char counts in asciiarr

    :param asciiarr: list of ascii char freqs
    :return: list of ascii char freqs with punctuation chars zeroed
    :rtype: list
    """
    return zero_ascii_chars(asciiarr, asciipunc)

def get_ascii_nonnum(asciiarr):
    """
    Zeros numeric ascii char counts in asciiarr

    :param asciiarr:
    :return: list of ascii char freqs with numeric chars zeroed
    :rtype: list
    """
    return zero_ascii_chars(asciiarr, asciinum)

def get_ascii_letters_nums(asciiarr):
    """
    Zeros non alphanumeric ascii char counts in asciiarr

    :param asciiarr: list of ascii char freqs
    :return: list of ascii char freqs with non alphanumeric chars zeroed
    :rtype: list
    """
    asciiarr = get_ascii_printable(asciiarr)
    asciiarr = get_ascii_nonwhitespace(asciiarr)
    asciiarr = get_ascii_nonpunc(asciiarr)

    return asciiarr

def get_ascii_letters(asciiarr):
    """
    Zeros non alpha ascii char counts in asciiarr

    :param asciiarr: list of ascii char freqs
    :return: list of ascii char freqs with non alpha chars zeroed
    :rtype: list
    """
    asciiarr = get_ascii_letters_nums(asciiarr)
    asciiarr = get_ascii_nonnum(asciiarr)

    return asciiarr

def combine_resultsets(asciiarr, chardict):
    """
    Combine array of ascii counts and dictionary of non ascii chars into single dictionary

    Removes ascii chars with zero occurences

    :param asciiarr: list of ascii char freqs
    :param chardict: dict of non ascii char keys and freq values
    :return: dict of all expressed char keys and freq values
    :rtype: dict
    """
    asciiletters = get_ascii_letters_nums(asciiarr)
    for charcode, freq in enumerate(asciiletters):
        if freq > 0:
            chardict[chr(charcode)] = freq

    return chardict

def get_mode_chars(chardict):
    """
    Get list of most frequently occuring characters

    :param chardict: dict
    :return: list
    """
    maxfreq = max(chardict.iteritems(), key=operator.itemgetter(1))[1]
    modechars = [x for x, y in chardict.items() if y == maxfreq]

    return modechars

def get_num_lines(asciiarr):
    """
    Get sum of newlines chars in asciiarr

    :param asciiarr: list of ascii char freqs
    :return: int sum of LF, VT and FF char frequencies
    :rtype: int
    """
    numlines = sum(asciiarr[10:13]) + 1

    return numlines

def get_num_words(asciiarr):
    """
    Calculate number of words

    :param asciiarr: list of ascii char freqs
    :return: int whitespace char freq less repeated whitespace freq
    :rtype: int
    """
    # printable whitespace values
    wscharcodes = [9, 10, 11, 12, 32]
    # get sum of whitespace in file
    sumws = 0
    for charcode in wscharcodes:
        sumws += asciiarr[charcode]
    # less the repeated whitespace count
    sumws -= asciiarr[129]
    # "counting some strings" is 3 words with 2 whitespace chars
    sumwords = sumws + 1

    return sumwords

def get_non_case_sensitive(asciiarr):
    for i in range(65, 91):
        asciiarr[i + 32] += asciiarr[i]
        asciiarr[i] = 0

    return asciiarr

def compute_spec_results(asciiarr, nonasciidict):
    sumwords = get_num_words(asciiarr)
    sumlines = get_num_lines(asciiarr)
    sumprintnonwhitespace = sum(get_ascii_nonwhitespace(get_ascii_printable(asciiarr))) + sum(nonasciidict.values())
    meanlnword = sumprintnonwhitespace / float(sumwords)
    combosetscs = combine_resultsets(asciiarr, nonasciidict)
    modeletterscs = get_mode_chars(combosetscs)
    combosets = combine_resultsets(get_non_case_sensitive(asciiarr), nonasciidict)
    modeletters = get_mode_chars(combosets)

    return sumwords, sumlines, meanlnword, modeletters, modeletterscs