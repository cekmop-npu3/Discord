from discord.ext import commands
from discord import app_commands, Interaction, Embed, Color
from datetime import datetime


class CogHelpCmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='help', description='A Quick Guide to Slash Commands')
    async def help(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        embed = Embed(
            title='**Доступные команды [PWNZ]Bot**',
            color=Color.brand_green(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url='https://emoji.discadia.com/emojis/240656fb-c20c-4fa4-ab7d-cdf7f829e44e.PNG')
        embed.set_footer(text='[PWNZ]Community')
        embed.add_field(
            name='**1. /predict [prompt]**',
            value='```'
                  'Комманда /predict позволяет воспользоваться '
                  'вычислительными способностями нейросети RuGPT3. '
                  'В чем суть RuGPT3? Эта нейросеть предназначена для создания '
                  'текстового контента: новостей, стихов, рассказов, романов, '
                  'пародий и т.д. Модель содержит 1,3 млрд параметров и умеет '
                  'дописывать текст на русском языке (на английском тоже немного). '
                  'Для этого сначала требуется написать какую-нибудь фразу на '
                  'интересующую вас тему в поле Prompt, и модель ее допишет.'
                  '```',
            inline=False
        )
        embed.add_field(
            name='**2. /imagine [prompt] [style]**',
            value='```'
                  'Команда /imagine - посредник между сервером и упрощённой «сестрой» '
                  'Dall-E 2 - Craiyon. Craiyon представляет собой механизм генерации '
                  'изображений, использующий искусственный интеллект и машинное обучение. '
                  'Чтобы воспользоваться нейросетью, нужно лишь указать в поле Prompt '
                  'текст, описывающий изображение, которое вы хотите увидеть. Поле'
                  'Style позволяет задать стиль итогового изображения. Допустимые значения:'
                  '\n - Art,\n - Drawing,\n - Photo,\n - None.\n'
                  'Работает исключительно на английском языке.'
                  '```',
            inline=False
        )
        embed.add_field(
            name='**3. /clear [value]**',
            value='```Позволяет удалить заданное количество сообщений. Работает при наличии прав админа.'
                  '```',
            inline=False
        )
        await interaction.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(CogHelpCmd(client))
