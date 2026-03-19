import httpx

from framework.internal.http.mail.endpoints import Endpoints


class MailApi:
    _endpoints: Endpoints = Endpoints()

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._client = httpx.Client(base_url=self._base_url)

    def find_msg(self, query: str) -> httpx.Response:
        params = {"query": query, "limit": 1, "kind": "containing", "start": 0}
        return self._client.get(Endpoints.search, params=params)
