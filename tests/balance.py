from typing import List, Optional
from pydantic import BaseModel
import math

asks = []
votes = []
tx = []
balances = {}

class Tx(BaseModel):
    debit: str
    credit: str
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
    print(f'Balance ({addr_balance(addr)}) / Emission ({emission()})')
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
            print(f'{ask.addr} ask {ask.id} for {ask.amount}')
            balance = 0
            for vote in ask_votes(id):
                print('------')
                print(f'Vote from: {vote}')
                k = addr_karma(vote)
                print(f'Karma: {k}')
                balance += ask.amount * k
                print('------')
            print(f'{ask.id} ask balance: {math.floor(balance)}')
            return math.floor(balance)

def addr_current_balance(addr: str):
    asks = addr_asks(addr)
    b = 1
    for ask in asks:
        b += ask_balance(ask)
    return b

def calc_balances():
    for a in balances:
        print('---')
        b = addr_current_balance(a)
        balances.update({a: b})
        print(a, b)
        print('---')
class Person:
    def __init__(self, addr: str):
        balances.update({addr: 1})
        self.addr = addr
        
    def ask(self, id: str, amount: int):
        asks.append(Ask(addr=self.addr, id=id, amount=amount))

    def vote(self, id: str):
        votes.append(Vote(addr=self.addr, id=id))

    def send(self, addr, amount):
        tx.append(Tx(debit=addr, credit = self.addr, amount=amount))

a = Person(addr = 'Foundation')
b = Person(addr = 'Bob')
c = Person(addr = 'Alice')
a.ask('1', 21000)
a.vote('1')
c.vote('1')

b.ask('2', 1200)
a.vote('2')

c.ask('3', 2400)
c.vote('3')

a.ask('4', 10000)
b.vote('4')

a.send('Bob', 100)

for i in range(10):
    calc_balances()

print('Asks:', asks)
print('Votes:', votes)
print('Tx:', tx)

print('Balances:', balances)
print('Emission:', emission())
