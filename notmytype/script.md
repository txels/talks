# Sorry, you're not my type

What type annotations (aka type hints) are in Python, how to use them,
and goodies we can get out of them.

---

## `whoami`

I'm Carles Barrobés, a freelance Software Engineer with a special focus on Developer Enablement and Continuous Delivery.

---

## What are Type Hints

_(aka Type annotations)_

Type hints is how we tell our Python tools the types our code uses, so that tools can use this information for _interesting stuff_.

> **New in version 3.5.**
>
> The Python runtime does not enforce function and variable type annotations. They can be used by third party tools such as type checkers, IDEs, linters, etc.

Useful links:

- https://www.python.org/dev/peps/pep-0483/ an intro to type hints
- https://docs.python.org/3.8/library/typing.html the `typing` package

---

## Gradual typing

From the docs:

> Gradual typing allows one to annotate only part of a program, thus leverage desirable aspects of both dynamic and static typing.

We don't need to add type definitions everywhere!

They are optional, and we can add them where we may get the most value

---

## A very simple usage example

```python
# pack/example.py
from typing import Dict, List

def hello(name: str) -> None:
   print(f"Hello {name}")

def main():
    hello(12)
    hello({"name": "Jim"})
```

Tools: `mypy` - static analysis of type annotations

Basic usage:

```sh
$ mypy <file>.py      # single file
$ mypy -p <package>   # a python package, recursively
```

```sh
 $ mypy pack/example.py
Success: no issues found in 1 source file
```

WAT?

---

Caveats:

- By default, `mypy` will only find issues if "callee and caller" both use type hints

Options: either always use type definitions...

```python
def main() -> str:
    hello(12)
    hello({"name": "Jim"})
```

````sh
 $ mypy pack/example.py
pack/example.py:5: error: Missing return statement
pack/example.py:6: error: Argument 1 to "hello" has incompatible type "int"; expected "str"
pack/example.py:7: error: Argument 1 to "hello" has incompatible type "Dict[str, str]"; expected "str"
Found 3 errors in 1 file (checked 1 source file)```
````

---

...or use `--check-untyped-defs`

```sh
$ mypy --check-untyped-defs example.py
```

---

As type annotations, you may use:

- primitive types
- user-defined types (classes, enums, `NewType`...)
- definitions from the `typing` package: `Dict`, `List`, `Optional`...

---

## This is catchy!

We've seen that `mypy` may catch:

- Incorrect types provided to arguments
- Missing return statements

It can also catch:

- Undesired assignment of `None`
- Incorrect usage of types (e.g. missing attributes)

---

```python
# pack/example2.py
from typing import List, Optional

class Greeter:
    audience: List[str]
    greeting: str = "Hello"
    emphatic: bool

    def __init__(self, audience: List[str], emphatic: Optional[bool] = None) -> None:
        self.audience = audience
        self.emphatic = emphatic

def main() -> None:
    greeter = Greeter(["Carles", "Marta", "Joan"])
    greeter.greet()
```

---

```sh
 $ mypy pack/example2.py
pack/example2.py:11: error: Incompatible types in assignment (expression has type "Optional[bool]", variable has type "bool")
pack/example2.py:17: error: "Greeter" has no attribute "greet"; maybe "greeting"?
Found 2 errors in 1 file (checked 1 source file)
```

Fix incompatible assignment:

```python
    # mypy now sees that we are always assigning a boolean value != None
    self.emphatic = False if emphatic is None else emphatic
```

---

Let's add the missing method:

```python
# pack/example3.py - adds to example2

class Greeter:
    #...

    def greet(self) -> str:
        whom = self.audience.join(", ")
        greeting = f"{self.greeting} {whom}"
        if self.emphatic:
            greeting += ", innit!"
```

---

```sh
 $ mypy pack/example3.py
pack/example3.py:17: error: Missing return statement
pack/example3.py:18: error: "List[str]" has no attribute "join"
Found 2 errors in 1 file (checked 1 source file)
```

> ...oh boy, I will have my Python programmer license revoked :)

```python
    def greet(self) -> str:
        # whom = self.audience.join(", ")
        whom = ", ".join(self.audience)  # how could I get this wrong???
        greeting = f"{self.greeting} {whom}"
        if self.emphatic:
            greeting += ", innit!"
        return greeting  # ADDED THIS
```

---

Places where we've seen we can use type annotations:

- when defining variables
- in function parameters
- in function return types

...but we can also use them to define new types.

---

## Type aliases

```python
# pack/example4.py
from typing import Dict, List

# Let's give things meaningful names
Person = Dict[str, str]
Contacts = List[Person]


def find(addressbook: Contacts, name: str) -> Person:
    return next(p for p in addressbook if p["name"] == name)
```

---

Usage:

```python
addressbook: Contacts = [
    {
        "name": "Petra",
    },
    {
        "name": "Eloi",
    },
]

eloi: Person = find(addressbook, "Eloi")
print(eloi)
```

---

Error usage:

```python
incorrect: str = find({"name": "Eloi"}, 2)
```

```
 $ mypy --check-untyped-defs pack/example4.py
pack/example4.py:24: error: Incompatible types in assignment (expression has type "Dict[str, str]", variable has type "str")
pack/example4.py:24: error: Argument 1 to "find" has incompatible type "Dict[str, str]"; expected "List[Dict[str, str]]"
pack/example4.py:24: error: Argument 2 to "find" has incompatible type "int"; expected "str"
Found 3 errors in 1 file (checked 1 source file)
```

---

Other useful definitions in the `typing` library:

```python
# pack/example5.py
from typing import Callable, Sized

ProcessCallback = Callable[[Sized, int], bool]


def process_item(item: str, callback: ProcessCallback) -> None:
    callback(item, 3)


def suitable_callback(name: Sized, expected_len: int) -> bool:
    return len(name) == expected_len

# correct
process_item("potato", suitable_callback)
```

```python
def unsuitable_callback(name: str) -> int:
    return len(name)

# Incorrect
process_item("potato", unsuitable_callback)
```

```sh
 $ mypy --check-untyped-defs pack/example5.py
pack/example5.py:28: error: Argument 2 to "process_item" has incompatible type "Callable[[str], int]"; expected "Callable[[Sized, int], bool]"
Found 1 error in 1 file (checked 1 source file)
```

---

## Unlocking badges

Using type hints opens up new possibilities for tools, because they can be smarter about understanding your code:

- IDEs
- `dataclass` decorator - reduce boilerplate
- pydantic - data validation
- FastAPI - build HTTP APIs

---

## Dataclasses

The `dataclass` decorator (since 3.7) frees us from writing boilerplate.

[Example](pack/example_dataclass.py)

https://docs.python.org/3/library/dataclasses.html

---

## Pydantic

> Data validation and settings management using python type annotations.
> `pydantic` enforces type hints at runtime, and provides user friendly errors when data is invalid.

[Example](pack/example_pydantic.py)

https://pydantic-docs.helpmanual.io/

---

## FastAPI

> FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

Relies on `pydantic`

[Example](pack/example_fastapi.py)

https://fastapi.tiangolo.com/

---

`Any` is a placeholder for any type. It can have its uses, e.g. for unstructured data.

E.g. see pack/example_json.py

... but it can be a trap.

```python
person: Any
some_list: List[Any]
```

`mypy --disallow-any-expr` - disallow use of Any

---

# Thanks!

https://carles.barrobes.com/pro

If you could do with help with CI/CD, or making your developer teams more productive, contact me!
