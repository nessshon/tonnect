import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext

from aiogram.types import Message
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from . import keyboards
from .filters import IsPrivate
from .tonnect import TonnectException, get_auth_token


async def command_start(message: Message, state: FSMContext):
    if message.get_args():  # checking if arguments were passed to the start command
        data = await state.get_data()  # getting the data from RedisStorage
        secret_key = message.get_args()  # getting secret key from command arguments

        # checking if the secret key is valid or not expired
        try:
            message_id = data["message_id"]  # getting the message ID for editing
            auth_token = await get_auth_token(secret_key)  # getting the AuthToken with the wallet address
            text = f"Done!\nYour wallet address is:\n{auth_token.address}"

            await message.bot.edit_message_text(
                text, chat_id=message.chat.id,
                message_id=message_id
            )  # editing the message with wallet address

        # if the secret key is not valid or expired
        except TonnectException as e:
            message_id = data["message_id"]  # getting the message ID for editing
            text = f"{e.__str__()}\nTry again."

            await message.bot.edit_message_text(
                text, chat_id=message.chat.id,
                message_id=message_id
            )  # editing the message with error message

        except Exception as e:
            logging.error(e)

    bot = await message.bot.get_me()  # Getting the bot to get its username
    text = f"Hi, 👋!\nConnect your wallet!"
    markup = keyboards.connect_markup(bot.username)

    msg = await message.answer(text, reply_markup=markup)
    await state.update_data(message_id=msg.message_id)  # save or update message for later editing
    await message.delete()  # deleting the message /start


async def command_source(message: Message):
    text = "https://github.com/nessshon/tonnect"
    await message.answer(text)


def register(dp: Dispatcher):
    dp.register_message_handler(
        command_start, IsPrivate(), commands="start"
    )
    dp.register_message_handler(
        command_source, IsPrivate(), commands="source"
    )
    # register the commands
    # IsPrivate() will only register for private messages


async def setup(bot: Bot):
    commands = [
        BotCommand("start", "Restart"),
        BotCommand("source", "Source code"),
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
    )
    # set bot commands
