from typing import List, Optional
from pydantic import BaseModel
import math
import time
import sys
from functools import wraps
import logging


#sys.path.append('../src')
#from src.balance import qwe

logfmt = '%(levelname)s | %(message)s'
logging.basicConfig(level=logging.DEBUG, format=logfmt)
logging.basicConfig(level=logging.INFO, format=logfmt) #handlers=loghdlrs
logging.basicConfig(level=logging.WARNING, format=logfmt)
logging.basicConfig(level=logging.ERROR, format=logfmt)
logging.getLogger().setLevel(logging.WARNING)

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
    logging.debug(f'Balance ({addr_balance(addr)}) / Emission ({emission()})')
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
            logging.debug(f'{ask.addr} ask {ask.id} for {ask.amount}')
            balance = 0
            for vote in ask_votes(id):
                logging.debug('------')
                logging.debug(f'Vote from: {vote}')
                k = addr_karma(vote)
                logging.debug(f'Karma: {k}')
                balance += ask.amount * k
                logging.debug('------')
            logging.debug(f'{ask.id} ask balance: {math.floor(balance)}')
            return math.floor(balance)

def addr_current_balance(addr: str):
    asks = addr_asks(addr)
    b = 1
    for ask in asks:
        b += ask_balance(ask)
    return b + int(netto.get(addr) or 0)

def calc_balances():
    #logging.info(f'Pre balances: {balances}')
    for i in range(5):
        for u in users:
            b = addr_current_balance(u)
            balances.update({u: b})
        logging.info(f'{i} balances: {balances}')
    logging.warning(f'Balances: {balances}')

def calc_tx():
    for t in tx:
        c = netto.get(t.credit)
        d = netto.get(t.debit)
        netto.update({t.credit: int(c or 0) - t.amount})
        netto.update({t.debit: int(d or 0) + t.amount})

def print_on_call(func):
    @wraps(func)
    def wrapper(*args, **kw):
        #print('{} called'.format(func.__name__))
        try: res = func(*args, **kw)
        finally: calc_balances()
        return res
    return wrapper

def decorate_all_functions(function_decorator):
    def decorator(cls):
        for name, obj in vars(cls).items():
            if callable(obj): setattr(cls, name, function_decorator(obj))
        return cls
    return decorator

@decorate_all_functions(print_on_call)
class Person:
    def __init__(self, addr: str):
        users.append(addr)
        logging.warning(f'Person: {addr}')
        self.addr = addr
        
    def ask(self, id: str, amount: int):
        logging.warning(f"{time.time_ns()} Ask(addr={self.addr}, id={id}, amount={amount})")
        asks.append(Ask(addr=self.addr, id=id, amount=amount))

    def vote(self, id: str):
        logging.warning(f"{time.time_ns()} Vote(addr={self.addr}, id={id})")
        votes.append(Vote(addr=self.addr, id=id))

    def send(self, addr, amount):
        logging.warning(f"{time.time_ns()} Tx(debit={addr}, credit = {self.addr}, amount={amount})")
        tx.append(Tx(debit=addr, credit = self.addr, amount=amount))

a = Person(addr = 'Foundation')

a.ask('1', 21000)
a.vote('1')

c = Person(addr = 'Alice')
c.vote('1')

b = Person(addr = 'Bob')
b.ask('2', 1200)
a.vote('2')

c.ask('3', 2400)
c.vote('3')

a.ask('4', 10000)
b.vote('4')

a.send('Bob', 100)
calc_tx()
b.send('Alice', 250)
calc_tx()
a.send('Alice', 1000)
calc_tx()

print('Balances:', balances)

print('Transactions:', netto)

for i in range(5):
    calc_balances()
    print(f'{i} Balances: {balances}')

print('Asks:', asks)
print('Votes:', votes)
print('Tx:', tx)
print('Emission:', emission())
