import unittest

from day10 import create_bots_and_bins_from_directives, perform_bots_step


class TestDay10(unittest.TestCase):
    def test_example1(self):
        directives = ['value 5 goes to bot 2',
                      'bot 2 gives low to bot 1 and high to bot 0',
                      'value 3 goes to bot 1',
                      'bot 1 gives low to output 1 and high to bot 0',
                      'bot 0 gives low to output 2 and high to output 0',
                      'value 2 goes to bot 2']

        bots_and_bins = create_bots_and_bins_from_directives(directives)

        # Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
        self.assertEqual(bots_and_bins['bot 1'].holding, [3])
        self.assertEqual(bots_and_bins['bot 2'].holding, [5, 2])

        # Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
        didstep = perform_bots_step(bots_and_bins)
        self.assertEqual(didstep, True)
        self.assertEqual(bots_and_bins['bot 2'].holding, [])
        self.assertEqual(bots_and_bins['bot 1'].holding, [3, 2])
        self.assertEqual(bots_and_bins['bot 0'].holding, [5])

        # Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
        didstep = perform_bots_step(bots_and_bins)
        self.assertEqual(didstep, True)
        self.assertEqual(bots_and_bins['bot 1'].holding, [])
        self.assertEqual(bots_and_bins['output 1'].holding, [2])
        self.assertEqual(bots_and_bins['bot 0'].holding, [5, 3])

        # Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.
        didstep = perform_bots_step(bots_and_bins)
        self.assertEqual(didstep, True)
        self.assertEqual(bots_and_bins['bot 0'].holding, [])
        self.assertEqual(bots_and_bins['output 2'].holding, [3])
        self.assertEqual(bots_and_bins['output 0'].holding, [5])

        # all done, should be no more steps
        didstep = perform_bots_step(bots_and_bins)
        self.assertEqual(didstep, False)

if __name__ == '__main__':
    unittest.main()
