from typing import Dict, List

# Let's give things meaningful names
Person = Dict[str, str]
Contacts = List[Person]


def find(addressbook: Contacts, name: str) -> Person:
    return next(p for p in addressbook if p["name"] == name)


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

incorrect: str = find({"name": "Eloi"}, 2)
