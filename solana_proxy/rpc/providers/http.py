from typing import Optional, Dict, Union, Tuple

import httpx
from solana.rpc.providers.http import HTTPProvider as OriginHTTPProvider
from solana.rpc.providers.core import DEFAULT_TIMEOUT, _after_request_unparsed
from solders.rpc.requests import Body
from proxystr import Proxy

from .session import Session


class HTTPProvider(OriginHTTPProvider):
    def __init__(
        self,
        endpoint: Optional[str] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        timeout: float = DEFAULT_TIMEOUT,
        *,
        proxy: Union[Proxy, str] = None,
        **kwargs
    ):
        super().__init__(
            endpoint=endpoint,
            extra_headers=extra_headers,
            **kwargs
        )
        self.session = Session(proxy, timeout=timeout)
        self._proxy = proxy

    def __str__(self) -> str:
        """String definition for HTTPProvider."""
        return f"HTTP RPC connection {self.endpoint_uri} | proxy={self._proxy}"

    def make_request_unparsed(self, body: Body) -> str:
        """Make an async HTTP request to an http rpc endpoint."""
        request_kwargs = self._before_request(body=body)
        raw_response = self.session.post(**request_kwargs)
        return _after_request_unparsed(raw_response)

    def make_batch_request_unparsed(self, reqs: Tuple[Body, ...]) -> str:
        """Make an async HTTP request to an http rpc endpoint."""
        request_kwargs = self._before_batch_request(reqs)
        raw_response = self.session.post(**request_kwargs)
        return _after_request_unparsed(raw_response)

    def is_connected(self) -> bool:
        """Health check."""
        try:
            response = self.session.get(self.health_uri)
            response.raise_for_status()
        except (IOError, httpx.HTTPError) as err:
            self.logger.error("Health check failed with error: %s", str(err))
            return False

        return response.status_code == httpx.codes.OK

    def __enter__(self):
        self.session.__enter__()
        return self

    def __exit__(self, *args):
        self.session.__exit__(*args)

    def close(self):
        self.session.close()
