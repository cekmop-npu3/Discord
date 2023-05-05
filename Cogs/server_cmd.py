from discord.ext import commands
from discord import app_commands, Interaction, Embed, Color
from datetime import datetime
from time import mktime

from Discord.Backend.engine import Functions


class CogServerCmd(commands.Cog):
    def __init__(self, backend) -> None:
        self.backend = backend

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
        embed.add_field(name='**Roles**', value='\n'.join(map(lambda x: ' -  '+str(x), interaction.guild.roles[1::])), inline=False)
        embed.set_footer(text='[PWNZ]Community')
        await interaction.followup.send(embed=embed)

    @app_commands.command(name='server_top', description='The most active users')
    async def server_top(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        top = self.backend.get_data(f'Discord/{interaction.guild.id}/messages')
        embed = Embed(
            title=f'**{interaction.guild.name}**',
            description=f"{sum(top.values())} messages",
            color=Color.brand_green(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url='https://emoji.discadia.com/emojis/4bb53359-5c67-437f-9d45-b2cbc8469a02.PNG')
        embed.set_footer(text='[PWNZ]Community')
        top_users = (lst := sorted(list(filter(lambda x: x[1] > 0, list(top.items()))), key=lambda x: x[1], reverse=True))[:len(lst) if len(lst) < 10 else 10]
        [embed.add_field(name=f'{count}. {await interaction.guild.fetch_member(int(value[0]))}', value=f'{value[1]} messages', inline=False) for count, value in enumerate(top_users, start=1)]
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

    @app_commands.command(name='rules', description='Function is deprecated')
    async def rules(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        if any(list(map(lambda x: str(x).lower().endswith('админ'), interaction.user.roles))):
            embed = Embed(
                title='**Rules**',
                color=Color.brand_green(),
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url='https://emoji.discadia.com/emojis/46c1fdf5-c2da-427e-9464-d29e3b14eee9.png')
            embed.set_footer(text='[PWNZ]Community')
            embed.add_field(
                name='**1. Общие положения**',
                value='```'
                      '- Участники сервера Дискорд равны перед правилами вне зависимости от опыта и роли.\n'
                      '- Мат разрешается, но без злоупотребления.\n'
                      '- Запрещено оскорбление других пользователей.\n'
                      '- Запрещено злоупотребление Caps Lock.'
                      '```',
                inline=False
            )
            embed.add_field(
                name='**2. Размещение ссылок**',
                value='```'
                      '-Запрещается реклама без согласования с администратором.\n'
                      '-Не допускается спам-рассылка в личных СМС с другими пользователями.'
                      '```',
                inline=False
            )
            embed.add_field(
                name='**3. Ники и аватарки**',
                value='```'
                '- Администратор вправе требовать изменение ника и картинки, '
                'если считает, что они оскорбляют кого-либо.\n'
                '- Запрещены ники типа User, Discord User, NickName и прочие, '
                'в том числе Admin, Moderator и т. д.\n'
                '- Запрещено использование имен с рекламой, пропагандой алкоголя / наркотиков.\n'
                '- Не допускается применение символики террористов и запрещенных организации, '
                'призыв к насилию и экстремизму.\n'
                '- Нельзя использовать бессмысленный набор символов с многократным '
                'повторением одной или нескольких букв.\n'
                '```',
                inline=False
            )
            embed.add_field(
                name='**4. Ответственность**',
                value='```'
                      '- При нарушении правил сервера Дискорд принимаются меры к пользователям вплоть до '
                      'ограничения доступа.\n'
                      '- Обход бана путем входа под другим идентификатором или иными путями — бан.\n'
                      '- Администратор ДС вправе отказать в доступе любому участнику. '
                      'Он не обязан указывать причины или предупреждать об этом.\n'
                      'Нарушение упомянутых выше норм — бан.\n'
                      '- Разжигание межнациональной розни, конфликтов на политической и религиозном основании — бан.'
                      '```',
                inline=False
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(content='**InappropriateRuleError:** Admin rules are required')


async def setup(client):
    await client.add_cog(CogServerCmd(Functions('server_cmd')))
