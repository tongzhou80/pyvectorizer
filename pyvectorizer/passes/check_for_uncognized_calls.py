import ast

def analyze(node, recognized_funcs, recognized_packages):
    unrecognized = []
    # Walk all descendants of nodes in the loop body
    for bodynode in node.body:
        for child in ast.walk(bodynode):
            if isinstance(child, ast.Call):
                # The call could be either a direct call or a method call
                func = child.func
                if isinstance(child.func, ast.Name):
                    if func.id not in recognized_funcs:
                        unrecognized.append(func.id)
                elif isinstance(func, ast.Attribute):
                    if func.value.id not in recognized_packages or func.attr not in recognized_funcs:
                        unrecognized.append(f'{func.value.id}.{func.attr}')
    
    return unrecognized