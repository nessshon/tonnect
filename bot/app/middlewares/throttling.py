from contextlib import suppress

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.utils.exceptions import Throttled, MessageCantBeDeleted, MessageToDeleteNotFound


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self,
                 key: str = 'default',
                 message_limit: float = 1
                 ):
        self.default_key = key
        self.message_limit = message_limit
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        if handler:
            throttling_key = getattr(handler, "throttling_key", None)
            key = throttling_key if throttling_key else self.default_key
            limit = getattr(handler, "throttling_rate_limit", self.message_limit)
        else:
            limit = self.message_limit
            key = self.default_key

        try:
            await dispatcher.throttle(key, rate=limit)

        except Throttled:
            with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
                await message.bot.delete_message(
                    message.chat.id, message.message_id
                )
            raise CancelHandler()


def rate_limit(limit: float, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)

        return func

    return decorator
