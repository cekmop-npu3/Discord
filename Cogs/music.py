from discord.ext import commands
from discord import app_commands, Interaction, VoiceClient, FFmpegPCMAudio, Embed, Color
from datetime import datetime

from Discord.Backend.engine import Functions
from Discord.Backend.ui import CustomView, MusicButton


class CogMusic(commands.Cog):
    def __init__(self, client, backend):
        self.client = client
        self.backend = backend
        self.switch = list()
        self.track_name = str()

    @app_commands.describe(owner_id='Ссылка на профиль вк или id')
    @app_commands.command(name='create_playlist', description='Create a playlist from user or group audios')
    async def create_playlist(self, interaction: Interaction, owner_id: str):
        await interaction.response.defer(thinking=True)
        await interaction.followup.send(content='**Music is loading...**')
        text = await self.backend.create_playlist(interaction, owner_id)
        await interaction.edit_original_response(content=text)

    async def search_vc(self, interaction, track_name, track_url):
        for voice_client in self.client.voice_clients:
            if interaction.user.voice.channel == voice_client.channel:
                voice_client: VoiceClient = voice_client
                break
            else:
                if interaction.guild == voice_client.guild:
                    await interaction.user.move_to(voice_client.channel)
                    break
        else:
            voice_client: VoiceClient = await interaction.user.voice.channel.connect()
        if voice_client.is_playing():
            voice_client.stop()
        self.switch = ['paused', 'resumed']
        self.track_name = track_name
        voice_client.play(FFmpegPCMAudio(source=track_url, executable=r'D:/PythonProject/Discord/Backend/ffmpeg.exe'))

    async def embed_edit(self, interaction, track_name, artist, button='⏸️'):
        embed = Embed(
            title='**Music player**',
            color=Color.brand_green(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url='https://emoji.discadia.com/emojis/8f38959e-2f7b-4eec-904b-2be82b129043.PNG')
        embed.set_footer(text='[PWNZ]Community')
        embed.add_field(
            name=f'**{artist}**',
            value=track_name
        )
        await interaction.edit_original_response(embed=embed, view=CustomView(
            [MusicButton(label=label, func=func) for label, func in
             zip(['⏪', '⏹️', button, '🔁', '⏩'], [self.left, self.stop, self.pause_resume, self.repeat, self.right])]))

    @app_commands.command(name='play', description='Search and play music from your playlist')
    async def play(self, interaction: Interaction, track_name: str):
        await interaction.response.defer(thinking=True)
        if interaction.user.voice:
            if (lst := self.backend.get_data(f'Discord/{interaction.guild.id}/playlist')) is not None:
                if track_name:
                    for name in lst.keys():
                        if ' '.join(''.join(list(map(lambda x: str(x) if (x.isalpha() or x.isdigit()) else ' ', track_name))).split()).lower() in name:
                            data = self.backend.get_data(f'Discord/{interaction.guild.id}/playlist/{name}')
                            await self.search_vc(interaction, name, data.get('url'))
                            embed = Embed(
                                title='**Music player**',
                                color=Color.brand_green(),
                                timestamp=datetime.now()
                            )
                            embed.set_thumbnail(
                                url='https://emoji.discadia.com/emojis/8f38959e-2f7b-4eec-904b-2be82b129043.PNG')
                            embed.set_footer(text='[PWNZ]Community')
                            embed.add_field(
                                name=f'**{data.get("artist")}**',
                                value=data.get('title')
                            )
                            await interaction.followup.send(embed=embed, view=CustomView(
                                [MusicButton(label=label, func=func) for label, func in
                                 zip(['⏪', '⏹️', '⏸️', '🔁', '⏩'], [self.left, self.stop, self.pause_resume, self.repeat, self.right])]))
                            break
                    else:
                        await interaction.followup.send(content='**An Error occurred, type track name another way**')
            else:
                await interaction.followup.send(content="**You haven't got any playlist yet. You can create one using /create_playlist**")
        else:
            await interaction.followup.send(content='**You are not in a voice channel**')

    async def repeat(self, interaction):
        if interaction.user.voice:
            if (data := self.backend.get_data(f'Discord/{interaction.guild.id}/playlist/{self.track_name}')) is not None:
                await self.embed_edit(
                    interaction,
                    data.get('title'),
                    data.get('artist'),
                    '⏸️'
                )
                await self.search_vc(interaction, self.track_name, data.get('url'))
        else:
            await interaction.followup.send(content="**Bot is not in a voice channel**")

    async def left(self, interaction):
        if interaction.guild.voice_client:
            if (data := self.backend.get_data(f'Discord/{interaction.guild.id}/playlist')) is not None:
                track_name = (lst := list(data.keys()))[lst.index(self.track_name) - 1 if lst.index(self.track_name) > 0 else len(lst) - 1]
                await self.embed_edit(interaction, data.get(track_name).get('title'), data.get(track_name).get("artist"))
                await self.search_vc(interaction, track_name, data.get(track_name).get('url'))
        else:
            await interaction.followup.send(content="**Bot is not in a voice channel**")

    async def right(self, interaction):
        if interaction.guild.voice_client:
            if (data := self.backend.get_data(f'Discord/{interaction.guild.id}/playlist')) is not None:
                track_name = (lst := list(data.keys()))[lst.index(self.track_name) + 1 if len(lst) > lst.index(self.track_name) + 1 else 0]
                await self.embed_edit(interaction, data.get(track_name).get('title'), data.get(track_name).get("artist"))
                await self.search_vc(interaction, track_name, data.get(track_name).get('url'))
        else:
            await interaction.followup.send(content="**Bot is not in a voice channel**")

    async def stop(self, interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect(force=True)
            await interaction.delete_original_response()
        else:
            await interaction.followup.send(content="**Bot is not in a voice channel**")

    async def pause_resume(self, interaction):
        if interaction.user.voice:
            for voice_client in self.client.voice_clients:
                if interaction.user.voice.channel == voice_client.channel:
                    voice_client = voice_client
                    voice_client.pause() if self.switch[0] == 'paused' else voice_client.resume()
                    if (data := self.backend.get_data(f'Discord/{interaction.guild.id}/playlist/{self.track_name}')) is not None:
                        await self.embed_edit(interaction, data.get('title'), data.get("artist"), '▶️' if self.switch[0] == 'paused' else '⏸️')
                        self.switch = self.switch[::-1]
                    break
            else:
                await interaction.followup.send(content="**Bot is not in a voice channel**")
        else:
            await interaction.followup.send(content='**You are not in a voice channel**')


async def setup(client):
    await client.add_cog(CogMusic(client, Functions('music')))
