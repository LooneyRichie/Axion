import os
import importlib.resources
import time

class Env:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' is not defined")
    
    def declare(self, name, value=None, is_const=False):
        if name in self.vars:
            raise NameError(f"Variable '{name}' already declared in this scope")
        self.vars[name] = {"value": value, "const": is_const}

    def set(self, name, value, is_const=False):
        if name in self.vars:
            if self.vars[name]['const']:
                raise ValueError(f"Cannot reassign constant '{name}'")
            self.vars[name]['value'] = value
        elif self.parent:
            self.parent.set(name, value, is_const)
        else:
            raise NameError(f"Variable '{name}' is not defined")

    def update(self, name, value):
        if name in self.vars:
            if self.vars[name]['const']:
                raise ValueError(f"Cannot reassign constant '{name}'")
            self.vars[name]['value'] = value
        elif self.parent:
            self.parent.update(name, value)
        else:
            raise NameError(f"Variable '{name}' is not defined")

    def exists(self, name):
        if name in self.vars:
            return True
        elif self.parent:
            return self.parent.exists(name)
        return False

    def is_const(self, name):
        if name in self.vars:
            return self.vars[name]['const']
        elif self.parent:
            return self.parent.is_const(name)
        return False

    def get_value(self, name):
        if name in self.vars:
            return self.vars[name]['value']
        elif self.parent:
            return self.parent.get_value(name)
        else:
            raise NameError(f"Variable '{name}' is not defined")


