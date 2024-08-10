from typing import Optional, Dict, Union

from solana.rpc.api import Client as OriginClient
from solana.rpc.commitment import Commitment
from proxystr import Proxy

from .providers import HTTPProvider, DEFAULT_TIMEOUT


class Client(OriginClient):  # pylint: disable=too-many-public-methods
    """Client class.

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
        self._provider = HTTPProvider(
            endpoint=endpoint,
            timeout=timeout,
            extra_headers=extra_headers,
            proxy=proxy,
            **kwargs)

    def __enter__(self):
        self._provider.__enter__()
        return self

    def __exit__(self, *args):
        self._provider.__exit__(*args)

    def close(self):
        self._provider.close()
