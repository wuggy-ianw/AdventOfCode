import re


class CpuInstruction_Copy_Constant(object):
    match_re = re.compile('cpy (-?[0-9]+) ([a-z])')

    @staticmethod
    def match_and_create(instruction):
        match = CpuInstruction_Copy_Constant.match_re.match(instruction)
        if not match:
            return None

        return CpuInstruction_Copy_Constant(int(match.group(1)), match.group(2))

    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def perform(self, registers):
        assert self.dest in registers
        registers[self.dest] = self.source
        return 1


class CpuInstruction_Copy_Register(object):
    match_re = re.compile('cpy ([a-z]) ([a-z])')

    @staticmethod
    def match_and_create(instruction):
        match = CpuInstruction_Copy_Register.match_re.match(instruction)
        if not match:
            return None

        return CpuInstruction_Copy_Register(match.group(1), match.group(2))

    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def perform(self, registers):
        assert self.dest in registers
        assert self.source in registers
        registers[self.dest] = registers[self.source]
        return 1


class CpuInstruction_Increment(object):
    match_re = re.compile('inc ([a-z])')

    @staticmethod
    def match_and_create(instruction):
        match = CpuInstruction_Increment.match_re.match(instruction)
        if not match:
            return None

        return CpuInstruction_Increment(match.group(1))

    def __init__(self, register):
        self.register = register

    def perform(self, registers):
        assert self.register in registers
        registers[self.register] += 1
        return 1


class CpuInstruction_Decrement(object):
    match_re = re.compile('dec ([a-z])')

    @staticmethod
    def match_and_create(instruction):
        match = CpuInstruction_Decrement.match_re.match(instruction)
        if not match:
            return None

        return CpuInstruction_Decrement(match.group(1))

    def __init__(self, register):
        self.register = register

    def perform(self, registers):
        assert self.register in registers
        registers[self.register] -= 1
        return 1


class CpuInstruction_Jump_Register_Nonzero(object):
    match_re = re.compile('jnz ([a-z]) ([a-z]|-?[0-9]+)')

    @staticmethod
    def match_and_create(instruction):
        match = CpuInstruction_Jump_Register_Nonzero.match_re.match(instruction)
        if not match:
            return None

        distance = match.group(2)
        if distance in 'abcd':
            return CpuInstruction_Jump_Register_Nonzero(match.group(1), match.group(2))
        else:
            return CpuInstruction_Jump_Register_Nonzero(match.group(1), int(match.group(2)))

    def __init__(self, source, distance):
        self.source = source
        self.distance = distance

    def perform(self, registers):
        if registers[self.source] != 0:
            if type(self.distance) == int:
                return self.distance
            else:
                return registers[self.distance]
        return 1

class CpuInstruction_Jump_Constant_Nonzero(object):
    match_re = re.compile('jnz ([0-9]+) ([a-z]|-?[0-9]+)')

    @staticmethod
    def match_and_create(instruction):
        match = CpuInstruction_Jump_Constant_Nonzero.match_re.match(instruction)
        if not match:
            return None

        distance = match.group(2)
        if distance in 'abcd':
            return CpuInstruction_Jump_Constant_Nonzero(match.group(1), match.group(2))
        else:
            return CpuInstruction_Jump_Constant_Nonzero(match.group(1), int(match.group(2)))

    def __init__(self, source, distance):
        self.source = source
        self.distance = distance

    def perform(self, registers):
        if self.source != 0:
            if type(self.distance) == int:
                return self.distance
            else:
                return registers[self.distance]
        return 1


class CpuSimulator(object):
    def __init__(self, instructions, initialregisters = None):
        self.program = self.parse_program(instructions)
        if initialregisters:
            self.registers = initialregisters
        else:
            self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.pc = 0

    instruction_types = [CpuInstruction_Copy_Constant, CpuInstruction_Copy_Register, CpuInstruction_Increment, CpuInstruction_Decrement, CpuInstruction_Jump_Register_Nonzero, CpuInstruction_Jump_Constant_Nonzero ]
    def parse_instruction(self, instruction):
        # find the first matching instruction
        match = None
        for it in self.instruction_types:
            match = it.match_and_create(instruction)
            if match:
                break
        return match

    def parse_program(self, instructions):
        program = []
        for instruction in instructions:
            match = self.parse_instruction(instruction)
            assert match, "Instruction didn't match any known?"

            program.append(match)
        return program

    def step(self):
        self.pc += self.program[self.pc].perform(self.registers)

    def run(self):
        while self.pc < len(self.program):
            self.step()


def day12a_solver(instructions, initialregisters = None):
    cpu = CpuSimulator(instructions, initialregisters)
    cpu.run()

    return cpu.registers['a']

def day12b_solver(instructions):
    return day12a_solver(instructions, {'a': 0, 'b': 0, 'c': 1, 'd': 0})

if __name__ == '__main__':
    with(open('input_12a.txt', 'r')) as infile:
        instructions = infile.read().splitlines()

    print(day12a_solver(instructions))
    print(day12b_solver(instructions))

