from discord.ui import View, Select, Button, Modal, TextInput


class CustomView(View):
    def __init__(self, items):
        super().__init__(timeout=None)
        [self.add_item(item) for item in items] if isinstance(items, list) else self.add_item(items)


class Menu(Select):
    def __init__(self, options):
        super().__init__(options=options, placeholder='Выберите изображение из списка')

    async def callback(self, interaction):
        await interaction.response.defer()
        [await interaction.edit_original_response(content=i, view=CustomView(self)) for i in self.values]


class MusicButton(Button):
    def __init__(self, label, func):
        super().__init__(label=label)
        self.func = func

    async def callback(self, interaction):
        await interaction.response.defer()
        await self.func(interaction)
