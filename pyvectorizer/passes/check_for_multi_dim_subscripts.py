import ast

def analyze(node):
    for child in ast.walk(node):
        if isinstance(child, ast.Subscript):
            if isinstance(child.slice, ast.Tuple):
                return True
    return False