from dataclasses import dataclass
from typing import List


@dataclass
class Greeter:
    audience: List[str]
    emphatic: bool = False
    greeting: str = "Hello"
    # @dataclass will generate for us __init__, __repr__, __eq__...


greeter = Greeter(["Carles", "Marta", "Joan"])
print(greeter)
# Greeter(audience=['Carles', 'Marta', 'Joan'], emphatic=False, greeting='Hello')
greeter2 = Greeter(["Carles", "Marta", "Joan"], greeting="Hi", emphatic=True)
print(greeter2)
# Greeter(audience=['Carles', 'Marta', 'Joan'], emphatic=True, greeting='Hi'
greeter3 = Greeter(["Carles", "Marta", "Joan"], greeting="Hello", emphatic=False)

assert greeter == greeter3
assert greeter != greeter2
