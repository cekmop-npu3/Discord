from discord.ext import commands
from discord import app_commands, Interaction, VoiceClient, FFmpegPCMAudio
from aiohttp import ClientSession
from firebase_admin.exceptions import InvalidArgumentError

import Discord.Setup.config as config
from Discord.Backend.engine import Functions


class CogMusic(commands.Cog):
    def __init__(self, backend):
        self.backend = backend

    @app_commands.command(name='create_playlist', description='Create a playlist from user or group audios')
    async def create_playlist(self, interaction: Interaction, owner_id: int):
        await interaction.response.defer(thinking=True)
        await interaction.followup.send(content='**Music is loading...**')
        async with ClientSession() as session:
            config.ls_payload['owner_id'] = owner_id
            async with session.post(url=config.vk_urls.get('load_section'), data=config.ls_payload, headers=config.ls_headers) as response:
                response = await response.json()
                if isinstance(response.get('payload')[0], int):
                    for chunk in response.get('payload')[1][0].get('list'):
                        config.ids_params[1] = ('audios', f'{chunk[1]}_{chunk[0]}_')
                        async with session.get(url=config.vk_urls.get('get_by_id'), params=config.ids_params) as response:
                            response = await response.json()
                            if response.get('error') is None:
                                author, title, url = response.get('response')[0].get('artist').lower(), response.get('response')[0].get('title').lower(), response.get('response')[0].get('url')
                                author.replace('.', '').replace(',', '')
                                title.replace('.', '').replace(',', '')
                                if url:
                                    try:
                                        self.backend.push_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}', {f'{author}_{title}': url})
                                    except InvalidArgumentError:
                                        pass
                    if self.backend.get_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}') is not None:
                        await interaction.edit_original_response(content='**Music has been loaded**')
                    else:
                        await interaction.edit_original_response(content='**An Error occurred, try later**')
                else:
                    await interaction.edit_original_response(content='**An Error occurred, try later**')

    @app_commands.command(name='play', description='Search and play music from your playlist')
    async def play(self, interaction: Interaction, track_name: str):
        await interaction.response.defer(thinking=True)
        if interaction.user.voice:
            if self.backend.get_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}') is not None:
                if track_name:
                    for name in list(self.backend.get_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}').keys()):
                        if track_name in name:
                            url = self.backend.get_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}/{name}')
                            voice_client: VoiceClient = await interaction.user.voice.channel.connect()
                            voice_client.play(FFmpegPCMAudio(source=url, executable=r'D:/PythonProject/Discord/Backend/ffmpeg.exe'))
                            await interaction.followup.send(content=f'**{track_name} is playing**')
                            break
                    else:
                        await interaction.followup.send(content='**An Error occurred, type track name another way**')
            else:
                await interaction.followup.send(content="**You haven't got any playlist yet. You can create one using /create_playlist**")
        else:
            await interaction.followup.send(content='**You are not in a voice channel**')


async def setup(client):
    await client.add_cog(CogMusic(Functions('music')))
