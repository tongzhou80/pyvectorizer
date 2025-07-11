import ast
import copy
from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class VectorizationResult:
    is_vectorizable: bool
    fail_reason: Optional[str] = None
    dependencies: list = None

class AugAssignExpander(ast.NodeTransformer):
    def visit_AugAssign(self, node):
        target_copy = copy.deepcopy(node.target)
        target_copy.ctx = ast.Load()
        newnode = ast.Assign(
            targets=[node.target], 
            value=ast.BinOp(
                left=target_copy, 
                op=node.op, 
                right=node.value
            ),
            lineno=node.lineno,
        )
        ast.fix_missing_locations(newnode)
        return newnode
    
def analyze_vectorization(code_or_ast: Union[str, ast.AST]) -> VectorizationResult:
    try:
        if isinstance(code_or_ast, str):
            tree = ast.parse(code_or_ast).body[0]
        else:
            tree = code_or_ast
    except SyntaxError:
        return VectorizationResult(is_vectorizable=False, fail_reason="SyntaxError")
    
    # Check if `tree` is an ast.For
    if not isinstance(tree, ast.For):
        return VectorizationResult(is_vectorizable=False, fail_reason="Not a for loop")

    tree = AugAssignExpander().visit(tree)

    from .passes import has_nested_loops
    if has_nested_loops.analyze(tree):
        return VectorizationResult(is_vectorizable=False, fail_reason="Nested loops")

    from .passes import has_control_flows
    if has_control_flows.analyze(tree):
        return VectorizationResult(is_vectorizable=False, fail_reason="Control flow")
    
    # get the index var of loop `tree`
    index_var = tree.target.id

    from .passes import has_assign_to_name_x
    if has_assign_to_name_x.analyze(tree, index_var):
        return VectorizationResult(is_vectorizable=False, fail_reason="Assign to index var")
    
    from .passes import check_for_uncognized_calls
    SAFE_FUNCS = [
        "sin", "cos", "tan", "exp", "log", "log10", "sqrt", "abs",
        "maximum", "minimum", "sum", "mean", "std", "floor", "ceil",
    ]
    SAFE_PACKAGES = ["math"]
    unrecognized_calls = check_for_uncognized_calls.analyze(tree, SAFE_FUNCS, SAFE_PACKAGES)
    if unrecognized_calls:
        return VectorizationResult(is_vectorizable=False, fail_reason=f"Unrecognized calls: {', '.join(unrecognized_calls)}")

    return VectorizationResult(is_vectorizable=True)

