from discord.ext import commands
from discord import app_commands, Interaction, VoiceClient, FFmpegPCMAudio, Embed, Color
from datetime import datetime

from Discord.Backend.engine import Functions


class CogMusic(commands.Cog):
    def __init__(self, client, backend):
        self.client = client
        self.backend = backend
        self.voice_clients = list()

    @app_commands.command(name='create_playlist', description='Create a playlist from user or group audios')
    async def create_playlist(self, interaction: Interaction, owner_id: int):
        await interaction.response.defer(thinking=True)
        await interaction.followup.send(content='**Music is loading...**')
        text = await self.backend.create_playlist(interaction, owner_id)
        await interaction.edit_original_response(content=text)

    @app_commands.command(name='play', description='Search and play music from your playlist')
    async def play(self, interaction: Interaction, track_name: str):
        await interaction.response.defer(thinking=True)
        if interaction.user.voice:
            if self.backend.get_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}') is not None:
                if track_name:
                    for name in list(self.backend.get_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}').keys()):
                        if track_name.lower() in name:
                            data = self.backend.get_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}/{name}')
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
                            voice_client.play(FFmpegPCMAudio(source=data.get('url'), executable=r'D:/PythonProject/Discord/Backend/ffmpeg.exe'))
                            embed = Embed(
                                title='**Music player**',
                                color=Color.brand_green(),
                                timestamp=datetime.now()
                            )
                            embed.set_thumbnail(url='https://emoji.discadia.com/emojis/8f38959e-2f7b-4eec-904b-2be82b129043.PNG')
                            embed.set_footer(text='[PWNZ]Community')
                            embed.add_field(
                                name=f'**{data.get("artist")}**',
                                value=data.get('title')
                            )
                            await interaction.followup.send(embed=embed)
                            break
                    else:
                        await interaction.followup.send(content='**An Error occurred, type track name another way**')
            else:
                await interaction.followup.send(content="**You haven't got any playlist yet. You can create one using /create_playlist**")
        else:
            await interaction.followup.send(content='**You are not in a voice channel**')

    async def spare(self, interaction, text: str):
        await interaction.response.defer(thinking=True)
        if interaction.user.voice:
            for voice_client in self.client.voice_clients:
                if interaction.user.voice.channel == voice_client.channel:
                    voice_client: VoiceClient = voice_client
                    voice_client.pause() if text == 'paused' else voice_client.resume()
                    await interaction.followup.send(content=f"**Music is {text}**")
                    break
            else:
                await interaction.followup.send(content="**Bot is not in a voice channel**")
        else:
            await interaction.followup.send(content='**You are not in a voice channel**')

    @app_commands.command(name='pause', description='Pause playing audio')
    async def pause(self, interaction: Interaction):
        await self.spare(interaction, 'paused')

    @app_commands.command(name='resume', description='Resume playing audio')
    async def resume(self, interaction: Interaction):
        await self.spare(interaction, 'resumed')

    @app_commands.command(name='stop', description='Kick out the bot from voice channel')
    async def stop(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect(force=True)
            await interaction.followup.send(content='**Bot has been kicked out**')


async def setup(client):
    await client.add_cog(CogMusic(client, Functions('music')))
