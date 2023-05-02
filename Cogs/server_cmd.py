from discord.ext import commands
from discord import app_commands, Interaction, Embed, Color
from datetime import datetime
from time import mktime


class CogServerCmd(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @app_commands.command(name='server', description='Server info')
    async def server(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        embed = Embed(
            title=f'**{interaction.guild.name}**',
            color=Color.brand_green(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name='**Server id**', value=interaction.guild.id, inline=False)
        embed.add_field(name='**Creation date**', value=datetime.fromtimestamp(mktime(interaction.guild.created_at.timetuple())),inline=False)
        embed.add_field(name='**Owner**', value=interaction.guild.owner, inline=False)
        embed.add_field(name='**Members**', value=interaction.guild.member_count, inline=False)
        embed.add_field(name='**Rules channel**', value=interaction.guild.rules_channel, inline=False)
        embed.add_field(name='**Roles**', value='\n'.join(map(str, interaction.guild.roles[1::])), inline=False)
        embed.set_footer(text='[PWNZ]Community')
        await interaction.followup.send(embed=embed)

    @app_commands.command(name='welcome_message', description='Function is deprecated')
    async def welcome_message(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        if any(list(map(lambda x: str(x).lower().endswith('супер-админ'), interaction.user.roles))):
            embed = Embed(
                title='**Добро пожаловать на сервер!**',
                description='```Вам выдана роль ❌--Muted--❌, ограничивающая ваши возможности на сервере. '
                            'Для того, чтобы Вы могли общаться на сервере без ограничений, '
                            'вам следует подождать, пока ваш аккаунт подтвердит администрация и выдаст '
                            'соответствующую роль.```',
                color=Color.brand_green(),
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url='https://emoji.discadia.com/emojis/674dfa4a-5fed-4343-9060-1fa6f6350e0a.png')
            embed.set_footer(text='[PWNZ]Community')
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(content='**InappropriateRuleError:** Admin rules are required')


async def setup(client):
    await client.add_cog(CogServerCmd(client))
