import unittest

from day12 import CpuSimulator

class Day12Tests(unittest.TestCase):
    def test_example(self):
        instructions = ['cpy 41 a',
                        'inc a',
                        'inc a',
                        'dec a',
                        'jnz a 2',
                        'dec a']

        cpu = CpuSimulator(instructions)

        # check initial state
        self.assertEqual(cpu.pc,0)
        self.assertEqual(cpu.registers, {'a': 0, 'b': 0, 'c': 0, 'd': 0})

        # run cpy 41 a
        cpu.step()
        self.assertEqual(cpu.pc, 1)
        self.assertEqual(cpu.registers, {'a': 41, 'b': 0, 'c': 0, 'd': 0})

        # run inc a
        cpu.step()
        self.assertEqual(cpu.pc, 2)
        self.assertEqual(cpu.registers, {'a': 42, 'b': 0, 'c': 0, 'd': 0})

        # run inc a
        cpu.step()
        self.assertEqual(cpu.pc, 3)
        self.assertEqual(cpu.registers, {'a': 43, 'b': 0, 'c': 0, 'd': 0})

        # run dec a
        cpu.step()
        self.assertEqual(cpu.pc, 4)
        self.assertEqual(cpu.registers, {'a': 42, 'b': 0, 'c': 0, 'd': 0})

        # run jnz a 2
        cpu.step()
        self.assertEqual(cpu.pc, 6)
        self.assertEqual(cpu.registers, {'a': 42, 'b': 0, 'c': 0, 'd': 0})


if __name__ == '__main__':
    unittest.main()
