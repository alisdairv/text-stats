import unittest

from text_stats.results_processer import *
from text_stats.text_processor import gen_stats

# Cheating somewhat by using gen_stats to produce the stats!
class TestResultsProcessor(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_num_words(self):
        teststr = 'the quick brown fox jumps over the lazy dog'
        out1 = gen_stats(teststr)
        numfound = get_num_words(out1[0])
        numactual = 9
        self.assertEqual(numactual, numfound)

    def test_get_num_words_double_space(self):
        teststr = 'the quick brown fox   jumps over the lazy dog'
        out = gen_stats(teststr)
        numfound = get_num_words(out[0])
        numactual = 9
        self.assertEqual(numactual, numfound)

    def test_get_num_words_double_newline(self):
        teststr = 'the quick brown fox \n \njumps over the lazy dog'
        out = gen_stats(teststr)
        numfound = get_num_words(out[0])
        numactual = 9
        self.assertEqual(numactual, numfound)

    def test_get_num_words_two_chunk(self):
        teststr = 'the quick brown fox \n \njumps over the lazy dog'
        out1 = gen_stats(teststr)
        out2 = out1
        numfound = get_num_words(out1[0]) + get_num_words(out2[0])
        numactual = 18
        self.assertEqual(numactual, numfound)

    def test_get_num_lines_one(self):
        teststr = 'the quick brown fox jumps over the lazy dog'
        out = gen_stats(teststr)
        numfound = get_num_lines(out[0])
        numactual = 1
        self.assertEqual(numfound, numactual)

    def test_get_num_lines_two(self):
        teststr = 'the quick brown fox\njumps over the lazy dog'
        out = gen_stats(teststr)
        numfound = get_num_lines(out[0])
        numactual = 2
        self.assertEqual(numfound, numactual)

    def test_get_num_lines_two_multi(self):
        teststr = 'the quick brown fox\n\f\vjumps over the lazy dog'
        out = gen_stats(teststr)
        numfound = 4
        numactual = teststr.count('\n') + teststr.count('\f') + teststr.count('\v') + 1
        self.assertEqual(numfound, numactual)

    def test_get_mode_chars(self):
        teststr = 'the quick brown fox jumps over the lazy dog'
        out = gen_stats(teststr)
        combinedresults = combine_resultsets(out[0].tolist(), out[1])
        modefound = get_mode_chars(combinedresults)
        modeactual = ['o']
        self.assertEqual(modeactual, modefound)

if __name__ == '__main__':
    unittest.main()