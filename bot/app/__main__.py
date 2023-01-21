from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from aiogram.utils.exceptions import Unauthorized
from aiogram.contrib.fsm_storage.redis import RedisStorage2


async def on_startup(dp: Dispatcher):
    from . import filters
    filters.setup(dp)

    from . import middlewares
    middlewares.setup(dp)

    from . import commands
    commands.register(dp)
    await commands.setup(dp.bot)


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()

    session = await dp.bot.get_session()
    await session.close()


def init():
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    )

    from environs import Env
    env = Env()
    env.read_env()

    dp = Dispatcher(
        bot=Bot(
            token=env.str("BOT_TOKEN"),
            parse_mode="HTML"
        ),
        storage=RedisStorage2(
            host=env.str("REDIS_HOST"),
            port=env.int("REDIS_PORT"),
            db=env.int("REDIS_DB")
        )
    )

    try:
        executor.start_polling(
            dispatcher=dp,
            skip_updates=False,
            reset_webhook=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )

    except Unauthorized:
        logging.error("Invalid bot token!")

    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    init()
