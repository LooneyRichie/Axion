import sys
import argparse
from axion.lexer import tokenization
from axion.parser import parser, ParseError
from axion.interpreter import Interpreter, Env

try:
    from . import __version__
except ImportError:
    __version__ = "0.1.0"

def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="axion",
        description="Axion Programming Language Interpreter",
        epilog="Example: axion run hello.ax"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"Axion {__version__}"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug mode for detailed error information"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run an Axion program")
    run_parser.add_argument("file", help="Path to the .ax file to execute")
    
    return parser

def run_file(filename, debug=False):
    """Execute an Axion program file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        return 1
    except Exception as e:
        print(f"Error reading file: {e}")
        return 1

    try:
        tokens = tokenization(source)
        p = parser(tokens)
        ast = p.parse_program()

        env = Env()
        interpreter = Interpreter(ast)
        interpreter.global_env = env
        interpreter.run()
        return 0

    except Exception as e:
        if debug:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        return 1

def main():
    """Main entry point for the Axion CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == "run":
        return run_file(args.file, args.debug)
    
    return 0
