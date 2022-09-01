from typing import Optional
from pydantic import BaseModel, PositiveInt

class Tx(BaseModel):
    credit: str
    debit: str
    amount: PositiveInt
    uniq: str
    sign: str
    type: Optional[int] = 0
    msg: Optional[str] = ''
    time: Optional[int]
    hash: Optional[str]

class UserContent(BaseModel):
    addr: str
    req: str
    time: int
    content: str
    sign: str

class User(BaseModel):
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]