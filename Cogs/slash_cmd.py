from discord.ext import commands
from discord import app_commands, Interaction, Embed, Color
from datetime import datetime

from Discord.Backend.engine import Functions
from Discord.Setup.config import styles, imagine_payload


class CogSlashCmd(commands.Cog):
    def __init__(self, backend):
        self.backend = backend

    async def spare(self, interaction, url, data):
        await interaction.response.defer(thinking=True)
        text = await self.backend.create(url, data)
        await interaction.followup.send(content=text)

    @app_commands.command(name='predict', description='Generate text with RuGPT3')
    async def predict(self, interaction: Interaction, prompt: str):
        await self.spare(
            interaction,
            'https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict',
            {'text': prompt}
        )

    @app_commands.command(name='imagine2', description='Generate images with CraiyonV3')
    @app_commands.describe(style='Style of the image')
    @app_commands.choices(style=[
        app_commands.Choice(name=i, value=str(g)) for i, g in zip(['art', 'drawing', 'photo', 'none'], range(4))
    ])
    async def imagine2(self, interaction: Interaction, prompt: str, style: app_commands.Choice[str]):
        await self.spare(
            interaction,
            'https://api.craiyon.com/v3',
            {'prompt': prompt, 'model': style.name, 'version': '35s5hfwn9n78gb06', 'negative_prompt': ''}
        )

    @app_commands.command(name='imagine', description='Generate images with Kandinsky 2.1')
    @app_commands.describe(size='Width of the image')
    @app_commands.choices(size=[
        app_commands.Choice(name=i, value=g) for i, g in zip(['768', '1152', '1536'], range(1, 4))

    ])
    @app_commands.describe(style='Style of the image')
    @app_commands.choices(style=[
        app_commands.Choice(name=i, value=g) for i, g in styles.items()
    ])
    async def imagine(self, interaction: Interaction, prompt: str, size: app_commands.Choice[int], style: app_commands.Choice[str]):
        imagine_payload['variables']['input']['requestText'] = prompt
        imagine_payload['variables']['input']['style'] = style.value
        imagine_payload['variables']['input']['width'] = int(size.name)
        await self.spare(interaction, 'https://api3.rudalle.ru/graphql/', imagine_payload)

    @app_commands.command(name='clear', description='Clears a certain amount of messages. Admin rules are required')
    async def clear(self, interaction: Interaction, value: int):
        await interaction.response.defer(thinking=True)
        if any(list(map(lambda x: str(x).endswith('админ'), interaction.user.roles))) and value <= 100:
            await interaction.channel.purge(limit=value+1)
        else:
            await interaction.followup.send(content='**InappropriateRuleError:** Admin rules are required')

    @app_commands.command(name='get_short_link', description='Allows you to get a URL shortened with vk.cc')
    async def short(self, interaction: Interaction, url: str):
        await interaction.response.defer(thinking=True)
        text = await self.backend.s_link(url, interaction.guild.id)
        await interaction.followup.send(content=text)

    @app_commands.command(name='get_link_stats', description='Returns statistics of clicks on a shortened link')
    @app_commands.describe(interval='Unit of time for calculating statistics')
    @app_commands.choices(interval=[
        app_commands.Choice(name=i, value=str(g)) for i, g in zip(['hour', 'day', 'week', 'month', 'forever'], range(5))
    ])
    async def l_stats(self, interaction: Interaction, url: str, interval: app_commands.Choice[str]):
        await interaction.response.defer(thinking=True)
        data = await self.backend.l_stats(url, interval.name, interaction.guild.id)
        embed = Embed(
                title=f'**Link stats**',
                color=Color.brand_green(),
                timestamp=datetime.now()
        )
        embed.set_thumbnail(url='https://emoji.discadia.com/emojis/4bb53359-5c67-437f-9d45-b2cbc8469a02.PNG')
        embed.set_footer(text='[PWNZ]Community')
        if isinstance(data, list):
            [embed.add_field(name=name, value=value, inline=False) for name, value in
             zip(['**1. Countries**', '**2. Cities**', '**3. Sex_Age**', '**4. Total views**'], data)
             ]
            await interaction.followup.send(embed=embed)
        else:
            if 'Error' not in data:
                embed.add_field(
                    name='**Response**',
                    value=data,
                    inline=False
                )
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(content=data)


async def setup(client):
    await client.add_cog(CogSlashCmd(Functions('[DEFAULT]')))
