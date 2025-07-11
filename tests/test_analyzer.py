import pytest
from pyvectorizer import analyze_vectorization


def test_simple_vectorizable_loop():
    code = """
for i in range(10):
    a[i] = b[i] + 1
"""
    result = analyze_vectorization(code)
    assert result.is_vectorizable


def test_nested_loop_not_vectorizable():
    code = """
for i in range(10):
    for j in range(10):
        a[i] = b[j]
"""
    result = analyze_vectorization(code)
    assert not result.is_vectorizable


def test_control_flow_not_vectorizable():
    code = """
for i in range(10):
    if a[i] > 0:
        a[i] = b[i]
"""
    result = analyze_vectorization(code)
    assert not result.is_vectorizable


def test_loop_var_reassignment_not_vectorizable():
    code = """
for i in range(10):
    i = i + 1
    a[i] = b[i]
"""
    result = analyze_vectorization(code)
    assert not result.is_vectorizable


def test_index_not_loop_var_not_vectorizable():
    code = """
for i in range(10):
    a[i + 1] = b[i]
"""
    result = analyze_vectorization(code)
    assert not result.is_vectorizable


def test_unrecognized_function_call_not_vectorizable():
    code = """
for i in range(10):
    a[i] = custom_func(b[i])
"""
    result = analyze_vectorization(code)
    assert not result.is_vectorizable


def test_recognized_function_call_vectorizable():
    code = """
for i in range(10):
    a[i] = math.log(b[i])
"""
    result = analyze_vectorization(code)
    print(result)  # Optional: pytest captures stdout by default
    assert result.is_vectorizable


def test_augassign_vectorizable():
    code = """
for i in range(10):
    a[i] += 1
"""
    result = analyze_vectorization(code)
    assert result.is_vectorizable


def test_scalar():
    code = """
for i in range(10):
    x = s + a[i]
    s = x
"""
    result = analyze_vectorization(code)
    assert result.is_vectorizable
