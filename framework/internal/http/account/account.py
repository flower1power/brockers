from types import TracebackType

import httpx

from framework.internal.http.account.endpoints import Endpoints


class AccountApi:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._client = httpx.Client(base_url=self._base_url)

    def __enter__(self) -> "AccountApi":
        return self

    def __exit__(
            self,
            exc_type: type[BaseException],
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> None:
        self.close()

    def register_user(self, login: str, email: str, password: str) -> httpx.Response:
        data = {"login": login, "email": email, "password": password}
        return self._client.post(Endpoints.async_register, json=data)

    def activate_user(self, token: str) -> httpx.Response:
        return self._client.put(Endpoints.activate(token))

    def close(self) -> None:
        self._client.close()
