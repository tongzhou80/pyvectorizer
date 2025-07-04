import ast

def analyze(node, name_x):
    # Walk all descendants of the node
    for child in ast.walk(node):
        if isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name) and target.id == name_x:
                    return True
    return False