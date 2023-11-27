import os
from discord import Intents
from discord.ext import commands
from connections_discord_bot import connections_parser

TOKEN = os.environ['TOKEN']
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.command()
async def stats(ctx, mode):
    if mode == 'public':
        results = []
        async for m in ctx.channel.history(limit=100):
            if ctx.author == m.author:
                res = connections_parser.parse_connections_result(m.content)
                if res is not None:
                    results.append(res)
        stats = connections_parser.analyze_connections_history(results)
        await ctx.send(stats.display())


bot.run(TOKEN)
