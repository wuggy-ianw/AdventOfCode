import unittest

from day5 import day5a_solver, day5b_solver

class Day5TestCase(unittest.TestCase):
    def test_day5a_solver(self):
        cptest = None
        def cptest_dispatch(index, tohash, hsh, password):
            if (cptest): cptest(index, tohash, hsh, password)

        def cptest3(index, tohash, hsh, password):
            if (index==5278568):
                self.assertTrue(hsh.startswith('00000f'))
                self.assertEqual(password,'18f')

                nonlocal cptest
                cptest = None
            else:
                self.assertTrue (index < 5278568)

        def cptest2(index, tohash, hsh, password):
            if (index==5017308):
                self.assertTrue(hsh.startswith('000008f82'))
                self.assertEqual(password,'18')

                nonlocal cptest
                cptest = cptest3
            else:
                self.assertTrue(index<5017308)

        def cptest1(index, tohash, hsh, password):
            if (index==3231929):

                self.assertEqual(tohash,'abc3231929')
                self.assertEqual(password,'1')

                nonlocal cptest
                cptest = cptest2
            else:
                self.assertTrue(index<3231929)

        cptest = cptest1
        password = day5a_solver('abc', cptest_dispatch)

        self.assertEqual(password,'18f47a30')


    def test_day5b_solver(self):
        cptest = None
        def cptest_dispatch(index, tohash, hsh, password):
            if (cptest): cptest(index, tohash, hsh, password)

        def cptest3(index, tohash, hsh, password):
            if (index==5357525):
                self.assertTrue(hsh.startswith('000004e'))
                self.assertEqual(password,'_5__e___')

                nonlocal cptest
                cptest = None
            else:
                self.assertTrue (index < 5357525)

        def cptest2(index, tohash, hsh, password):
            if (index==5017308):
                self.assertTrue(hsh.startswith('000008f82'))
                self.assertEqual(password,'_5______')

                nonlocal cptest
                cptest = cptest3
            else:
                self.assertTrue(index<5017308)

        def cptest1(index, tohash, hsh, password):
            if (index==3231929):

                self.assertEqual(tohash,'abc3231929')
                self.assertEqual(password,'_5______')

                nonlocal cptest
                cptest = cptest2
            else:
                self.assertTrue(index<3231929)

        cptest = cptest1
        password = day5b_solver('abc', cptest_dispatch)

        self.assertEqual(password,'05ace8e3')



if __name__ == '__main__':
    unittest.main()
