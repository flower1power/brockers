from types import TracebackType

import httpx

from framework.internal.http.mail.endpoints import Endpoints


class MailApi:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._client = httpx.Client(base_url=self._base_url)

    def __enter__(self) -> "MailApi":
        return self

    def __exit__(
            self,
            exc_type: type[BaseException],
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> None:
        self.close()

    def find_msg(self, query: str) -> httpx.Response:
        params = {"query": query, "limit": 1, "kind": "containing", "start": 0}
        return self._client.get(Endpoints.search, params=params)

    def close(self) -> None:
        self._client.close()
