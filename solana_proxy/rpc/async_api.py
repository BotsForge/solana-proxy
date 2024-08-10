from typing import Optional, Dict, Union

from solana.rpc.async_api import AsyncClient as OriginAsyncClient
from solana.rpc.commitment import Commitment
from proxystr import Proxy

from .providers import AsyncHTTPProvider, DEFAULT_TIMEOUT


class AsyncClient(OriginAsyncClient):  # pylint: disable=too-many-public-methods
    """Async client class.

    Args:
        endpoint: URL of the RPC endpoint.
        commitment: Default bank state to query. It can be either "finalized", "confirmed" or "processed".
        timeout: HTTP request timeout in seconds.
        extra_headers: Extra headers to pass for HTTP request.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        commitment: Optional[Commitment] = None,
        timeout: float = DEFAULT_TIMEOUT,
        extra_headers: Optional[Dict[str, str]] = None,
        *,
        proxy: Union[Proxy, str] = None,
        **kwargs
    ):
        """Init API client."""
        super().__init__(commitment)
        self._provider = AsyncHTTPProvider(
            endpoint=endpoint,
            timeout=timeout,
            extra_headers=extra_headers,
            proxy=proxy,
            **kwargs
        )

    async def __aexit__(self, *args):
        await self._provider.__aexit__(*args)
