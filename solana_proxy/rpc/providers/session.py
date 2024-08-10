from typing import Union

import httpx
from httpx_socks import AsyncProxyTransport, SyncProxyTransport
from proxystr import Proxy


class Session(httpx.Client):
    def __init__(self, proxy: Union[Proxy, str] = None, follow_redirects=True, **kwargs):
        if proxy:
            proxy = Proxy(proxy)
            if 'http' in proxy.protocol:
                kwargs['proxy'] = proxy.url
            elif 'socks' in proxy.protocol:
                kwargs['transport'] = SyncProxyTransport.from_url(proxy.url)
        super().__init__(follow_redirects=follow_redirects, **kwargs)


class AsyncSession(httpx.AsyncClient):
    def __init__(self, proxy: Union[Proxy, str] = None, follow_redirects=True, **kwargs):
        if proxy:
            proxy = Proxy(proxy)
            if 'http' in proxy.protocol:
                kwargs['proxy'] = proxy.url
            elif 'socks' in proxy.protocol:
                kwargs['transport'] = AsyncProxyTransport.from_url(proxy.url)
        super().__init__(follow_redirects=follow_redirects, **kwargs)
