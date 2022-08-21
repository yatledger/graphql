import strawberry
import motor.motor_asyncio
import decimal

from fastapi import FastAPI
from strawberry.asgi import GraphQL
from typing import List, Optional

#from models import Tx, User, UserContent

cli = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

db = cli.yat
txs = db.tx
usrs = db.users

@strawberry.type
class Tx:
    credit: str
    debit: str
    amount: int
    time: decimal.Decimal
    sign: str
    hash: str
    msg: Optional[str]

async def load_tx(amount, time, start, end) -> List[Tx]:
    if amount >= 0:  amount_direction = '$gt'
    else:
        amount_direction = '$lt'
        amount = -amount
    
    if time >= 0: time_direction = '$gt'
    else:
        time_direction = '$lt'
        time = -amount

    q = {
        'amount': {amount_direction: amount},
        'time': {time_direction: time},
    }

    tx = await txs.find({'$query': q, '$orderby': {'_id': -1}}).skip(start).limit(end).to_list(None)

    return [
        Tx(
            credit = t['credit'],
            debit = t['debit'],
            amount = t['amount'],
            time = t['time'],
            sign = t['sign'],
            hash = t['hash'],
            msg = t['msg'] if 'msg' in t else '',
        )
        for t in tx
    ]

#loader = DataLoader(load_fn=load_tx)

@strawberry.type
class Query:
    @strawberry.field
    async def tx(self, amount: int = 0, time: int = 0, start: int = 0, end: int = 100) -> List[Tx]:
        return await load_tx(amount, time, start, end)


schema = strawberry.Schema(query=Query)


graphql_app = GraphQL(schema)#graphiql=False

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)