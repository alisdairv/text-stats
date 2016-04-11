import unittest

from text_stats.main import *

class TestMain(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_pos_int_success(self):
        validints = [1, 99]
        for validint in validints:
            ret = is__pos_int(validint)
            self.assertTrue(ret)

    def test_is_pos_int_fail(self):
        invalidints = [0, -1]
        for invalidint in invalidints:
            ret = is__pos_int(invalidint)
            self.assertFalse(ret)

if __name__ == '__main__':
    unittest.main()