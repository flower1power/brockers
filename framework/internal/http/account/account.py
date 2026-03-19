import httpx

from framework.internal.http.account.endpoints import Endpoints


class AccountApi:
    _endpoints: Endpoints = Endpoints()

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._client = httpx.Client(base_url=self._base_url)

    def register_user(self, login: str, email: str, password: str) -> httpx.Response:
        data = {"login": login, "email": email, "password": password}
        return self._client.post(Endpoints.async_register, json=data)

    def activate_user(self, token: str) -> httpx.Response:
        return self._client.put(Endpoints.activate(token))
