from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def connect_markup(bot_username: str) -> InlineKeyboardMarkup:
    """Creates an inline keyboard markup with a ton-connect button

    :param bot_username: bot username without `@`
    :return: :class:`InlineKeyboardMarkup`
    """
    app_id = "41ce47914bffe24cc5979b4c1b36ec5a6960ccfd480d2a567f7aa38284a1560031373033"
    base_url = "http://tonapi.io/login?app={}&return_url={}"
    return_url = "https://tonnect.ru/api/login/bot={}"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Connect Tonkeeper",
                    url=base_url.format(app_id, return_url.format(bot_username))
                )
            ]
        ]
    )
