from discord.ext import commands
from discord import Object
from asyncio import sleep

from Discord.Backend.engine import Functions


class CogEvents(commands.Cog):
    def __init__(self, client, backend):
        self.client = client
        self.backend = backend

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments:
            if str(message.attachments[0]).endswith(('ogg', 'mp3', 'wav')):
                text = await self.backend.speech_recognition(str(message.attachments[0]))
                await message.reply(text)

    @commands.Cog.listener()
    async def on_ready(self):
        [[self.backend.push_data(f'Discord/{guild.id}/messages', {member.id: 0}) for member in guild.members] for guild in self.client.guilds if self.backend.get_data(f'Discord/{guild.id}/messages') is None]
        [await member.add_roles(Object(id=1054454788126945350)) for member in self.client.get_all_members() if len(member.roles) < 2]
        print('[Log]: CogEvents class is ready')


async def setup(client):
    await client.add_cog(CogEvents(client, Functions('events')))
