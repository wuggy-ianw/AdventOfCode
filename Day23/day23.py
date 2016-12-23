from Day12 import day12 as day12
import re

def Extend_Cpu_Instruction_Class_With_Togglable_Extension(base_class):
    # define a new class, inherited from the base class, which includes methods used
    # for togglability

    class C(base_class):
        @staticmethod
        def match_and_create(instruction):
            obj = base_class.match_and_create(instruction)
            if obj:
                obj = C(instruction, obj)

            return obj

        def __init__(self, instruction, base):
            self.__dict__ = base.__dict__.copy()
            self.instruction = instruction

        def perform(self, cpu_state):
            return base_class.perform(self, cpu_state.registers)

    return C

CpuInstruction_Copy_Constant = Extend_Cpu_Instruction_Class_With_Togglable_Extension(day12.CpuInstruction_Copy_Constant)
CpuInstruction_Copy_Register = Extend_Cpu_Instruction_Class_With_Togglable_Extension(day12.CpuInstruction_Copy_Register)
CpuInstruction_Increment = Extend_Cpu_Instruction_Class_With_Togglable_Extension(day12.CpuInstruction_Increment)
CpuInstruction_Decrement = Extend_Cpu_Instruction_Class_With_Togglable_Extension(day12.CpuInstruction_Decrement)
CpuInstruction_Jump_Register_Nonzero = Extend_Cpu_Instruction_Class_With_Togglable_Extension(day12.CpuInstruction_Jump_Register_Nonzero)
CpuInstruction_Jump_Constant_Nonzero = Extend_Cpu_Instruction_Class_With_Togglable_Extension(day12.CpuInstruction_Jump_Constant_Nonzero)


class CpuInstruction_Skipped_Invalid(object):
    def __init__(self, instruction):
        self.instruction = instruction

    def perform(self, cpu_state):
        # do nothing, just increment the pc
        return 1

class CpuInstruction_Toggle_Register(object):
    match_re = re.compile(r'tgl ([a-z])')

    @staticmethod
    def match_and_create(instruction):
        match = CpuInstruction_Toggle_Register.match_re.match(instruction)
        if not match:
            return None

        return CpuInstruction_Toggle_Register(instruction, match.group(1))

    def __init__(self, instruction, dest):
        self.instruction = instruction
        self.dest = dest

    toggle_translation = {'inc': 'dec', 'dec': 'inc', 'tgl': 'inc',
                          'jnz': 'cpy', 'cpy': 'jnz'}

    def perform(self, cpu_state):
        # get the instruction index to modify in the program
        index = cpu_state.pc + cpu_state.registers[self.dest]

        # if the index is within the bounds of the program
        if index >= 0 and index < len(cpu_state.program):
            # toggle the text of it's instruction
            instruction_text = cpu_state.program[index].instruction
            toggled_instruction_text = None
            for k,v in self.toggle_translation.items():
                if instruction_text.startswith(k):
                    toggled_instruction_text = v + instruction_text[len(k):]
                    break

            assert toggled_instruction_text, "Unknown instruction encountered?"

            # try and parse the instruction text
            toggled_instruction = cpu_state.parse_instruction(toggled_instruction_text)

            # if this didn't match any instruction, make it a skipped instruction
            if not toggled_instruction:
                toggled_instruction = CpuInstruction_Skipped_Invalid(toggled_instruction_text)

            # replace the instruction in our program
            cpu_state.program[index] = toggled_instruction

        return 1


class CpuSimulator(day12.CpuSimulator):
    instruction_types = [CpuInstruction_Copy_Constant, CpuInstruction_Copy_Register, CpuInstruction_Increment,
                         CpuInstruction_Decrement, CpuInstruction_Jump_Register_Nonzero,
                         CpuInstruction_Jump_Constant_Nonzero, CpuInstruction_Toggle_Register]
                        # don't include the 'skip invalid'... only toggling an instruction should generate that

    def __init__(self, instructions, initialregisters = None, loop_optimisers = None):
        super(CpuSimulator, self).__init__(instructions, initialregisters)

        self.debug = False
        if loop_optimisers:
            self.loop_optimisers = loop_optimisers
        else:
            self.loop_optimisers = {}

    def step(self):
        if self.pc in self.loop_optimisers:
            self.pc += self.loop_optimisers[self.pc](self)
        else:
            self.pc += self.program[self.pc].perform(self)

        if self.debug:
            print(self.registers)
            for i,l in enumerate(self.program):
                print('>' if self.pc == i else ' ', l.instruction)
            print()


def optimiser_for_slow_multiply_loop(cpustate):
    # our code contains a few loops that have a simplifiable effect (mostly multiplication
    # this loop starts at 'l' and ends at the jnz 1 c instruction...
    # because the effect of toggling might be complicated, I've not tried to simplify the whole loop
    # but at least the inner parts between the loop start 'l' and the 'tgl' instruction
    #
    # cpy a b
    # dec b
    # l -->cpy a d  d' = a														}
    # cpy 0 a  a' = 0															}
    # cpy b c   }            }													}
    # inc a     }            }													}
    # dec c     }            }													}
    # jnz c -2  } c=0 a+=b   }													}
    # dec d                  }													}
    # jnz d -5               } a=b*d c=0 d=0 ...  a'' = b * d' c'=0 d''=0		}
    # dec b     b' = b - 1	    												}
    # cpy b c   				}												}
    # cpy c d   				}												} a'' = b * a
    # dec d     }				}												} b' = b - 1
    # inc c     }				}												} c'' = b' * 2
    # jnz d -2  } c+=d d=0		} c'' = b'*2 d'''=0	    				    	} d''' = 0
    # tgl c
    # cpy -16 c
    # jnz 1 c   c -> l      ... this will be terminated by when some instruction is toggled, probably this or the cpy above
    # cpy 81 c
    # jnz 93 d
    # inc a
    # inc d
    # jnz d -2
    # inc c
    # jnz c -5
    #
    # so we can collapse the big loop at least

    a, b, c, d = cpustate.registers['a'], cpustate.registers['b'], cpustate.registers['c'], cpustate.registers['d']

    cpustate.registers['a'] = b * a
    cpustate.registers['b'] = b - 1
    cpustate.registers['c'] = (b - 1) * 2
    cpustate.registers['d'] = 0

    return 14       # this optimised chunk is 14 instructions long

default_loop_optimisers = {2: optimiser_for_slow_multiply_loop}



def day23a_solver(instructions, initialregisters = None, loop_optimisers = None):
    if not initialregisters:
        initialregisters = {'a': 7, 'b': 0, 'c': 0, 'd': 0}

    cpu = CpuSimulator(instructions, initialregisters, loop_optimisers)
    cpu.run()

    return cpu.registers['a']


def day23a_solver_loop_optimised(instructions):
    return day23a_solver(instructions, loop_optimisers=default_loop_optimisers)




def day23b_solver(instructions):
    return day23a_solver(instructions, {'a': 12, 'b': 0, 'c': 0, 'd': 0})



def day23b_solver_loop_optimised(instructions):
    return day23a_solver(instructions, {'a': 12, 'b': 0, 'c': 0, 'd': 0}, loop_optimisers=default_loop_optimisers)




if __name__ == '__main__':
    with(open('input_23a.txt', 'r')) as infile:
        instructions = infile.read().splitlines()

    #print(day23a_solver(instructions))
    print(day23a_solver_loop_optimised(instructions))

    #print(day23b_solver(instructions)) # this runs terribly slowly
    print(day23b_solver_loop_optimised(instructions))



