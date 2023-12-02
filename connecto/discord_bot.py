import sys
import discord
import logging
import os
from connections_parser import parse_messages

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("connecto")
bot = discord.Bot(intents=discord.Intents.default())


@bot.event
async def on_ready():
    logger.info(
        f"Logged in as {bot.user} (ID: {bot.user.id}). Ready to serve commands."
    )


@bot.slash_command(name="stats", description="Get your Connections stats!")
@discord.option(
    name="visibility",
    description="Post stats here or get a DM",
    choices=["public", "private"],
)
async def stats(ctx, visibility):
    """Returns the user's connections stats.

    Fetches all messages sent by the user in this channel and uses Connections result strings to compute and return the
    user's Connections stats.
    """
    logger.info(f"{ctx.author} issued stats command with {visibility} visibility")
    messages = await get_message_history_raw(ctx.channel, ctx.author)
    user_stats = parse_messages(messages)
    result = user_stats.display()
    logger.info(f"responding to {ctx.author} with {result}")
    if visibility == "public":
        await ctx.respond(user_stats.display())
    elif visibility == "private":
        await ctx.user.send(user_stats.display())
        await ctx.respond("Sent!")


async def get_message_history_raw(channel, author):
    """Returns all messages sent by the author in this channel."""
    results = []
    async for m in channel.history(limit=None):
        if author == m.author:
            results.append(m.content)
    return results


bot.run(os.environ["TOKEN"])
