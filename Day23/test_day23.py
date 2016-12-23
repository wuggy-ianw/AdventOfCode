import unittest

from day23 import CpuSimulator




class MyTestCase(unittest.TestCase):
    def test_toggle_example(self):
        instructions = ['cpy 2 a',
                        'tgl a',
                        'tgl a',
                        'tgl a',
                        'cpy 1 a',
                        'dec a',
                        'dec a']
        cpu = CpuSimulator(instructions)

        # check initial state
        self.assertEqual(cpu.pc, 0)
        self.assertEqual(cpu.registers, {'a': 0, 'b': 0, 'c': 0, 'd': 0})

        #cpy 2 a initializes register a to 2.
        cpu.step()
        self.assertEqual(cpu.pc, 1)
        self.assertEqual(cpu.registers, {'a': 2, 'b': 0, 'c': 0, 'd': 0})

        #The first tgl a toggles an instruction a (2) away from it, which changes the third tgl a into inc a.
        cpu.step()
        self.assertEqual(cpu.pc, 2)
        self.assertEqual(cpu.registers, {'a': 2, 'b': 0, 'c': 0, 'd': 0})

        expected = ['cpy 2 a',
                    'tgl a',
                    'tgl a',
                    'inc a',
                    'cpy 1 a',
                    'dec a',
                    'dec a']
        self.assertEqual([x.instruction for x in cpu.program], expected)

        #The second tgl a also modifies an instruction 2 away from it, which changes the cpy 1 a into jnz 1 a.
        cpu.step()
        self.assertEqual(cpu.pc, 3)
        self.assertEqual(cpu.registers, {'a': 2, 'b': 0, 'c': 0, 'd': 0})

        expected = ['cpy 2 a',
                    'tgl a',
                    'tgl a',
                    'inc a',
                    'jnz 1 a',
                    'dec a',
                    'dec a']
        self.assertEqual([x.instruction for x in cpu.program], expected)

        #The fourth line, which is now inc a, increments a to 3.
        cpu.step()
        self.assertEqual(cpu.pc, 4)
        self.assertEqual(cpu.registers, {'a': 3, 'b': 0, 'c': 0, 'd': 0})

        #Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions ahead, skipping the dec a instructions.
        cpu.step()
        self.assertEqual(cpu.pc, 7)
        self.assertEqual(cpu.registers, {'a': 3, 'b': 0, 'c': 0, 'd': 0})


if __name__ == '__main__':
    unittest.main()
