from __future__ import annotations

from dataclasses import asdict, dataclass

import aiohttp


async def get_auth_token(secret_key: str) -> AuthToken:
    """Get auth token by secret key.

    :param secret_key: string
    :return: :class:`AuthToken` object.
    """
    url = "https://tonnect.ru/api/getAuthToken"
    params = {"secret_key": secret_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response_json = await response.json()

            match response.status:
                case 200:
                    return AuthToken(**response_json)
                case _:
                    error = response_json.get("error")
                    raise TonnectException(error)


@dataclass
class AuthToken:
    """
    Attributes:
        address (str): example - EQCt...s7Ui
        user_token (str): example - abcd...
    """
    address: str
    user_token: str

    def to_dict(self) -> dict:
        return asdict(self)


class TonnectException(Exception):
    ...
