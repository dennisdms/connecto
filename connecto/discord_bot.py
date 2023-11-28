import os
from discord import Intents
from discord.ext import commands
from connecto import connections_parser

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.command()
async def stats(ctx, mode):
    print(f'{ctx.author} issued stats command in {mode} mode')
    if mode == 'public':
        results = []
        async for m in ctx.channel.history(limit=100):
            if ctx.author == m.author:
                res = connections_parser.parse_connections_result(m.content)
                if res is not None:
                    results.append(res)
        stats = connections_parser.analyze_connections_history(results)
        await ctx.send(stats.display())
    else:
        print(f'{ctx.author} issued stats command in unknown {mode} mode')


if __name__ == '__main__':
    TOKEN = os.environ['TOKEN']
    bot.run(TOKEN)