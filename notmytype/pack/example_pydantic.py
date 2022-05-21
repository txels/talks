from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    "id": "123",
    "name": "Jerry",
    "signup_ts": "2019-06-01 12:22",
    "friends": [1, 2, "3"],
}
user = User(**external_data)
print(user)
# id=123 name='Jerry' signup_ts=datetime.datetime(2019, 6, 1, 12, 22) friends=[1, 2, 3]
