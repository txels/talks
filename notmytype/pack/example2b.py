from typing import List, Optional


def hello(name: str) -> None:
    print(f"Hello {name}")


class Greeter:
    audience: List[str]
    greeting: str = "Hello"
    emphatic: bool

    def __init__(self, audience: List[str], emphatic: Optional[bool] = None) -> None:
        self.audience = audience
        self.emphatic = False if emphatic is None else emphatic

    def greet(self) -> str:
        whom = self.audience.join(", ")
        greeting = f"{self.greeting} {whom}"
        if self.emphatic:
            greeting += ", innit!"


greeter = Greeter(["Carles", "Marta", "Joan"])
greeter.greet()
