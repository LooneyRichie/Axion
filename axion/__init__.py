"""
Axion Language Interpreter Package
Exposes main components for external use.
"""

__version__ = "0.1.0"
__author__ = "Axion Language Contributors"
__description__ = "A lightweight experimental programming language built in Python"

from .cli import main
from .lexer import tokenization
from .parser import parser
from .interpreter import Interpreter, Env
