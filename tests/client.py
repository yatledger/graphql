from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from random import randint

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="http://127.0.0.1:9696/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query getTx ($amount: Int, $skip: Int, $limit: Int) {
      tx (
        amount: $amount,
        skip: $skip,
        limit: $limit
      ) {
      amount
      credit
      debit
      msg
      time
      hash
    }
    }
"""
)
for _ in range(0, 10):
    amount = randint(-1000, 1000)
    skip = randint(0, 1000)
    limit = randint(1, 1000)
    params = {
        "amount": amount,
        "skip": skip,
        "limit": limit,
    }
    print(params)
    # Execute the query on the transport
    result = client.execute(query, variable_values=params)
    #print(result)
    l = len(result["tx"])
    if l == limit: print(f"Limit: {l} =  {limit}")
    else: print(f"Limit: {l} !=  {limit}")