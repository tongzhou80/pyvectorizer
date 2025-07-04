import ast

def analyze(node):
    # Walk all descendants of the node
    for child in ast.walk(node):
        if isinstance(child, (ast.For, ast.While)):
            # Make sure it's not the node itself (to avoid false positive)
            if child is not node:
                return True
    return False