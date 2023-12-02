from bot import discord_bot
import logging
import os

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    bot = discord_bot.bot
    bot.run(os.environ["TOKEN"])