class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.global_env = Env()
        self.functions = {}
        self.loaded_modules = set()
        self.base_dir = "."
        self.global_env.declare("time_now", lambda: int(time.time() * 1000))
        self.functions["time_now"] = {"builtin": True, "impl": lambda: int(time.time() * 1000)}

    def run(self):
        return self.eval_program(self.ast, self.global_env)

    def eval_program(self, program, env):
        result = None
        for stmt in program['body']:
            result = self.eval_statement(stmt, env)
        return result

    def eval_statement(self, stmt, env):
        t = stmt['type']

        if t == 'VarDecl':
            init_val = self.eval_expression(stmt['value'], env) if stmt['value'] else None
            env.declare(stmt['name'], init_val)

        elif t == 'ConstDecl':
            if stmt['value'] is None:
                raise ValueError(f"Constant '{stmt['name']}' must be initialized")
            init_val = self.eval_expression(stmt['value'], env)
            env.declare(stmt['name'], init_val, is_const=True)

        elif t == 'ExpressionStatement':
            return self.eval_expression(stmt['expr'], env)
        elif t == 'IO':
            if stmt['action'] == 'log':
                value = self.eval_expression(stmt['expr'], env)
                print(value,end="")
            elif stmt['action'] == 'input':
                message = self.eval_expression(stmt['message'], env) if 'message' in stmt else ""
                raw = input(str(message))
                try:
                    if '.' in raw:
                        value = float(raw)
                    else:
                        value = int(raw)
                except ValueError:
                    value = raw
                
                if stmt['target']['type'] == "IDENTIFIER":
                    env.set(stmt['target']['value'], value)

                elif stmt['target']['type'] == "Index":
                    if stmt['target']['target']['type'] == "IDENTIFIER":
                        varname = stmt['target']['target']['value']
                        if env.is_const(varname):
                            raise ValueError(f"Cannot modify constant '{varname}'")
                    arr = self.eval_expression(stmt['target']['target'], env)
                    idx = self.eval_expression(stmt['target']['index'], env)
                    while len(arr) <= idx:
                        arr.append(None)
                    arr[idx] = value

            
            elif stmt['action']=='logln':
                value = self.eval_expression(stmt['expr'],env)
                print(value)

        elif t == 'IfStatement':
            if self.eval_expression(stmt['condition'], env):
                return self.eval_block(stmt['body'], Env(env))
            for elseif in stmt.get('elseifs', []):
                if self.eval_expression(elseif['condition'], env):
                    return self.eval_block(elseif['body'], Env(env))
            if stmt.get('else'):
                return self.eval_block(stmt['else'], Env(env))
        elif t == 'FuncDecl':
            self.functions[stmt['name']] = stmt

        elif t == 'ReturnStatement':
            return {'type': 'return', 'value': self.eval_expression(stmt['expr'], env)}

        elif t == 'BreakStatement':
            return "Break"
        elif t == 'SkipStatement':
            return "Skip"
        elif t == 'ForLoop':
            start = self.eval_expression(stmt['start'], env)
            end = self.eval_expression(stmt['end'], env)
            step = self.eval_expression(stmt['step'], env)
            var = stmt['var']
            i = start
            while i <= end:
                loop_env = Env(env)
                loop_env.declare(var, i)
                res = self.eval_block(stmt['body'], loop_env)
                if res == "Skip":
                    i += step
                    continue
                if res == "Break":
                    break
                i += step
        elif t == 'WhileLoop':
            while self.eval_expression(stmt['condition'], env):
                res = self.eval_block(stmt['body'], Env(env))
                if res == "Break":
                    break
                if res == "Skip":
                    continue
        elif t == 'DoWhileLoop':
            while True:
                res = self.eval_block(stmt['body'], Env(env))
                if res == "Break":
                    break
                if res == "Skip":
                    continue
                if not self.eval_expression(stmt['condition'], env):
                    break

        elif t == 'MatchStatement':
            expr_value = self.eval_expression(stmt['expr'], env)
            for case in stmt['cases']:
                if self.eval_expression(case['value'], env) == expr_value:
                    return self.eval_statement(case['body'], Env(env))
            if stmt.get('else'):
                return self.eval_statement(stmt['else']['body'], Env(env))
        
        elif t == "Include":
            self.handle_include(stmt["path"], env)
            return

    def eval_block(self, block, env):
        result = None
        for stmt in block:
            result = self.eval_statement(stmt, env)
            if result == "Break":
                return "Break"
            if isinstance(result, dict) and result.get('type') == 'return':
                return result
            if result == 'Skip':
                return "Skip"
        return result
    
    def handle_include(self, path, env):
        if path in self.loaded_modules:
            return 

        code = None
        if path.endswith(".ax") or path.startswith(".") or path.startswith("/"):
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                raise RuntimeError(f"Module file not found: {path}")
            with open(abs_path, "r") as f:
                code = f.read()
        else:
            try:
                import importlib.resources
                with importlib.resources.open_text("axion.stdlib", f"{path}.ax") as f:
                    code = f.read()
            except FileNotFoundError:
                raise RuntimeError(f"Stdlib module not found: {path}")

        self.loaded_modules.add(path)

        from axion.lexer import tokenization
        from axion.parser import parser

        tokens = tokenization(code)
        p = parser(tokens)
        program = p.parse_program()

        module_interpreter = Interpreter(program)
        module_interpreter.loaded_modules = self.loaded_modules 
        module_env = Env(None)
        module_interpreter.eval_block(program['body'], module_env)
        
        def make_module_func(func_name, interpreter_instance):
            def func(*args):
                if func_name not in interpreter_instance.functions:
                    raise RuntimeError(f"Function '{func_name}' not found in module")
                func_decl = interpreter_instance.functions[func_name]
                return interpreter_instance.call_function(func_decl, args, module_env)
            return func
        module_dict = {}
        for name, val in module_env.vars.items():
            module_dict[name] = val['value']
        for func_name in module_interpreter.functions:
            module_dict[func_name] = make_module_func(func_name, module_interpreter)

        module_name = os.path.splitext(os.path.basename(path))[0]
        env.declare(module_name, module_dict)
    
    def call_function(self, func_decl, args, calling_env):
        func_env = Env(calling_env)

        func_name = func_decl['name']
        func_env.declare(func_name, lambda *a: self.call_function(func_decl, a, func_env))
        
        for pname, arg_val in zip(func_decl['params'], args):
            func_env.declare(pname, arg_val)
        
        result = self.eval_block(func_decl['body'], func_env)
        
        if isinstance(result, dict) and result.get('type') == 'return':
            return result['value']
        return result

    def eval_expression(self, expr, env):
        t = expr['type']
        if t == 'NUMBER':
            if '.' in expr['value']:
                return float(expr['value'])
            else:
                return int(expr['value'])

        elif t == 'STRING':
            raw_str = expr['value']
            result = ""
            i = 0
            while i < len(raw_str):
                if raw_str[i] == '{':
                    j = i + 1
                    while j < len(raw_str) and raw_str[j] != '}':
                        j += 1
                    if j >= len(raw_str):
                        raise Exception("Unclosed interpolation in string")

                    inner_code = raw_str[i+1:j].strip()

                    from axion.lexer import tokenization
                    from axion.parser import parser

                    inner_tokens = tokenization(inner_code)
                    inner_ast = parser(inner_tokens).parse_expression()
                    value = self.eval_expression(inner_ast, env)

                    result += str(value)
                    i = j + 1
                else:
                    result += raw_str[i]
                    i += 1
            return result

        elif t == 'IDENTIFIER':
            return env.get_value(expr['value'])
        elif t == "MemberAccess":
            obj = self.eval_expression(expr["object"], env)
            prop = expr["property"]

            if isinstance(obj, dict) and prop in obj:
                return obj[prop]
            elif hasattr(obj, prop):
                return getattr(obj, prop)
            else:
                raise RuntimeError(f"Property '{prop}' not found on {obj}")
        elif t == 'BinaryOp':
            left = self.eval_expression(expr['left'], env)
            right = self.eval_expression(expr['right'], env)
            op = expr['op']
            if op == '+': return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/': return left / right
            elif op == '%': return left % right
            elif op == '==': return left == right
            elif op == '!=': return left != right
            elif op == '<': return left < right
            elif op == '<=': return left <= right
            elif op == '>': return left > right
            elif op == '>=': return left >= right
            elif op == 'both': return left and right
            elif op == 'any': return left or right

            elif op == '&': return int(left) & int(right)
            elif op == '|': return int(left) | int(right)
            elif op == '^': return int(left) ^ int(right)
            elif op == '<<': return int(left) << int(right)
            elif op == '>>': return int(left) >> int(right)

        elif t == 'UnaryOp':
            op = expr['op']
            if op == '~':
                val = self.eval_expression(expr['expr'], env)
                return ~val
            elif op == 'invert':
                val = self.eval_expression(expr['expr'], env)
                def _to_bool(v):
                    if isinstance(v, bool):
                        return v
                    if isinstance(v, (int, float)):
                        return v != 0
                    if isinstance(v, str):
                        s = v.strip().lower()
                        if s == 'true':
                            return True
                        if s == 'false':
                            return False
                        try:
                            return float(s) != 0
                        except Exception:
                            return len(s) > 0
                    return bool(v)
                return not _to_bool(val)
            elif op == '-':
                val = self.eval_expression(expr['expr'], env)
                return -val
            else:
                raise SyntaxError(f"Unknown unary operator: {op}")

        elif t == 'Assignment':
            target = expr['target']
            value = self.eval_expression(expr['value'], env)
            op = expr['op']

            if target['type'] == "IDENTIFIER":
                name = target['value']
                if env.is_const(name):
                    raise ValueError(f"Cannot modify constant '{name}'")

                if op == '=':
                    env.update(name, value)
                elif op == '+=':
                    env.update(name, env.get_value(name) + value)
                elif op == '-=':
                    env.update(name, env.get_value(name) - value)
                elif op == '*=':
                    env.update(name, env.get_value(name) * value)
                elif op == '/=':
                    env.update(name, env.get_value(name) / value)
                elif op == '%=':
                    env.update(name, env.get_value(name) % value)
                return env.get_value(name)

            elif target['type'] == "Index":
                arr = self.eval_expression(target['target'], env)
                idx = self.eval_expression(target['index'], env)

                if target['target']['type'] == "IDENTIFIER":
                    name = target['target']['value']
                    if env.is_const(name):
                        raise ValueError(f"Cannot modify constant '{name}'")

                if op == '=':
                    while len(arr) <= idx:
                        arr.append(None)
                    arr[idx] = value
                else:
                    current = arr[idx]
                    if op == '+=': arr[idx] = current + value
                    elif op == '-=': arr[idx] = current - value
                    elif op == '*=': arr[idx] = current * value
                    elif op == '/=': arr[idx] = current / value
                    elif op == '%=': arr[idx] = current % value

                return arr[idx]

        elif t == 'Call':
            callee = expr['callee']

            if callee['type'] == 'IDENTIFIER':
                func_name = callee['value']
                
                if func_name in self.functions:
                    func_def = self.functions[func_name]
                    if func_def.get("builtin"):
                        return func_def["impl"]()
                    func_env = Env(env)

                    func_env.declare(func_name, lambda *args: self.call_function(func_def, args, func_env))

                    for pname, arg_expr in zip(func_def['params'], expr['args']):
                        func_env.declare(pname, self.eval_expression(arg_expr, env))
                    result = self.eval_block(func_def['body'], func_env)
                    if isinstance(result, dict) and result.get('type') == 'return':
                        return result['value']
                    return result

            
                
                try:
                    func = env.get_value(func_name)
                    if not callable(func):
                        raise Exception(f"Error: Variable '{func_name}' is not callable")
                    return func(*[self.eval_expression(arg, env) for arg in expr['args']])
                except NameError:
                    raise Exception(f"Error: Function '{func_name}' is not defined")

            elif callee['type'] == 'MemberAccess':
                obj = self.eval_expression(callee['object'], env)
                prop = callee['property']
                func = None
                if isinstance(obj, dict) and prop in obj:
                    func = obj[prop]
                elif hasattr(obj, prop):
                    func = getattr(obj, prop)
                if not callable(func):
                    raise Exception(f"Error: '{prop}' is not callable on {obj}")
                args = [self.eval_expression(arg, env) for arg in expr['args']]
                return func(*args)

            elif callee['type'] == 'Index':
                obj = self.eval_expression(callee['target'], env)
                idx = self.eval_expression(callee['index'], env)
                func = obj[idx]
                if not callable(func):
                    raise Exception(f"Error: Element at index {idx} is not callable")
                return func(*[self.eval_expression(arg, env) for arg in expr['args']])

            else:
                raise Exception(f"Error: Unsupported callee type {callee['type']}")

        elif t == 'ArrayLiteral':
            return [self.eval_expression(el, env) for el in expr['elements']]
        elif t == 'Index':
            arr = self.eval_expression(expr['target'], env)
            idx = self.eval_expression(expr['index'], env)
            return arr[idx]