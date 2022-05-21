from dataclasses import dataclass, field
from typing import List


@dataclass(order=True, frozen=True)
class TomatoOwner:
    tomatoes: int
    name: str
    serialnumbers: List[int] = field(default_factory=list)


me = TomatoOwner(12, "Carles")
me.serialnumbers.append([1, 2, 3])
my_wife = TomatoOwner(0, "Marta")
a_competitor = TomatoOwner(12, "Jane")

print(sorted([me, my_wife, a_competitor]))
# [
#  TomatoOwner(tomatoes=0, name='Marta', serialnumbers=[]),
#  TomatoOwner(tomatoes=12, name='Carles', serialnumbers=[[1, 2, 3]]),
#  TomatoOwner(tomatoes=12, name='Jane', serialnumbers=[])
# ]
