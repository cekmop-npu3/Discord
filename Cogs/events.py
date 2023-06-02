from discord.ext import commands
from discord import Message, Member
from asyncio import sleep
from aiohttp import ClientSession

from Discord.Backend.engine import Functions
from Discord.Setup.config import vk_urls, spare_payload


class CogEvents(commands.Cog):
    def __init__(self, client, backend):
        self.client = client
        self.backend = backend

    async def _spare(self, message):
        if (lst := self.backend.get_data(f'Discord/{message.guild.id}/last_messages/{message.channel.id}')) is not None:
            if len(lst) != 50:
                self.backend.push_data(f'Discord/{message.guild.id}/last_messages', {message.channel.id: [[message.id, message.author.id], *lst]})
            else:
                self.backend.push_data(f'Discord/{message.guild.id}/last_messages', {message.channel.id: [[message.id, message.author.id], *lst[:-1:]]})
        else:
            self.backend.push_data(f'Discord/{message.guild.id}/last_messages', {message.channel.id: [[message.id, message.author.id]]})

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        self.backend.push_data(f'Discord/{member.guild.id}/messages', {member.id: 0})

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        print(message)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.attachments:
            if str(message.attachments[0]).endswith(('ogg', 'mp3', 'wav')):
                text = await self.backend.speech_recognition(str(message.attachments[0]))
                await message.reply(text)
        await self._push(f'Discord/{message.guild.id}/messages', message.author.id)
        if message.interaction:
            if message.interaction.name == 'clear':
                await sleep(3)
                self.backend.push_data(f'Discord/{message.guild.id}/last_messages', {message.channel.id: [[message.id, message.author.id] async for message in message.channel.history(limit=50)]})
            else:
                await self._spare(message)
        else:
            await self._spare(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        self.backend.push_data(f'Discord/{message.guild.id}/last_messages', {message.channel.id: [[message.id, message.author.id] async for message in message.channel.history(limit=50)]})

    async def _push(self, path: str, author_id: int):
        try:
            self.backend.push_data(path, {author_id: self.backend.get_data(f'{path}/{author_id}') + 1})
        except TypeError:
            return

    async def _msg_normalize(self):
        for guild in self.client.guilds:
            for channel in guild.channels:
                try:
                    async for message in channel.history(limit=50):
                        if (lst := self.backend.get_data(f'Discord/{guild.id}/last_messages/{channel.id}')) is not None:
                            if [message.id, message.author.id] not in lst:
                                await self._push(f'Discord/{guild.id}/messages', message.author.id)
                            else:
                                break
                        else:
                            await self._push(f'Discord/{guild.id}/messages', message.author.id)
                    last_messages = [[message.id, message.author.id] async for message in channel.history(limit=50)]
                    if last_messages:
                        self.backend.push_data(f'Discord/{guild.id}/last_messages/', {channel.id: last_messages})
                except AttributeError:
                    pass

    @staticmethod
    async def _del_s_links(links: list):
        async with ClientSession() as session:
            for key in links:
                spare_payload['key'] = key
                async with session.post(url=vk_urls.get('delete_short_link'), data=spare_payload) as _:
                    return

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            if (lst := self.backend.get_data(f'Discord/{guild.id}/short_links')) is not None:
                if len(lst.keys()) > 25:
                    await self._del_s_links(list(dict(list(lst.items())[len(lst.keys())-25:]).keys()))
                    self.backend.push_data(f'Discord/{guild.id}', {'short_links': dict(list(lst.items())[:len(lst.keys())-25])})
        for guild in self.client.guilds:
            for member in guild.members:
                if self.backend.get_data(f'Discord/{guild.id}/messages/{member.id}') is None:
                    self.backend.push_data(f'Discord/{guild.id}/messages', {member.id: 0})
        await self._msg_normalize()
        print('Messages have been loaded')


async def setup(client):
    await client.add_cog(CogEvents(client, Functions('events')))
