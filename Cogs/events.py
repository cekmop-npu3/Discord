from discord.ext import commands
from discord import Object

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
        [await member.add_roles(Object(id=1054454788126945350)) for member in self.client.get_all_members() if len(member.roles) < 2]


async def setup(client):
    await client.add_cog(CogEvents(client, Functions('events')))
