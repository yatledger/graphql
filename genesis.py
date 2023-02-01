import time
import random
import uuid
import base58
import hashlib
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from src.models import Ask, Vote
from pymongo import MongoClient

cli = MongoClient('localhost', 27017)

db = cli.yat
txs = db.tx
asks = db.asks
votes = db.votes

def tob2b(t):
    h = hashlib.blake2b()
    h.update(t)
    return base58.b58encode(h.digest())

sk = 'DQsYfHpJ9WAGai9JJ1eDntkx4CpeCAbhPi2MrPDiwYs5'
sk_bytes = base58.b58decode(sk.encode())
pk = 'B3qUs7s5C5G4n7V5x2XE4JMWzPMvVXWRzkxfp76zgs6t'

amount = 1000000000000
uniq = str(uuid.uuid4())
m = pk + str(amount) + str(uniq)
signing_key = SigningKey(sk_bytes)
message_bytes = bytes(m.encode("utf-8"))
signed = base58.b58encode(signing_key.sign(message_bytes))
hash_ask = tob2b(signed)

a = Ask(addr = pk,
    amount = amount,
    uniq = uniq,
    title = '',
    cover = '',
    desc = '',
    sign = signed,
    prev_hash = '',
    hash = hash_ask,
    time = int(round(time.time() * 1000)))

r = asks.insert_one(dict(a))
if r.inserted_id: print(r.inserted_id)

uniq = str(uuid.uuid4())
like = True
m = pk + str(hash_ask) + str(like) + str(uniq)
message_bytes = bytes(m.encode("utf-8"))
signed = base58.b58encode(signing_key.sign(message_bytes))
hash_vote = tob2b(signed)

v = Vote(addr = pk,
    id = hash_ask,
    like = like,
    uniq = uniq,
    sign = signed,
    prev_hash = '',
    hash = hash_vote,
    time = int(round(time.time() * 1000)))

r = votes.insert_one(dict(v))
if r.inserted_id: print(r.inserted_id)    

print(a)
print(v)