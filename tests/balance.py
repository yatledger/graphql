from typing import List, Optional
from pydantic import BaseModel
import math

asks = []
votes = []
balances = {}

class Balance(BaseModel):
    addr: str
    amount: int

class Ask(BaseModel):
    id: str
    addr: str
    amount: int

class Vote(BaseModel):
    addr: str
    id: str

def emission() -> int:
    return int(sum(balances.values()))

def addr_balance(addr: str) -> int:
    return balances.get(addr)

def addr_asks(addr: str) -> List:
    a = []
    for ask in asks:
        if ask.addr == addr:
            a.append(ask.id)
    return a

def addr_karma(addr: str) -> int:
    return addr_balance(addr) / emission()

def ask_votes(id: str) -> List:
    v = []
    for vote in votes:
        if vote.id == id:
            v.append(vote.addr)
    return v
    #return [list(votes.keys())[list(votes.values()).index(id)]]
    #return votes.keys()[votes.values().index(id)]
    #return [list(votes.values()).index(id)]
    #[votes.values().index(id)]

def ask_balance(id: str) -> int:
    for ask in asks:
        if ask.id == id:
            print('Ask ammount:', ask.amount)
            print('Ask votes:', ask_votes(id))
            balance = 0
            for vote in ask_votes(id):
                print('Vote from:', vote, '| Karma:', addr_karma(vote))
                balance += ask.amount * addr_karma(vote)
            return math.floor(balance)

def addr_set_balance(addr: str):
    asks = addr_asks(addr)
    b = 0
    for ask in asks:
        b += ask_balance(ask)
    return b


class Person:
    def __init__(self, addr: str):
        self.balance = 0
        self.addr = addr
        balances.update({addr: 1})
    def ask(self, id: str, amount: int):
        asks.append(Ask(addr=self.addr, id=id, amount=amount))
    def vote(self, id: str):
        votes.append(Vote(addr=self.addr, id=id))

a = Person(addr = 'Foundation')
print('Emission:', emission())
a.ask('first', 21000)
a.vote('first')
print('Asks:', asks)
print('Votes:', votes)
a.balance = addr_set_balance('Foundation')
print('First ask balance:', a.balance)
balances.update({a.addr: a.balance})
print(addr_balance(a.addr))
print('-------')
b = Person(addr = 'John')
print('Emission:', emission())
b.ask('second', 1200)
a.vote('second')
print('Asks:', asks)
print('Votes:', votes)
b.balance = addr_set_balance('John')
print('Second ask balance:', b.balance)
balances.update({b.addr: b.balance})
print('John balance', addr_balance(b.addr))
print('-------')
c = Person(addr = 'Liza')
print('Emission:', emission())
c.ask('third', 2400)
c.vote('third')
b.vote('third')
print('Asks:', asks)
print('Votes:', votes)
c.balance = addr_set_balance('Liza')
print('Third ask balance:', c.balance)
balances.update({c.addr: c.balance})
print('Liza balance', addr_balance(c.addr))
print('-------')
print('Emission:', emission())
