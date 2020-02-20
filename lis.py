"""A lispy interpreter
"""
from sys import exit

import math
import operator as op


Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)


class Env(dict):
    """Environment: with {'var': val} pairs, with outer Env
    """
    def __init__(self, parms=(), args=(), outer=None):
        super().__init__(self)
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """Return the inner most Env where var appears
        """
        return self if var in self else self.outer.find(var)

class Procedure:
    """user defined scheme procedure
    """
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return lis_eval(self.body, Env(self.parms, args, self.env))


def tokenize(chars: str) -> list:
    """Convert string of chars into a list of tokens
    """
    return chars.replace("(", " ( ").replace(")", " ) ").split()

def parse(program: str) -> Exp:
    """Read a Scheme Expr from string
    """
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens: list) -> Exp:
    """Read Exp from sequence of tokens
    """
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF")
    token = tokens.pop(0)
    if token == '(':
        result = []
        while tokens[0] != ')':
            result.append(read_from_tokens(tokens))
        tokens.pop(0)
        return result
    elif token == ')':
        raise SyntaxError("unexpected ')'")
    else:
        return atom(token)

def atom(token: str) -> Atom:
    """Number becomes int or float; everything else is a symbol
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

def standard_env() -> Env:
    """Env with some Scheme standard procedures
    """
    env = Env()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'expt': pow,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: List(x),
        'list?': lambda x: isinstance(x, List),
        'map': lambda f, x: List(map(f, x)),
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'print': print,
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
        'exit': exit,
    })
    return env

global_env = standard_env()

def lis_eval(x: Exp, env=global_env) -> Exp:
    """lis_evaluate an Exp in an env
    """
    if isinstance(x, Symbol):
        return env.find(x)[x]
    elif not isinstance(x, List):
        return x
    op, *args = x
    if op == 'quote':
        return args[0]
    elif op == 'if':
        (test, conseq, alt) = args
        exp = (conseq if lis_eval(test, env) else alt)
        return lis_eval(exp, env)
    elif op == 'define':
        (symbol, exp) = args
        env[symbol] = lis_eval(exp, env)
    elif op == 'set!':
        (symbol, exp) = args
        env.find(symbol)[symbol] = lis_eval(exp, env)
    elif op == 'lambda':
        (parms, body) = args
        return Procedure(parms, body, env)
    else:
        proc = lis_eval(x[0], env)
        vals = [lis_eval(arg, env) for arg in x[1:]]
        return proc(*vals)

def repl(prompt="lispy> "):
    """Read Eval Print Loop
    """
    print("(exit) to exit")
    while True:
        try:
            val = lis_eval(parse(input(prompt)))
            if val:
                print(schemestr(val))
        except Exception as exc:
            print(exc)

def schemestr(exp):
    """Convert Py Object back into scheme readable string
    """
    if isinstance(exp, List):
        return f"({' '.join(map(schemestr, exp))})"
    else:
        return str(exp)

if __name__ == "__main__":
    repl()
