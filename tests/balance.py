from typing import List, Optional
from pydantic import BaseModel
import math
import time

import logging
logfmt = '%(message)s'
#TODO: %(asctime)s - %(levelname)s - %(message)s
#formatTime(record, datefmt=None)
#loghdlrs = [logging.FileHandler('chain.log'), logging.StreamHandler()]
logging.basicConfig(level=logging.INFO, format=logfmt) #handlers=loghdlrs

asks = []
votes = []
tx = []
users = []
balances = {}
netto = {}

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
    return int(sum(balances.values()) or 1)

def addr_balance(addr: str) -> int:
    return int(balances.get(addr) or 1)

def addr_asks(addr: str) -> List:
    a = []
    for ask in asks:
        if ask.addr == addr:
            a.append(ask.id)
    return a

def addr_karma(addr: str) -> int:
    #print(f'Balance ({addr_balance(addr)}) / Emission ({emission()})')
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
            #print(f'{ask.addr} ask {ask.id} for {ask.amount}')
            balance = 0
            for vote in ask_votes(id):
                #print('------')
                #print(f'Vote from: {vote}')
                k = addr_karma(vote)
                #print(f'Karma: {k}')
                balance += ask.amount * k
                #print('------')
            #print(f'{ask.id} ask balance: {math.floor(balance)}')
            return math.floor(balance)

def addr_current_balance(addr: str):
    asks = addr_asks(addr)
    b = 1
    for ask in asks:
        b += ask_balance(ask)
    return b + int(netto.get(addr) or 0)

def calc_balances():
    print('Pre balances:', balances)
    for i in range(3):
        for u in users:
            #print('---')
            b = addr_current_balance(u)
            balances.update({u: b})
            #print('---')
        print(f'{i} balances: {balances}')
    print('Post balances:', balances)
class Person:
    def __init__(self, addr: str):
        users.append(addr)
        print('Person:', addr)
        self.addr = addr
        
    def ask(self, id: str, amount: int):
        #balances.update({self.addr: 1})
        logging.info(f"{time.time_ns()} Ask(addr={self.addr}, id={id}, amount={amount})")
        asks.append(Ask(addr=self.addr, id=id, amount=amount))

    def vote(self, id: str):
        logging.info(f"{time.time_ns()} Vote(addr={self.addr}, id={id})")
        votes.append(Vote(addr=self.addr, id=id))

    def send(self, addr, amount):
        logging.info(f"{time.time_ns()} Tx(debit={addr}, credit = {self.addr}, amount={amount})")
        tx.append(Tx(debit=addr, credit = self.addr, amount=amount))

def calc_tx():
    for t in tx:
        c = netto.get(t.credit)
        d = netto.get(t.debit) #if None -> 0
        #print(c, d)
        netto.update({t.credit: int(c or 0) - t.amount})
        netto.update({t.debit: int(d or 0) + t.amount})

a = Person(addr = 'Foundation')

a.ask('1', 21000)
print(asks)
calc_balances()
a.vote('1')
calc_balances()

c = Person(addr = 'Alice')
c.vote('1')
calc_balances()

b = Person(addr = 'Bob')
b.ask('2', 1200)
calc_balances()
a.vote('2')
calc_balances()

c.ask('3', 2400)
calc_balances()
c.vote('3')
calc_balances()

a.ask('4', 10000)
calc_balances()
b.vote('4')
calc_balances()

a.send('Bob', 100)
calc_tx()
calc_balances()
b.send('Alice', 250)
calc_tx()
calc_balances()

print('Balances:', balances)

print('Transactions:', netto)

'''for i in range(5):
    calc_balances()
    print(f'{i} Balances: {balances}')'''

print('Asks:', asks)
print('Votes:', votes)
print('Tx:', tx)
print('Balances:',balances)
print('Emission:', emission())
