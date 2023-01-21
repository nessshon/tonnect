from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def connect_markup(bot_username: str) -> InlineKeyboardMarkup:
    """Creates an inline keyboard markup with a ton-connect button

    :param bot_username: bot username without `@`
    :return: :class:`InlineKeyboardMarkup`
    """
    base_url = "http://tonapi.io/login?return_url={}"
    return_url = "https://tonnect.ru/api/login/bot={}"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Connect Tonkeeper",
                    url=base_url.format(return_url.format(bot_username))
                )
            ]
        ]
    )
