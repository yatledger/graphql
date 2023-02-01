from typing import List
import math
from pymongo import MongoClient
import redis
from src.models import Ask, Vote, Tx, User
import logging

logfmt = '%(levelname)s | %(message)s'
logging.basicConfig(level=logging.DEBUG, format=logfmt)
logging.basicConfig(level=logging.INFO, format=logfmt) #handlers=loghdlrs
logging.basicConfig(level=logging.WARNING, format=logfmt)
logging.basicConfig(level=logging.ERROR, format=logfmt)
logging.getLogger().setLevel(logging.INFO)

cli = MongoClient('localhost', 27017)
r = redis.Redis(host='localhost', port=6379, db=0)

db = cli.yat
db_tx= db.tx
db_asks= db.asks
db_votes= db.votes
db_users= db.users

asks = db_asks.find({})
votes = db_votes.find({})
tx = db_tx.find({})
users = db_users.find({})

balances = {}
netto = {}

def emission() -> int:
    return int(sum(balances.values()) or 1)

def addr_balance(addr: str) -> int:
    return int(balances.get(addr) or 1)

def addr_asks(addr: str) -> List:
    a = []
    asks = db_asks.find({})
    for ask in asks:
        ask = Ask(**ask)
        if ask.addr == addr:
            a.append(ask.hash)
    return a

def addr_karma(addr: str) -> int:
    return addr_balance(addr) / emission()

def ask_votes(id: str) -> List:
    v = []
    votes = db_votes.find({})
    for vote in votes:
        vote = Vote(**vote)
        if vote.id == id:
            v.append(vote.addr)
    return v

def ask_balance(id: str) -> int:
    balance = 0
    ask = db_asks.find_one({"hash": id})
    ask = Ask(**ask)
    for vote in ask_votes(id):
        k = addr_karma(vote)
        balance += ask.amount * k
    return math.floor(balance)

def addr_current_balance(addr: str):
    asks_current = addr_asks(addr)
    print(asks_current)
    b = 1
    for ask in asks_current:
        b += ask_balance(ask)
    return b + int(netto.get(addr) or 0)

def calc_balances():
    for _ in range(5):
        for u in users:
            u = User(**u)
            print(u)
            b = addr_current_balance(u.addr)
            balances.update({u.addr: b})

def calc_tx():
    for t in tx:
        t = Tx(**t)
        c = netto.get(t.credit)
        d = netto.get(t.debit)
        netto.update({t.credit: int(c or 0) - t.amount})
        netto.update({t.debit: int(d or 0) + t.amount})

for i in range(5):
    calc_balances()
    print(f'{i} Balances: {balances}')

for b in balances:
    r.set(b, balances[b])