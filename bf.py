"""
Brainfuck interpreter/transpiler using parsita a parser combinator library for parsing

pip install parsita

❯ python bf.py -h
usage: bf.py [-h] [-t] [filename]

BF transpiler/interpreter Use without any options for repl

positional arguments:
  filename          file to use

optional arguments:
  -h, --help        show this help message and exit
  -t, --transpiler  Transpile given bf sourcecode to c sourcecode
"""
import sys

from parsita import *
import parsita.util as util


class BrainfuckParser(TextParsers, whitespace=r'[^><+-.,\[\]]*'):
    left = lit('<')
    right = lit('>')
    plus = lit('+')
    minus = lit('-')
    dot = lit('.')
    comma = lit(',')

    opcode = left | right | plus | minus | dot | comma
    statement = opcode | lit('[') >> rep(statement) << lit(']')
    entry = rep(statement)

class Brainfuck:

    def __init__(self, sourcecode):
        self.code = BrainfuckParser.entry.parse(sourcecode)
        if isinstance(self.code, Failure):
            raise SyntaxError("Unmatched Brackets")
        self.array = [0] * 30000
        self.data_pointer = 0
    
    def evaluate(self, code):
        pc = 0
        while pc < len(code):
            ch = code[pc]
            if isinstance(ch, list):
                while self.array[self.data_pointer]:
                    self.evaluate(ch)
            elif ch == '>':
                self.data_pointer += 1
            elif ch == '<':
                self.data_pointer -= 1
            elif ch == '+':
                self.array[self.data_pointer] += 1
            elif ch == '-':
                self.array[self.data_pointer] -= 1
            elif ch == '.':
                print(chr(self.array[self.data_pointer]), end="")
            elif ch == ',':
                inp = ord(sys.stdin.read(1))
                self.array[self.data_pointer] = inp
            pc += 1
    
    def transpile(self):
        """transpiles the sourcecode to c code and returns as string
        """
        c_code = [
"""
#include <stdio.h>

int main () {
    char array[30000] = {0};
    char *ptr = array;
"""
        ]
        def helper(ch, tab=1):
            tabs = " " * (tab * 4)
            if isinstance(ch, list):
                s = f"{tabs}while (*ptr) {{\n"
                for token in ch:
                    s += helper(token, tab + 1)
                s += f"{tabs}}}\n"
                return s
            elif ch == '>':
                return f"{tabs}++ptr;\n"
            elif ch == '<':
                return f"{tabs}--ptr;\n"
            elif ch == '+':
                return f"{tabs}++*ptr;\n"
            elif ch == '-':
                return f"{tabs}--*ptr;\n"
            elif ch == '.':
                return f"{tabs}putchar(*ptr);\n"
            elif ch == ',':
                return f"{tabs}*ptr=getchar();\n"
        for token in self.code.value:
            c_code.append(helper(token))
        c_code.append("}")
        return "".join(c_code)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="BF transpiler/interpreter\nUse without any options for repl")
    parser.add_argument('-t', '--transpiler', action='store_true', help="Transpile given bf sourcecode to c sourcecode")
    parser.add_argument('filename', nargs='?', default='', help='file to use')
    args = parser.parse_args()

    if args.transpiler == True:
        if args.filename == '':
            print("Need a file to transpile")
        else:
            with open(args.filename) as file:
                output = Brainfuck(file.read()).transpile()
                with open(args.filename + ".c", 'w') as out:
                    out.write(output)
    elif args.filename != '':
        with open(args.filename) as file:
            bf = Brainfuck(file.read())
            bf.evaluate(bf.code.value)
    else:
        while True:
            try:
                bf = Brainfuck(input(">> "))
                bf.evaluate(bf.code.value)
            except SyntaxError as e:
                print(e)
            except KeyboardInterrupt:
                print()
                print("see ya")
                sys.exit()
            print()