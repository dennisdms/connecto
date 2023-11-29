from connecto.bot import connections_parser
import discord
import logging

logger = logging.getLogger(__name__)
bot = discord.Bot(intents=discord.Intents.default())


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.slash_command(name="stats", description="Get your Connections stats!")
@discord.option(
    name="visibility",
    description="Post stats here or get a DM",
    choices=["public", "private"],
)
async def stats(ctx, visibility):
    logger.info(f"{ctx.author} issued stats command with {visibility} visibility")
    user_history = await get_message_history(ctx.channel, ctx.author)
    user_stats = connections_parser.analyze_connections_history(user_history)
    await get_message_history_raw(ctx.channel, ctx.author)
    if visibility == "public":
        await ctx.respond(user_stats.display())
    elif visibility == "private":
        await ctx.user.send(user_stats.display())
        await ctx.respond("Sent!")


async def get_message_history(channel, author):
    results = []
    async for m in channel.history():
        if author == m.author:
            res = connections_parser.parse_connections_result(m.content)
            if res is not None:
                results.append(res)
    return results


async def get_message_history_raw(channel, author):
    results = []
    async for m in channel.history(limit=None):
        if author == m.author:
            results.append(m.content)
    return results
