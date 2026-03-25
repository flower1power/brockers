import time
from json import loads, JSONDecodeError
from typing import Any, Callable, NoReturn

from framework.internal.http.account.account import AccountApi
from framework.internal.http.mail.mail import MailApi


def retrier(function: Callable[..., str | NoReturn]) -> Callable[..., str | NoReturn]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        token = None
        count = 0
        sleep = 1

        while token is None:
            print(f"Попытка получения токена номер: {count}")
            token = function(*args, **kwargs)
            count += 1

            if token:
                return token

            if count == 10:
                raise AssertionError("Превышено количество попыток получения токена")
            sleep = sleep * (count / 3)
            time.sleep(sleep)

    return wrapper


class AccountHelper:
    def __init__(self, account_api: AccountApi, mail_api: MailApi):
        self.account_api = account_api
        self.mail_api = mail_api

    def register_user(self, login: str, email: str, password: str):
        return self.account_api.register_user(login=login, email=email, password=password)

    def success_register_user(self, login: str, email: str, password: str):
        self.register_user(login=login, email=email, password=password)
        self.find_msg(email)

    def failed_register_user(self, login: str, email: str, password: str):
        self.register_user(login=login, email=email, password=password)
        self.failed_find_msg(email)

    @retrier
    def get_activation_token_by_login(self, login: str) -> str:
        token = None
        response = self.mail_api.find_msg(query=login)

        for item in response.json()['items']:
            try:
                user_data = loads(item['Content']['Body'])
            except JSONDecodeError:
                continue
            user_login = user_data.get('Login')
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break

        return token

    def failed_find_msg(self, query: str, count: int = 10) -> None:
        for _ in range(count):
            response = self.mail_api.find_msg(query=query)
            if response.json()["total"] > 0:
                raise AssertionError("Email over found")
            time.sleep(1)

    def find_msg(self, query: str, count: int = 10) -> None:
        for _ in range(count):
            response = self.mail_api.find_msg(query)
            if response.json()["total"] > 0:
                break
            time.sleep(1)
        else:
            raise AssertionError("Email not found")
