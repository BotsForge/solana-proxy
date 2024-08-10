import unittest
import asyncio

import python_socks
from proxystr import check_proxies

from solana_proxy import Client, AsyncClient


REAL_HTTP_PROXY = 'your_real_http_proxy_in_any_format'
REAL_SOCKS5_PROXY = 'socks5://your_real_socks5_proxy_in_any_format'


RPC_URL = 'https://api.mainnet-beta.solana.com'


class TestCheck(unittest.TestCase):
    def setUp(self):
        check_proxies([REAL_HTTP_PROXY, REAL_SOCKS5_PROXY], raise_on_error=True)
        self.fp = 'bAgsdfi:fZsdf@212.193.122.88:61176'
        self.fsp = 'socks5://bAgsdfi:fZsdf@212.193.122.88:61176'
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def test_sync(self):
        with Client(RPC_URL) as client:
            self.assertTrue(client.is_connected())

        with Client(RPC_URL, proxy=self.fp) as client:
            self.assertFalse(client.is_connected())

        with Client(RPC_URL, proxy=self.fsp) as client:
            self.assertFalse(client.is_connected())

        with Client(RPC_URL, proxy=REAL_HTTP_PROXY) as client:
            self.assertTrue(client.is_connected())

        with Client(RPC_URL, proxy=REAL_SOCKS5_PROXY) as client:
            self.assertTrue(client.is_connected())

    def test_async(self):
        self.loop.run_until_complete(self.async_test())

    async def async_test(self):
        async with AsyncClient(RPC_URL) as client:
            self.assertTrue(await client.is_connected())

        async with AsyncClient(RPC_URL, proxy=self.fp) as client:
            self.assertFalse(await client.is_connected())

        with self.assertRaises(python_socks._errors.ProxyTimeoutError):
            async with AsyncClient(RPC_URL, proxy=self.fsp) as client:
                await client.is_connected()

        async with AsyncClient(RPC_URL, proxy=REAL_HTTP_PROXY) as client:
            self.assertTrue(await client.is_connected())

        async with AsyncClient(RPC_URL, proxy=REAL_SOCKS5_PROXY) as client:
            self.assertTrue(await client.is_connected())


if __name__ == '__main__':
    unittest.main()
