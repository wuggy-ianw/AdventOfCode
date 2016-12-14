import unittest
from day14 import Day14Solver

class Day14Tests(unittest.TestCase):
    def test_example1(self):
        # For example, if the pre-arranged salt is abc:
        solver = Day14Solver('abc')

        # The first index which produces a triple is 18, because the MD5 hash of abc18
        # contains ...cc38887a5.... However, index 18 does not count as a key for your one-time pad,
        # because none of the next thousand hashes (index 19 through index 1018) contain 88888.
        for i in range(0, 18):
            key, didmatch3, didmatch5 = solver.step()
            self.assertEqual(solver.search_index, i)
            self.assertEqual(key, None)
            self.assertFalse(didmatch3)
            self.assertFalse(didmatch5)

        # index 18...
        key, didmatch3, didmatch5 = solver.step()
        self.assertEqual(solver.search_index, 18)
        self.assertEqual(key, None)
        self.assertTrue(didmatch3)
        self.assertFalse(didmatch5)

        self.assertTrue('cc38887a5' in solver.get_hash(18))
        for k in range(19, 1019):
            self.assertFalse('88888' in solver.get_hash(18))

        # The next index which produces a triple is 39; the hash of abc39 contains eee. It is also
        # the first key: one of the next thousand hashes (the one at index 816) contains eeeee.
        for i in range(19,39):
            key, didmatch3, didmatch5 = solver.step()
            self.assertEqual(solver.search_index, i)
            self.assertEqual(key, None)
            self.assertFalse(didmatch3)
            self.assertFalse(didmatch5)

        # index 39...
        key, didmatch3, didmatch5 = solver.step()
        self.assertEqual(solver.search_index, 39)
        self.assertTrue('eee' in key)
        self.assertTrue(didmatch3)
        self.assertTrue(didmatch5)

        # None of the next six triples are keys, but the one after
        # that, at index 92, is: it contains 999 and index 200 contains 99999.
        key = solver.find_next_valid_key()
        self.assertTrue('999' in key)
        self.assertEqual(solver.search_index, 92)
        self.assertTrue('99999' in solver.get_hash(200))

        # Eventually, index 22728 meets all of the criteria to generate the 64th key.
        n_keys = 2      # for the 2 already found
        while solver.search_index<22728:
            key = solver.find_next_valid_key()
            self.assertTrue(key)

            n_keys += 1

        self.assertEqual(n_keys, 64)
        self.assertTrue(key)

    def test_stretched_example1(self):

        solver = Day14Solver('abc', stretched = True)

        # So, the stretched hash for index 0 in this situation is a107ff....
        hash = solver.get_hash(0)
        self.assertTrue(hash.startswith('a107ff'))

        # The first triple (222, at index 5) has no matching 22222 in the next thousand hashes.
        for i in range(0,5):
            key, didmatch3, didmatch5 = solver.step()
            self.assertEqual(solver.search_index, i)
            self.assertEqual(key, None)
            self.assertFalse(didmatch3)
            self.assertFalse(didmatch5)

        # index 5...
        key, didmatch3, didmatch5 = solver.step()
        self.assertEqual(solver.search_index, 5)
        self.assertEqual(key, None)
        self.assertTrue(didmatch3)
        self.assertFalse(didmatch5)

        # The second triple (eee, at index 10) hash a matching eeeee at index 89, and so it is the first key.
        key = solver.find_next_valid_key()
        self.assertEqual(solver.search_index, 10)

        # Eventually, index 22551 produces the 64th key (triple fff with matching fffff at index 22859.
        n_keys = 1  # for the 1 already found
        while solver.search_index < 22551:
            key = solver.find_next_valid_key()
            self.assertTrue(key)

            n_keys += 1

        self.assertEqual(n_keys, 64)
        self.assertTrue(key)

if __name__ == '__main__':
    unittest.main()
