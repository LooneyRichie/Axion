import re
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Token:
    """Represents a token with position information for better error reporting."""
    value: str
    type: str
    line: int
    column: int

def token_identification(token):
    """Identify the type of a token."""
    keywords = {
        'if', 'else', 'while', 'return', 'func', 'set', 'const', 'then', 
        'loop', 'from', 'to', 'step', 'do', 'match', 'case', 'default', 
        'break', 'repeat', 'input', 'log', 'logln', 'skip', 'include'
    }
    operators = {
        '+', '-', '*', '/', '=', '%', '==', '!=', '<', '>', '<=', '>=', 
        'both', 'any', 'invert', '+=', '-=', '*=', '/=', '%=', '->', 
        '&', '|', '^', '<<', '>>', '~'
    }
    punctuation = {'.', ',', ';', '(', ')', '{', '}', '[', ']'}

    if token in keywords:
        return 'KEYWORD'
    elif token.isidentifier():
        return 'IDENTIFIER'
    elif token.replace('.', '', 1).isdigit():  # Handle floats
        return 'NUMBER'
    elif (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
        return 'STRING'
    elif token in operators:
        return 'OPERATOR'
    elif token in punctuation:
        return 'PUNCTUATION'
    else:
        return 'UNKNOWN'

def tokenization(source_code: str) -> List[Token]:
    """
    Tokenize source code with position tracking for better error reporting.
    
    Args:
        source_code: The source code to tokenize
        
    Returns:
        List of Token objects with position information
    """
    # Enhanced regex pattern with better number handling and comment support
    token_pattern = r'''
        (?P<COMMENT>//.*?(?=\n|$)|/\*.*?\*/)              |  # Comments
        (?P<NUMBER>\d+(?:\.\d+)?)                          |  # Numbers (int/float)
        (?P<IDENTIFIER>[a-zA-Z_]\w*)                       |  # Identifiers
        (?P<STRING>"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')    |  # Strings
        (?P<OPERATOR><<=|>>=|<<|>>|<=|>=|==|!=|both|any|invert|[+\-*/%=<>!&|^~]+) |  # Operators
        (?P<PUNCTUATION>[.,;(){}\[\]])                     |  # Punctuation
        (?P<WHITESPACE>\s+)                                |  # Whitespace
        (?P<ERROR>.)                                          # Any other character
    '''
    
    tokens = []
    line_num = 1
    line_start = 0
    
    for match in re.finditer(token_pattern, source_code, re.VERBOSE | re.DOTALL):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start + 1
        
        if kind == 'WHITESPACE':
            # Count newlines to track line numbers
            if '\n' in value:
                line_num += value.count('\n')
                line_start = match.end() - len(value.split('\n')[-1])
            continue
        elif kind == 'COMMENT':
            # Skip comments but track newlines
            if '\n' in value:
                line_num += value.count('\n')
                line_start = match.end() - len(value.split('\n')[-1])
            continue
        elif kind == 'ERROR':
            raise SyntaxError(f"Unexpected character '{value}' at line {line_num}, column {column}")
        
        # Determine the actual token type
        if kind == 'IDENTIFIER':
            token_type = token_identification(value)
        else:
            token_type = kind
            
        tokens.append(Token(value, token_type, line_num, column))
    
    return tokens
