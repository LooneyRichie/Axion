def token_identification(token):
    keywords = {'if', 'else', 'while', 'return', 'func', 'set', 'const', 'then', 'loop', 'from', 'to', 'step', 'do', 'match', 'case', 'default', 'break', 'repeat', 'input', 'log','logln','skip','include'}
    operators = {'+', '-', '*', '/', '=','%', '==', '!=', '<', '>', '<=', '>=', 'both', 'any', 'invert', '+=', '-=', '*=', '/=', '%=', '->','&','|','^','<<','>>','~'}
    punctuation = {'.', ',', ';', '(', ')', '{', '}', '[', ']'}

    if token in keywords:
        return 'KEYWORD'
    elif token.isidentifier():
        return 'IDENTIFIER'
    elif token.isdigit():
        return 'NUMBER'
    elif (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
        return 'STRING'
    elif token in operators:
        return 'OPERATOR'
    elif token in punctuation:
        return 'PUNCTUATION'
    else:
        return 'UNKNOWN'


def tokenization(source_code):
    import re
    token_pattern = r'\s*(?:(\d+(\.\d+)?)|([a-zA-Z_]\w*)|(".*?")|(\'.*?\')|(<<=|>>=|<<|>>|<=|>=|==|!=|both|any|invert|[+\-*/%=<>!&|^~]+)|([.,;(){}\[\]]))'
    tokens = []

    for match in re.finditer(token_pattern, source_code):
        groups = match.groups()
        number = groups[0]
        identifier = groups[2]
        double_quoted = groups[3]
        single_quoted = groups[4]
        operator = groups[5]
        punct = groups[6]
        if number:
            tokens.append((number, 'NUMBER'))
        elif identifier:
            token_type = token_identification(identifier)
            tokens.append((identifier, token_type))
        elif double_quoted:
            tokens.append((double_quoted, 'STRING'))
        elif single_quoted:
            tokens.append((single_quoted, 'STRING'))
        elif operator:
            tokens.append((operator, 'OPERATOR'))
        elif punct:
            tokens.append((punct, 'PUNCTUATION'))

    return tokens
