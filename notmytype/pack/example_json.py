from typing import Any, List, Dict, Union

JSONPrimitives = Union[int, str, List[Any], Dict[str, Any]]
JSONList = List[JSONPrimitives]
JSONObject = Dict[str, Union[JSONPrimitives, JSONList, Dict[str, Any]]]
JSON = Union[JSONList, JSONObject]

json_data: JSON = [
    {
        "id": 1,
        "personal_data": {"name": "Carles", "age": None},
        "children": ["Mary", "Ann", "Jim", 41],
    },
    7,
    "potato",
]

not_json_data: JSON = [
    {
        13: "potato",
        "id": 1,
        "personal_data": {"name": "Carles", "age": None},
        "children": ["Mary", "Ann", "Jim"],
    },
    7,
    "potato",
]
