from discord.ext import commands
from discord import Intents, Member, Object
from os import listdir

from config import bot_token


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=Intents.all())

    async def on_ready(self):
        print('--------Bot is ready--------')

    async def on_member_join(self, member: Member):
        await member.add_roles(Object(id=1054454788126945350))

    async def setup_hook(self) -> None:
        for filename in listdir('Cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'Cogs.{filename[:-3]}')
        await self.tree.sync()


if __name__ == '__main__':
    client = Client()
    client.run(bot_token)
