from discord.ext import commands
from discord import app_commands, Interaction, Embed, Color, File
from discord import SelectOption
from datetime import datetime
from os import remove, path
from requests import get

from Discord.Backend.engine import Functions
from Discord.Setup.config import styles, models
from Discord.Backend.ui import Menu, CustomView


class CogSlashCmd(commands.Cog):
    def __init__(self, backend):
        self.backend = backend

    async def spare(self, interaction, url, data):
        await interaction.response.defer(thinking=True)
        text = await self.backend.create(url, data, interaction)
        if isinstance(text, list):
            await interaction.followup.send(content=text[0], view=CustomView(Menu(options=[SelectOption(label=str(i), value=g) for i, g in zip(range(1, len(text) + 1), text)])))
        else:
            try:
                if path.exists(text):
                    await interaction.followup.send(file=File(text))
                    remove(text)
                else:
                    await interaction.followup.send(content=text)
            except TypeError:
                await interaction.followup.send(content=text)

    @app_commands.command(name='predict', description='Generate text with RuGPT3')
    async def predict(self, interaction: Interaction, prompt: str):
        await self.spare(
            interaction,
            'https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict',
            {'text': prompt}
        )

    @app_commands.command(name='craiyon', description='Generate images with CraiyonV3')
    @app_commands.describe(style='Style of the image')
    @app_commands.choices(style=[
        app_commands.Choice(name=i, value=str(g)) for i, g in zip(['art', 'drawing', 'photo', 'none'], range(4))
    ])
    async def craiyon(self, interaction: Interaction, prompt: str, style: app_commands.Choice[str]):
        await self.spare(
            interaction,
            'https://api.craiyon.com/v3',
            {'prompt': prompt, 'model': style.name, 'version': '35s5hfwn9n78gb06', 'negative_prompt': ''}
        )

    @app_commands.command(name='kandinsky', description='Generate images with Kandinsky 2.1')
    @app_commands.describe(style='Style of the image')
    @app_commands.choices(style=[
        app_commands.Choice(name=i.get('title'), value=i.get('query')) for i in styles
    ])
    async def kandinsky(self, interaction: Interaction, prompt: str, style: app_commands.Choice[str]):
        await self.spare(
            interaction,
            'https://fusionbrain.ai/api/v1/text2image/run',
            {'queueType': 'generate', 'query': prompt, 'preset': 1, 'style': style.value}
        )

    @app_commands.command(name='clear', description='Clears a certain amount of messages. Admin rules are required')
    async def clear(self, interaction: Interaction, value: int):
        await interaction.response.defer(thinking=True)
        if any(list(map(lambda x: str(x).endswith('админ'), interaction.user.roles))):
            await interaction.channel.purge(limit=value + 1)
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

    @app_commands.command(name='generate', description='Generate images with getimg.ai')
    @app_commands.describe(prompt='Type <random> to get random prompt')
    @app_commands.describe(high_res='Boolean variable')
    @app_commands.describe(fix_faces='Boolean variable')
    @app_commands.describe(image_quantity='Number of images (1 - 10)')
    @app_commands.describe(steps='Stands for image quality (1 - 75)')
    @app_commands.describe(guidance_scale='Prompt interpretation (0 - 20)')
    @app_commands.describe(negative_prompt='Negative prompt')
    @app_commands.choices(model=[
        app_commands.Choice(name=i, value=g) for i, g in models
    ])
    @app_commands.choices(ratio=[
        app_commands.Choice(name=i, value=g) for i, g in [['1:1', '512,512'], ['4:5', '512,640'], ['2:3', '512,768'], ['4:7', '512,896'], ['5:4', '640,512'], ['3:2', '768,512'], ['7:4', '896,512']]
    ])
    async def generate(self, interaction: Interaction, model: app_commands.Choice[str], prompt: str, ratio: app_commands.Choice[str], high_res: bool = False, fix_faces: bool = False, image_quantity: int = 1, steps: int = 25, guidance_scale: int = 9, negative_prompt: str = 'Disfigured, cartoon, blurry, nude'):
        await self.spare(
            interaction,
            f'https://getimg.ai/api/models/{model.value}',
            {
                "tool": "generator",
                "num_inference_steps": steps if steps in range(1, 76) else 1,
                "guidance_scale": guidance_scale if guidance_scale in range(0, 20) else 9,
                "num_images": image_quantity if image_quantity in range(1, 11) else 1,
                "width": int(ratio.value.split(',')[0]) * (int(high_res) + 1),
                "height": int(ratio.value.split(',')[1]) * (int(high_res) + 1),
                "enhance_face": str(fix_faces).lower(),
                "scheduler": "dpmsolver++",
                "prompt": prompt if prompt.lower() != 'random' else get('https://getimg.ai/api/prompts/random').json().get('prompt'),
                "negative_prompt": negative_prompt
            }
        )


async def setup(client):
    await client.add_cog(CogSlashCmd(Functions('[DEFAULT]')))
