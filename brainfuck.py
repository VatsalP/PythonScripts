"""
Quick simple Brainfuck interpreter

Valid brainfuck commands: ><+-.,[]
Parantheses should be balanced
Everything else is ignored
Data array is of size 30_000

Here is a Hello world program in brainfuck:
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.

Check for more info: 
https://en.wikipedia.org/wiki/Brainfuck
https://esolangs.org/wiki/brainfuck
"""
import sys

from collections import deque
from pathlib import Path


class Brainfuck:

    def __init__(self, input: str):
        self.input = input
        self.data = [0 for _ in range(0, 30_000)]
        self.pc = 0
        self.dc = 0
        self.braces = {}
    
    def set_braces(self):
        stack = deque()
        for i, c in enumerate(self.input):
            if c == '[':
                stack.append((i, c))
            elif c == ']':
                if stack:
                    k, _ = stack.pop()
                    self.braces[k] = i
                    self.braces[i] = k
                else:
                    return False
        return True if not stack else False

    def run(self):
        if self.set_braces():
            while self.pc < len(self.input):
                curr = self.input[self.pc]
                if curr == '>':
                    self.dc += 1
                elif curr == '<':
                    if self.dc > 0:
                        self.dc -= 1
                    else:
                        print("Cannot decrement data pointer below 0. Aborting...")
                        break
                elif curr == '+':
                    self.data[self.dc] += 1
                elif curr == '-':
                    self.data[self.dc] -= 1
                elif curr == '.':
                    print(f"{chr(self.data[self.dc])}")
                elif curr == ',':
                    inp = ord(input()[0])
                    if inp > 255:
                        print("Only Ascii characters allowed as input")
                        break
                    self.data[self.dc] = inp
                elif curr == '[':
                    if not self.data[self.dc]:
                        self.pc = self.braces[self.pc] + 1
                        continue
                elif curr == ']':
                    if self.data[self.dc]:
                        self.pc = self.braces[self.pc] + 1
                        continue
                self.pc += 1
        else:
            print("Unbalanced Parantheses")
            

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            brainfuck = Path(sys.argv[1])
            if brainfuck.is_file():
                with open(brainfuck, 'r') as file:
                    Brainfuck(file.read()).run()
            else:
                print(f"{brainfuck} doesn't exist!")
                sys.exit(1)
        else:
            print("Brainfuck Interpreter 1.0.1")
            print("Ctrl+c to exit")
            while True:
                inp = input("> ")
                Brainfuck(inp).run()
    except KeyboardInterrupt:
        sys.exit(0)
