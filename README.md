# PyVectorizer

**PyVectorizer** is a Python tool to analyze loops in Python code and determine whether they are vectorizable. Useful for optimizing scientific and numerical applications.

## Installation

```bash
pip install pyvectorizer
```

## Usage

```python
from pyvectorizer import is_vectorizable

code = '''
for i in range(len(a)):
    a[i] = b[i] + c[i]
'''

print(is_vectorizable(code))  # True or False
```