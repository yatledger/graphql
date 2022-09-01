from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from random import randint
import time
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
from binascii import unhexlify

transport = AIOHTTPTransport(url="http://127.0.0.1:9696/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

sk = ['d4c6f7eab5e4ba71e55493174026bcdab93a98c96532b43a3d3a84e675108149', '87f387b8cdd98cd0b9fb63aa596f499be29c9564030b3e63a642dc29c9823760', '7cfaa722a12106912f982f658bebc54f196fac0b916e9e350a72b9206059351e', '09e00c4169074073c508c1122b00d61c8de27d5f4479701f7c80e4c4410ce5ab', '8b8ac1689b1aca2ef2d801aaa937bf89b69a6df7df463a6c6a87aaa9c8872314', '4ae79706598f255ae396489146cf15a33b939da00c5bd5cbcb2a6b354567afbe', 'ef5ab39dcb951e260606796c625e51e2b4e438df0c47253adbdd0306b1c2a7df', '28dec8163063be4d569a08830589e74afdca98a2bcb8e0b2ab8f2cbabd017c9e', 'fd187c9bd42b025b45ceb8b01855970ccbc4b902b2af4df4a5f76415fe350f13', 'c81a9365a5d6064b8f5f904b2c16fac24c02931ef740b201f4f85b5d857d5612']
pk = ['49700da9fa6bb1ba5177e072b54e83372b5af36a8812cb85948abacbc2e1bcb4', '2bd0943abf893f1b320dc46c75ec545e4d9d719888a350bf3e2bb4cd43dede32', '681052086f5d22073f86387eac8494760d087341119247fbec4acbd59a46d349', '0a2941cae93dd467332c800c388750d195fe6a50bf4fb7401804f9408b4a8fe8', 'a17f9d1aa44aca25ed45b35c15e3486b0a41914097310d68c93827dd912a2603', 'f41b9f07033f218c318ff506c2259d1755d201af3fe05ddbd19a54e5c7b1d13e', '433f3c687c4a34e2358dcdb6cb29d99f2426292f8492130dc52eb401cbb9f971', 'ddcb9218cbe329fbb388f5ede2c0c68ccb614ada8bd8e63d43a86843a87e21d4', 'fe19b04f617605cec8586fbcbbebff0bceb63e980197d5b81b7b3d31d8e86212', 'c211f43627d74f3f4158d9329c02535dd803f88d2041230f2660181efbe7d8f7']

query = gql(
"""
    query sendTx (
        $debit: Str,
        $credit: Str,
        $amount: Int,
        $sign: Str,
        $uniq: Str,
        $msg: Str,
        $type: Int,
        
    ) {
      send (
        debit: $debit,
        credit: $credit,
        amount: $amount,
        sign: $dsign,
        uniq: $uniq,
        msg: $msg,
        type: $type
      ) {
            status
        }
    }
"""
)
for _ in range(0, 10):
    i = randint(0, 9)
    c = pk[i]
    priv = sk[i]
    d = pk[randint(0, 9)]
    a = randint(100, 110)
    u = int(round(time.time() * 1000))
    m = str(randint(0, 100000))
    h = c + d + str(a) + str(m) + str(t)

    priv = unhexlify(priv)
    signing_key = SigningKey(priv)
    message_bytes = bytes(h.encode("utf-8"))
    signed_hex = signing_key.sign(message_bytes, encoder=HexEncoder)
    s = signed_hex.decode("utf-8")
    params = {
        "debit": d,
        "credit": c,
        "amount": a,
        "sign": s,
        "uniq": u,
        "msg": m,
        #"type": t
    }
    print(params)
    result = client.execute(query, variable_values=params)