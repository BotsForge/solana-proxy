# **solana-proxy**
[![Telegram channel](https://img.shields.io/endpoint?url=https://runkit.io/damiankrawczyk/telegram-badge/branches/master?url=https://t.me/bots_forge)](https://t.me/bots_forge)

**A library for using *HTTP* and *SOCKS5* proxies with [`solana`](https://pypi.org/project/solana/) clients**
The library provides `Client` and `AsyncClient` classes, which override the initialization of the original classes. Apart from these two classes, the library does not offer any additional features, and in all other cases, the original `solana` library, included as part of the installation package, should be used.

```bash
pip install solana-proxy
```
**Depencies**: `solana, httpx, httpx-socks, proxystr`

## Simple usage
```python
from solana_proxy import Client

RPC_URL = 'https://api.mainnet-beta.solana.com'
client = Client(RPC_URL, proxy='login:password@ip:port')  # or 'socks5://login:password@ip:port'
client.is_connected()
...
client.close()
```
`Client` and `AsyncClient` take proxy in any popular format because they use [`proxystr`](https://pypi.org/project/proxystr/) lib. Also they take a `Proxy` obj from that lib.
## Context manager
```python
import asyncio
from solana_proxy import Client, AsyncClient

RPC_URL = 'https://api.mainnet-beta.solana.com'
PROXY = 'login:password@ip:port'  # or 'socks5://login:password@ip:port'

with Client(RPC_URL, proxy=PROXY) as client:
    client.is_connected()

async def is_connected():
    async with AsyncClient(RPC_URL, proxy=PROXY) as client:
        return await client.is_connected()
```

## Support
Developed by `MrSmith06`: [telegram](https://t.me/Mr_Smith06) |  [gtihub](https://github.com/MrSmith06)
If you find this project helpful, feel free to leave a tip!
- EVM address (metamask): `0x6201d7364F01772F8FbDce67A9900d505950aB99`