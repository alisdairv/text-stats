import codecs
import getopt
from multiprocessing import Pool
import os
import sys

from printer import output_stdout
from text_processor import gen_stats
from reader import read_chunks
from results_processer import compute_spec_results

def is__pos_int(var):
    """
    Validate positive integers

    :param var: test subject
    :return: True if var is postive integer, False if not
    :rtype: bool
    """
    try:
        val = int(var)
        if val > 0:
            return True
        else:
            return False
    except ValueError:
        return False

def handle_cli_args(argv):
    """
    Parse and validate command line arguments

    Reads arguments and tests validity of switches and respective values,
    on failure prints error to screen and exits.
    Returns tuple of valid arguments.

    Required arguments:
    -i      relative or absolute path to input text file
    Optional arguments:
    -e      encoding string to pass to codec.open(filename), e.g. 'utf-8'. Default: 'ascii'
    -n      number of cores to use in text processing task. Default: 1
    -c      size in bytes of chunks of text to pass to text_processor

    :param argv: argument list
    :return: tuple of: (absolute input file path, encoding type string, number of cores, text chunk size in bytes)
    :rtype: (str, str, int, int)
    """
    absinputfile = ''
    encoding = 'ascii'
    numcores = 1
    chunksize = 26000

    usageprompt = 'Usage: text_stats.py -i <inputfile> [-e <encoding>] [-n <numcores>] [-c <chunksize>]'
    try:
        opts, args = getopt.getopt(argv[1:],"i:e:n:c:")
    except getopt.GetoptError:
        print usageprompt
        sys.exit(2)
    if len(opts) == 0:
        print usageprompt
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i"):
            # input file
            absdir = os.path.abspath(os.path.dirname(argv[0]))
            if arg[:1] == "/":
                absinputfile = arg
            else:
                absinputfile = '{:s}/{:s}'.format(absdir, arg)
        elif opt in ("-e"):
            # encoding
            encoding = arg
        elif opt in ("-n"):
            # number of cores
            if is__pos_int(arg):
                numcores = int(arg)
            else:
                print usageprompt
                print 'numcores requires a positive integer. {:s} given'.format(arg)
                sys.exit(2)
        elif opt in ("-c"):
            # chunk size
            if is__pos_int(arg):
                chunksize = int(arg)
            else:
                print usageprompt
                print 'chunksize requires a positive integer. {:s} given'.format(arg)
                sys.exit(2)

    return absinputfile, encoding, numcores, chunksize

def open_text_file(inputfile, encoding, runningcli = True):
    """
    Open file with prescribed encoding

    Attempts to open file, on failure prints error to screen and exits.
    Returns wrapped file with transparent encoding/decoding.

    :param inputfile: string absolute path to input file
    :param encoding: string file encoding
    :return: codecs.StreamReaderWriter wrapped file
    :rtype: codecs.StreamReaderWriter
    """
    try:
        wrappedfile = codecs.open(inputfile, encoding=encoding)
    except IOError:
        print('No such file: {:s}' .format(inputfile))
        if runningcli:
            sys.exit(2)
        else:
            raise
    except LookupError:
        print('Unknown encoding: {:s}'.format(encoding))
        if runningcli:
            sys.exit(2)
        else:
            raise
    except:
        print('Unexpected error reading file: {:s}'.format(sys.exc_info()[0]))
        if runningcli:
            sys.exit(2)
        else:
            raise

    return wrappedfile

def main(argv):
    """
    Command line start

    Parses command line arguments, runs processing and prints stats to screen

    :param argv: tuple command line arguments
    :return: void
    :rtype: None
    """
    inputfile, encoding, numcores, chunksize = handle_cli_args(argv)
    sumwords, sumlines, meanlnword, modeletters, modeletterscs = compute_stats(inputfile, encoding, numcores, chunksize, True)
    output_stdout(sumwords, sumlines, meanlnword, modeletters, modeletterscs)
    sys.exit(0)

def compute_stats(inputfile, encoding, numcores, chunksize, runningcli = False):
    """
    Generate text file statistics

    Opens text file, counts character frequency and computes spec statistics.
    Returns spec statistics.

    :param inputfile: string absolute path to text file
    :param encoding: string text file encoding
    :param numcores: int number of workers to use for text chunk processing
    :param chunksize: int size in bytes of chunk (+ next line size) to send to each worker per task
    :return: tuple text file statistics (number of words, number of lines, avg word length, list of most common letters, list of most common letters(case-sensitive))
    :rtype: (int, int, float, list, list)
    """
    wrappedfile = open_text_file(inputfile, encoding)
    try:
        asciiarr, nonasciidict = read_process_file(wrappedfile, numcores, chunksize)
    except UnicodeDecodeError:
        print('Unable to decode file using {:s} encoding'.format(encoding))
        if runningcli:
            sys.exit(2)
        else:
            raise

    if sum(asciiarr) == 0 and sum(nonasciidict.values()) == 0:
        sumwords = sumlines = meanlnword = 0
        modeletters = []
    else:
        sumwords, sumlines, meanlnword, modeletters, modeletterscs = compute_spec_results(asciiarr, nonasciidict)
    return sumwords, sumlines, meanlnword, modeletters, modeletterscs

def read_process_file(filehandle, numcores, chunksize):
    """
    Count character frequency in text file

    Initialises a <numcores> number of Pool workers,
    generates text chunks and passes to workers,
    aggregates results on worker chunk stats return.
    Returns aggregated results of text chunk stats

    :param filehandle: codecs.StreamReaderWriter wrapped file
    :param numcores: int number of workers to use for text chunk processing
    :param chunksize: int size in bytes of chunk (+ next line size) to send to each worker per task
    :return: tuple (130 element array of ascii char freqs (+ non ascii count + repeated whitespace count), dictionary of nonasciidict[character] = freq)
    :rtype: (list, dict)
    """
    asciiarr = [0] * 130
    nonasciidict = {}

    pool = Pool(numcores)
    for chunkresult in pool.imap_unordered(gen_stats, read_chunks(filehandle, chunksize)):
        for (char, freq) in enumerate(chunkresult[0]):
            asciiarr[char] += freq
        for char, freq in chunkresult[1].iteritems():
            if char not in nonasciidict:
                nonasciidict[char] = freq
            else:
                nonasciidict[char] += freq


    return asciiarr, nonasciidict