from discord.ext import commands
from discord import app_commands, Interaction

from Discord.Backend.engine import Functions
from Discord.config import styles


class CogSlashCmd(commands.Cog):
    def __init__(self, backend) -> None:
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
    async def imagine2(self, interaction: Interaction, prompt: str, style: app_commands.Choice[str] = 'none'):
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
    async def imagine(self, interaction: Interaction, prompt: str, size: app_commands.Choice[int] = 768, style: app_commands.Choice[str] = 'no_style'):
        await self.spare(
            interaction,
            'https://api3.rudalle.ru/graphql/',
            {
                'operationName': 'requestKandinsky2Image',
                'query': 'mutation requestKandinsky2Image($input: RequestImageInput!) {\n  requestKandinsky2Image(input: $input) '
                         '{\n    ...ImageRequest\n   __typename\n  }\n}\n'
                         'fragment ImageRequest on ImageRequestEntity {\n  queryId\n}',
                'variables': {
                    'input': {
                        'bf': '601294688103192',
                        'height': 768,
                        'requestText': prompt,
                        'style': style.value,
                        'width': int(size.name)
                    }
                }
            }
        )

    @app_commands.command(name='clear', description='Clears a certain amount of messages. Admin rules are required')
    async def clear(self, interaction: Interaction, value: int):
        await interaction.response.defer(thinking=True)
        if any(list(map(lambda x: str(x).endswith('админ'), interaction.user.roles))) and value <= 100:
            await interaction.channel.purge(limit=value)
        else:
            await interaction.followup.send(content='**InappropriateRuleError:** Admin rules are required')


async def setup(client):
    await client.add_cog(CogSlashCmd(Functions('[DEFAULT]')))
