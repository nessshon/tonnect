from dataclasses import dataclass, asdict
from typing import Literal

import requests as requests

from .exceptions import TonapiError, TonapiUnauthorized, TonapiException


@dataclass
class Url:
    MAINNET = "https://tonapi.io"
    TESTNET = "https://testnet.tonapi.io"


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


class Tonapi:
    def __init__(self, api_key: str, testnet: bool = False):
        self._api_key = api_key
        self._testnet = testnet

        self.__headers = {'Authorization': 'Bearer ' + api_key}
        self.__base_url = Url.TESTNET if testnet else Url.MAINNET

    def _request(self, method: str, params: dict = None):
        params = params.copy() if params is not None else {}

        with requests.Session() as session:
            with session.get(f"{self.__base_url}{method}",
                             params=params,
                             headers=self.__headers
                             ) as response:
                response_json = response.json()
                print(response_json)

                match response.status_code:
                    case 200:
                        return response_json
                    case 400:
                        raise TonapiError(response_json)
                    case 401:
                        raise TonapiUnauthorized(response_json)
                    case _:
                        raise TonapiException(response_json)

    def get_token(self, auth_token: str, rate_limit: int = 1,
                  token_type: Literal["client", "server"]
                  = "server") -> AuthToken:
        """Checks the validity of the auth token.

        :param auth_token: The token which was returned by
         the method below.
        :param rate_limit: Request per seconds. Default value 1
        :param token_type: [client, server], type of token which
         will be used to indicate the app. default value server.
         Learn more about serverside and clientside flows:
         https://tonapi.io/docs#serverside-and-clientside-flows/
        :return: :class:`AuthToken` object
        """
        params = {
            'auth_token': auth_token,
            'rate_limit': rate_limit,
            'token_type': token_type,
        }
        response = self._request("/v1/oauth/getToken", params)

        return AuthToken(**response)
