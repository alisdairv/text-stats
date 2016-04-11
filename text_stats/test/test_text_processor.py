# -*- coding: utf-8 -*-

import unittest

from text_stats.text_processor import gen_stats

class TestTextProcessor(unittest.TestCase):
    def setUp(self):
        pass

    def test_gen_stats_ascii_simple(self):
        teststr = 'the quick brown fox jumps over the lazy dog'
        out = gen_stats(teststr)
        for i in range(128):
            numfound = out[0][i]
            numactual = teststr.count(chr(i))
            self.assertEqual(numactual, numfound)

    def test_gen_stats_ascii_two_line(self):
        teststr = 'the quick brown fox jumps over the lazy dog\n\nthe quick brown fox jumps over the lazy dog\n'
        out = gen_stats(teststr)
        for i in range(128):
            numfound = out[0][i]
            numactual = teststr.count(chr(i))
            self.assertEqual(numactual, numfound)

    def test_gen_stats_ascii_two_chunk(self):
        teststr = 'the quick brown fox jumps over the lazy dog\n'
        out1 = gen_stats(teststr)
        out2 = gen_stats(teststr)
        combstr = teststr + teststr
        for i in range(128):
            numfound = out1[0][i] + out2[0][i]
            numactual = combstr.count(chr(i))
            self.assertEqual(numactual, numfound)

    def test_gen_stats_utf_simple(self):
        # trad chinese quick brown.... fyi
        teststr = u'快速的棕色狐狸跳過懶狗'
        out = gen_stats(teststr)
        for char in teststr:
            numfound = out[1][char]
            numactual = teststr.count(char)
            self.assertEqual(numactual, numfound)