import asyncio
from create_bot import create_bot
import logging

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        " - (Line: %(lineno)d [%(filename)s - %(funcName)s])",
    )
    try:
        asyncio.run(create_bot())
    except KeyboardInterrupt:
        logging.info("Bot stopped")
