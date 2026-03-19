class Endpoints:
    async_register = "/register/user/async-register"

    @staticmethod
    def activate(token: str) -> str:
        return f"/register/user/activate?token={token}"
