import ast

def analyze(for_node):
    assert isinstance(for_node, ast.For)

    for node in ast.walk(for_node):
        if isinstance(node, (
            ast.If, ast.While, ast.Match,
            ast.Break, ast.Continue,
            ast.Try, ast.Raise, ast.Return,
            ast.With, ast.AsyncWith,
            ast.Await, ast.Yield, ast.YieldFrom,
            ast.AsyncFor
        )):
            return True
    return False