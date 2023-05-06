from aiohttp import ClientSession, ClientTimeout, FormData
from asyncio.exceptions import TimeoutError
from json import dumps
from typing import Union
from firebase_admin.exceptions import InvalidArgumentError
from discord import Interaction

from Discord.Backend.database import Base
import Discord.Setup.config as config


class Functions(Base):
    def __init__(self, base_name):
        super().__init__(name=base_name)
        self.headers = config.headers
        self.access_token = config.access_token
        self.seconds = 90
        self.timeout = ClientTimeout(total=self.seconds)
        self.upload_url = str()

    async def speech_recognition(self, audio_url: str) -> str:
        async with ClientSession() as session:
            async with session.get(url=audio_url) as file_bytes:
                file = await file_bytes.content.read()
            if not self.upload_url:
                async with session.post(
                        url=config.vk_urls.get('get_upload'),
                        data={'access_token': self.access_token}
                ) as response:
                    self.upload_url = await response.json()
                    self.upload_url = self.upload_url.get('response').get('upload_url')
            data = FormData()
            data.add_field(name='file', value=file)
            async with session.post(
                    url=self.upload_url, data=data,
                    headers={'user-agent': self.headers.get('user-agent')}
            ) as response:
                audio = await response.json()
            if audio.get('error_code') is None:
                async with session.post(
                        url=config.vk_urls.get('process'),
                        data={'audio': dumps(audio), 'model': 'spontaneous', 'access_token': self.access_token}
                ) as response:
                    task_id = await response.json()
                    task_id = task_id.get('response').get('task_id')
                return await self._translate(session, task_id)
            else:
                return '**Internal server error**'

    async def _translate(self, session, task_id) -> str:
        async with session.post(
                url=config.vk_urls.get('check_status'),
                data={'task_id': task_id, 'access_token': self.access_token}
        ) as response:
            text = await response.json()
            while text.get('response').get('status') != 'finished':
                async with session.post(
                        url=config.vk_urls.get('check_status'), data={'task_id': task_id, 'access_token': self.access_token}
                ) as response:
                    text = await response.json()
                continue
        return f"**{text.get('response').get('text')}**" if text.get('response').get('text') else '**Не распознано**'

    async def create(self, url: str, payload: dict) -> str:
        async with ClientSession() as session:
            try:
                async with session.post(url=url, headers=self.headers, json=payload, timeout=self.timeout) as response:
                    response = await response.json()
                    if 'graphql' not in url:
                        return response.get('predictions')[:2000:] if 'gpt3' in url else '\n'.join(
                            list(map(lambda x: 'https://img.craiyon.com/' + x, response.get('images')[:4:]))
                        )
                    else:
                        r = response.get('data').get('requestKandinsky2Image').get('queryId')
                        url = f"https://img2.rudalle.ru/images/{''.join([f'{i}{g}/' for i, g in zip(r[:6:2], r[1:6:2])])}{r}_00000.jpg"
                        async with session.get(url=url) as response:
                            while response.status == 404:
                                async with session.get(url=url) as response:
                                    response = response
                                    continue
                        return url
            except TimeoutError:
                return f'**TimeoutError:** No response within {self.seconds} seconds'

    async def s_link(self, url: str, guild: int) -> str:
        async with ClientSession() as session:
            config.short_link_payload['url'] = url
            async with session.post(url=config.vk_urls.get('get_short_link'),
                                    data=config.short_link_payload) as response:
                response = await response.json()
                if response.get('error') is None:
                    self.push_data(f'Discord/{guild}/short_links',
                                   {response.get('response').get('key'): response.get('response')})
                    return response.get('response').get('short_url')
                else:
                    return '**InvalidUrlError:** Error code 100'

    @staticmethod
    async def spare(response: dict, session, names: list) -> str:
        lst = response.get('response').get('stats')[0].get(names[0])
        config.spare_payload[f'{names[1]}_ids'] = ', '.join([str(i.get(f'{names[1]}_id')) for i in lst])
        async with session.post(url=config.vk_urls.get(f'get_{names[1]}_by_id'), data=config.spare_payload) as response:
            response = await response.json()
            return '\n'.join([f'{key}: {value}' for key, value in
                              zip([i.get('title') for i in response.get('response')], [i.get('views') for i in lst])])

    async def l_stats(self, url: str, interval: str, guild: int) -> Union[list, str]:
        if url.startswith('https://vk.cc/'):
            async with ClientSession() as session:
                data = self.get_data(f'Discord/{guild}/short_links/{url.split("/")[-1]}')
                if data is not None:
                    config.stats_link_payload['access_key'] = data.get('access_key')
                    config.stats_link_payload['key'] = data.get('key')
                    config.stats_link_payload['interval'] = interval
                    async with session.post(url=config.vk_urls.get('get_link_stats'), data=config.stats_link_payload) as response:
                        response = await response.json()
                        if response.get('response').get('stats')[0].get('views') != 0:
                            return [await self.spare(response, session, ['countries', 'country']),
                                    await self.spare(response, session, ['cities', 'city']),
                                    ''.join([f"Age range: {i.get('age_range')}\n - Female: {i.get('female')}\n - Male: {i.get('male')}\n"
                                            for i in response.get('response').get('stats')[0].get('sex_age')]),
                                    response.get('response').get('stats')[0].get('views')
                                    ]
                        else:
                            return 'No Data'
        else:
            return '**InvalidUrlError:** Error code 100'

    async def create_playlist(self, interaction: Interaction, owner_id: int) -> str:
        async with ClientSession() as session:
            config.ls_payload['owner_id'] = owner_id
            async with session.post(url=config.vk_urls.get('load_section'), data=config.ls_payload, headers=config.ls_headers) as response:
                response = await response.json()
                if isinstance(response.get('payload')[0], int):
                    for chunk in response.get('payload')[1][0].get('list'):
                        config.ids_params[1] = ('audios', f'{chunk[1]}_{chunk[0]}_')
                        async with session.get(url=config.vk_urls.get('get_by_id'), params=config.ids_params) as response:
                            response = await response.json()
                            if response.get('error') is None:
                                artist, title, url = response.get('response')[0].get('artist'), response.get('response')[0].get('title'), response.get('response')[0].get('url')
                                artist1 = artist.replace('.', '').replace(',', '').replace('|', '').replace('"', '').replace("'", '').replace('[', '').replace(']', '').lower()
                                title1 = title.replace('.', '').replace(',', '').replace('|', '').replace('"', '').replace("'", '').replace('[', '').replace(']', '').lower()
                                if url:
                                    try:
                                        self.push_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}', {f'{artist1} {title1}': {'url': url, 'artist': artist, 'title': title}})
                                    except InvalidArgumentError:
                                        pass
                    if self.get_data(f'Discord/{interaction.guild.id}/playlists/{interaction.user.id}') is not None:
                        return '**Music has been loaded**'
                    else:
                        return '**An Error occurred, try later**'
                else:
                    return '**An Error occurred, try later**'
