import sys
from axion.lexer import tokenization
from axion.parser import parser
from axion.interpreter import Interpreter,Env

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "run":
        print("Usage: axion run <file.ax>")
        return

    filename = sys.argv[2]

    try:
        with open(filename, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return

    try:
        tokens = tokenization(source)
        p = parser(tokens)
        ast = p.parse_program()

        env = Env()
        interpreter = Interpreter(ast)
        interpreter.global_env = env
        interpreter.run()

    except Exception as e:
        print(f"Error: {e}")
