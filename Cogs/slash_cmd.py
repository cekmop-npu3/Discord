from discord.ext import commands
from discord import app_commands, Interaction

from Discord.Backend.engine import Functions


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

    @app_commands.command(name='imagine', description='Generate images with CraiyonV3')
    async def imagine(self, interaction: Interaction, prompt: str, style: str):
        await self.spare(
            interaction,
            'https://api.craiyon.com/v3',
            {'prompt': prompt, 'model': style.lower(), 'version': '35s5hfwn9n78gb06', 'negative_prompt': ''}
        )

    @app_commands.command(name='clear', description='Clears a certain amount of messages. Admin rules are required')
    async def clear(self, interaction: Interaction, value: int):
        await interaction.response.defer(thinking=True)
        if any(list(map(lambda x: str(x).endswith('админ'), interaction.user.roles))) and value <= 100:
            await interaction.channel.purge(limit=value)
        else:
            await interaction.followup.send(content='**InappropriateRuleError:** Admin rules are required')


async def setup(client):
    await client.add_cog(CogSlashCmd(Functions('slash_cmd')))
