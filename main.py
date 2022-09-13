import strawberry
import motor.motor_asyncio
import decimal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL
from typing import List, Optional

from aio_pika import connect_robust, Message, DeliveryMode

from models import Tx, User, UserContent

cli = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

db = cli.yat
txs = db.txdev
usrs = db.users

@strawberry.experimental.pydantic.type(model=Tx)
class GetTx:
    credit: Optional[str]
    debit: Optional[str]
    amount: Optional[float]
    time: Optional[decimal.Decimal]
    sign: Optional[str]
    hash: strawberry.auto
    msg: strawberry.auto

async def load_tx(amount, addr, msg, time, skip, limit) -> List[GetTx]:
    if amount >= 0: amount_direction = '$gt'
    else: amount_direction = '$lt'; amount = -amount
    
    if time >= 0: time_direction = '$gt'
    else: time_direction = '$lt'; time = -amount

    q = {
        'amount': {amount_direction: amount},
        'time': {time_direction: time},
    }

    if msg != None:
        if msg == True: q['msg'] = {'$ne': 'null'}
        else: q['msg'] = 'null'

    if addr:
        q['$or'] = [{'credit': addr}, {'debit': addr}]
    
    print(q)

    return [
        GetTx.from_pydantic(Tx(**t)) for t in await txs.find({
            '$query': q,
            '$orderby': {'_id': -1}
            })
            .skip(skip)
            .limit(limit)
            .to_list(None)
    ]

@strawberry.type
class Query:
    @strawberry.field
    async def tx(
        self,
        msg: bool = None,
        addr: str = '',
        amount: int = 0,
        time: int = 0,
        skip: int = 0,
        limit: int = 100
    ) -> List[GetTx]:
        return await load_tx(amount, addr, msg, time, skip, limit)


schema = strawberry.Schema(query=Query)


graphql_app = GraphQL(schema)#graphiql=False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    global mq
    connection = await connect_robust("amqp://guest:guest@localhost/")
    mq = await connection.channel()
    queue = await mq.declare_queue("tx", durable=True)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)