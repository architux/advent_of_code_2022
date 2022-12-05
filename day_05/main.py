"""
--- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded from the ships.
Supplies are stored in stacks of marked crates,
but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks.
To ensure none of the crates get crushed or fall over,
the crane operator will rearrange them in a series of carefully-planned steps.
After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure,
but they forgot to ask her which crate will end up where,
and they want to be ready to unload them as soon as possible, so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure
(your puzzle input). For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates.
Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top.
Stack 2 contains three crates; from bottom to top, they are crates M, C, and D.
Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given.
In each step of the procedure, a quantity of crates is moved from one stack to a different stack.
In the first step of the above rearrangement procedure,
one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

In the second step, three crates are moved from stack 1 to stack 3.
Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1.
Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack;
in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3,
so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?

--- Part Two ---

As you watch the crane operator expertly rearrange the crates,
you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away.
The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features:
air conditioning, leather seats, an extra cup holder,
and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 

However, the action of moving three crates from stack 1 to stack 3
means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3

Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3

Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3

In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation
so that the Elves know where they should stand to be ready to unload the final supplies.
After the rearrangement procedure completes, what crate ends up on top of each stack?
"""
from abc import ABC, abstractmethod
from collections import deque
from re import search

from common import get_input_data


class Stack(deque):
    def __str__(self):
        return f"Stack({self})"


class StackPack:
    def __init__(self, stacks: list[Stack]):
        self.stacks = stacks

    def __str__(self):
        return f"StackPack({self.stacks})"

    def get_top_crates(self):
        return "".join([stack[-1] for stack in self.stacks])


class Movement:
    def __init__(self, instruction: str):
        self.instruction = instruction

        result = search(r"move (\d+) from (\d+) to (\d+)", instruction)
        self.crates_count,\
            self.source_stack_index,\
            self.destination_stack_index = [
                int(item) for item in result.groups()
            ]

        self.source_stack_index -= 1
        self.destination_stack_index -= 1

    def __str__(self):
        return f"StackMovement({self.instruction})"


class CrateMover(ABC):
    def __str__(self):
        return f"{__class__.__name__}()"

    @abstractmethod
    def move(self, stack_pack: StackPack, movement: Movement):
        pass

    def make_moves(self,
                   stack_pack: StackPack,
                   stack_movements: list[Movement]):
        for stack_movement in stack_movements:
            self.move(stack_pack, stack_movement)


class CrateMover9000(CrateMover):
    def move(self, stack_pack: StackPack, movement: Movement) -> StackPack:
        for _ in range(movement.crates_count):
            stack_pack.stacks[movement.destination_stack_index].append(
                stack_pack.stacks[movement.source_stack_index].pop()
            )

        return stack_pack


class CrateMover9001(CrateMover):
    def move(self, stack_pack: StackPack, movement: Movement) -> StackPack:
        intermediate_stack = Stack()

        for _ in range(movement.crates_count):
            intermediate_stack.appendleft(
                stack_pack.stacks[movement.source_stack_index].pop()
            )

        stack_pack.stacks[movement.destination_stack_index].extend(
            intermediate_stack
        )

        return stack_pack


class InputDataParser:
    @staticmethod
    def parse_stacks(input_data: list[str]) -> list[Stack]:
        parsed_segments = []

        for i, line in enumerate(input_data):
            if line and not line.startswith("move"):
                parsed_segments.append(
                    [line[i] for i in range(1, len(line), 4)]
                )
                if parsed_segments[i][0].isdigit():
                    del parsed_segments[i]

        stacks = [Stack() for _ in range(len(parsed_segments[0]))]

        for i in range(len(parsed_segments) - 1, -1, -1):
            for j in range(len(parsed_segments[i])):
                if parsed_segments[i][j].isalpha():
                    stacks[j].append(parsed_segments[i][j])

        return stacks

    @staticmethod
    def parse_movements(input_data: list[str]) -> list[Movement]:
        movements = []
    
        for instruction in input_data:
            if instruction and instruction.startswith("move"):
                movements.append(Movement(instruction))
    
        return movements


if __name__ == "__main__":
    test_data = get_input_data("test_data.txt")
    prod_data = get_input_data("prod_data.txt")

    parser = InputDataParser()

    # Parts 1 and 2
    cranes_and_tests = {
        CrateMover9000: "CMZ",  # Part 1
        CrateMover9001: "MCD",  # Part 2
    }

    for CraneClass, TEST_VALUE in cranes_and_tests.items():
        crane = CraneClass()

        test_stack_pack = StackPack(parser.parse_stacks(test_data))
        test_movements = parser.parse_movements(test_data)
        crane.make_moves(test_stack_pack, test_movements)

        assert test_stack_pack.get_top_crates() == TEST_VALUE

        prod_stack_pack = StackPack(parser.parse_stacks(prod_data))
        prod_movements = parser.parse_movements(prod_data)
        crane.make_moves(prod_stack_pack, prod_movements)

        print(prod_stack_pack.get_top_crates())
