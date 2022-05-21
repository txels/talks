from typing import Dict, List, Union


class Tomato:
    data: Dict[str, int] = {"ripeness": 3}
    friends: List[str]
    extra: Union[str, bool] = "Jim"  # or = False


me: int = 12


def best_friend(tomato: Tomato) -> str:
    return tomato.friends[0]
