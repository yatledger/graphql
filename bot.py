import time
import random
import uuid
import base58
import hashlib
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from src.models import Ask, Vote
from pymongo import MongoClient

priv = ['DQsYfHpJ9WAGai9JJ1eDntkx4CpeCAbhPi2MrPDiwYs5', '3yuDvVMcZoSLxKbs8BHXrih94fp8cQrpZZcBigVFiksj', '4NHtsBpZaSNb8X3XNSRKuAY34ypmEHPSt74ALiJnchth']
pub = ['B3qUs7s5C5G4n7V5x2XE4JMWzPMvVXWRzkxfp76zgs6t', '7sBaswB6xNXG2FuXoRFuQeoeYP6SnygCwhECPKBPXjLe', '5GfBkvUygoJQ4xmy81z7HypcSF8BT38r99QS86mub4t4']

cli = MongoClient('localhost', 27017)

db = cli.yat
txs = db.tx
db_asks = db.asks
db_votes = db.votes

def tob2b(t):
    h = hashlib.blake2b()
    h.update(t)
    return base58.b58encode(h.digest())

def sign(sk, m):
    sk_bytes = base58.b58decode(sk.encode())
    signing_key = SigningKey(sk_bytes)
    message_bytes = bytes(m.encode("utf-8"))
    signed = base58.b58encode(signing_key.sign(message_bytes))
    hash = tob2b(signed)
    return signed, hash

for _ in range(10):

    i = random.randint(0, 2)
    sk = priv[i]
    pk = pub[i]
    
    uniq = str(uuid.uuid4())
    #t = random.randint(0, 2)
    t = 1

    if t == 0:
        amount = random.randint(0, 1000000)
        m = pk + str(amount) + str(uniq)
        signed, hash = sign(sk, m)
        a = Ask(addr = pk,
            amount = amount,
            uniq = uniq,
            title = '',
            cover = '',
            desc = '',
            sign = signed,
            prev_hash = '',
            hash = hash,
            time = int(round(time.time() * 1000)))
        r = db_asks.insert_one(dict(a))
        if r.inserted_id: print(f'{pk} ASK {hash.decode("utf-8")}')

    if t == 1:
        like = True
        m = pk + str(hash) + str(like) + str(uniq)
        signed, hash = sign(sk, m)

        asks = list(db_asks.find({}))
        i = random.randint(0, len(asks) - 1)
        id = asks[i]['hash']

        votes = db_votes.find({'id': id})
        voted = False
        for v in votes:
            if v['addr'] == pk:
                voted = True
        
        if not voted:
            v = Vote(addr = pk,
                id = id,
                like = like,
                uniq = uniq,
                sign = signed,
                prev_hash = '',
                hash = hash,
                time = int(round(time.time() * 1000)))
            r = db_votes.insert_one(dict(v))
            if r.inserted_id: print(f'{pk} VOTE {id}') 