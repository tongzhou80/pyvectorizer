# PyVectorizer

**PyVectorizer** is a Python tool to analyze loops in Python code and determine whether they are vectorizable. Useful for optimizing scientific and numerical applications.

## Installation

```bash
pip install pyvectorizer
```

## Usage

```python
from pyvectorizer import analyze_vectorization

code = '''
for i in range(len(a)):
    a[i] = b[i] + c[i]
'''

print(analyze_vectorization(code))  # analysis result
```

## Auto Vectorization

We first rule out input loops that are not in ``proper`` form:

* Loop must be a ``for`` loop over ``range(...)``
* No nested loops
* No control flow (if, break, continue, try, etc.)
* No reassignment of the loop index variable
* No unrecognized function calls

For loops in proper form, we get into dependence analysis. Dependence analysis for scalar variables 
is kind of tricky. Array variables are always global, e.g. they reference memory locations that are 
visiable before the loop, across loop iterations, and after the loop. Per Python's language semantics,
scalar variables have function scope, i.e. a variable defined in one loop iteration is visible in the following loop iterations and after the loop. So when we write loops like this:

```python
for i in range(len(a)):
    x = b[i] + c[i]
    a[i] = x
```

The unrolled execution of the loop looks like this:

```python
x = b[0] + c[0] # S0
a[0] = x        # S1
x = b[1] + c[1] # S2
a[1] = x        # S3
...
```

Dependence analysis will have the following results:

* True dependence from S0 to S1 (and S2 to S3)
* Anti-dependence from S1 to S2
* Output dependence from S0 to S2

Despite that there are these dependences, if the value of `x` is used only within its own iteration, 
the loop can actually be vectorized. However, when `x` is used outside of its own iteration, the loop will not be vectorizable, as shown in the following example:

```python
for i in range(len(a)):
    x = b[i] + c[i]
    a[i] = x

# Use `x` somehow
... = x
```

The unrolled execution of the loop looks like this:

```python
x = b[0] + c[0] # S0

x = b[1] + c[1] # S2

... = x
```
Now S0 and S2 cannot be reordered, because their order will affect what value of `x` will be read afterwards.

Being used outside of its own iteration can also mean being used in other iterations, like this:

```python    
for i in range(len(a)):
    if i == 6:
        x = x + 1
    else:
        x = b[i] + c[i]
    a[i] = x
```

In this case, even if `x` is not used after the loop, it is used across loop iterations, so the loop cannot be vectorized.

Another simple example of using non-local scalar variables is the following code:

```python
# Define `a`
a = ...
for i in range(10):
    a = i

# Use `a` somehow
... = a
```

The loop cannot be vectorized in this case either.

So how do we determine whether a scalar variable is used only within its own iteration?

Maybe we can check the reaching definition of all statements that use the variable. If all of them are in the loop, then the variable is used only within its own iteration. The idea is that, global scalar
variables will always have a reaching definition that comes from outside the loop, like this:

```python    
for i in range(len(a)):
    if i == 6:
        x = x + 1  # This will have a reaching def from outside
    else:
        x = b[i] + c[i]
    a[i] = x
```

Besides, check if there usage of `x` after the loop.

Check if this is True with Jun.