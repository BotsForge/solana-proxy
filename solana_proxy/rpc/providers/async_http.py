from typing import Optional, Dict, Union

from solana.rpc.providers.async_http import AsyncHTTPProvider as OriginAsyncHTTPProvider
from solana.rpc.providers.core import DEFAULT_TIMEOUT, _HTTPProviderCore
from proxystr import Proxy

from .session import AsyncSession


class AsyncHTTPProvider(OriginAsyncHTTPProvider):
    def __init__(
        self,
        endpoint: Optional[str] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        timeout: float = DEFAULT_TIMEOUT,
        *,
        proxy: Union[Proxy, str] = None,
        **kwargs
    ):
        _HTTPProviderCore.__init__(
            self,
            endpoint=endpoint,
            extra_headers=extra_headers,
            **kwargs
        )
        self.session = AsyncSession(proxy, timeout=timeout)
        self._proxy = proxy

    def __str__(self) -> str:
        """String definition for HTTPProvider."""
        return f"Async HTTP RPC connection {self.endpoint_uri} | proxy={self._proxy}"

    async def __aexit__(self, *args):
        await self.session.__aexit__(*args)

    async def close(self):
        await self.session.aclose()
