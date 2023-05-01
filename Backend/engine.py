from aiohttp import ClientSession, ClientTimeout, FormData
from asyncio.exceptions import TimeoutError
from json import dumps

from Discord.Backend.database import Base
import Discord.config as config


class Functions(Base):
    def __init__(self, base_name):
        super().__init__(name=base_name)
        self.headers = config.headers
        self.urls = config.vk_urls
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
                        url=self.urls.get('get_upload'),
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
                        url=self.urls.get('process'),
                        data={'audio': dumps(audio), 'model': 'spontaneous', 'access_token': self.access_token}
                ) as response:
                    task_id = await response.json()
                    task_id = task_id.get('response').get('task_id')
                return await self._translate(session, task_id)
            else:
                return '**Internal server error**'

    async def _translate(self, session, task_id) -> str:
        async with session.post(
                url=self.urls.get('check_status'),
                data={'task_id': task_id, 'access_token': self.access_token}
        ) as response:
            text = await response.json()
            while text.get('response').get('status') != 'finished':
                async with session.post(
                        url=self.urls.get('check_status'), data={'task_id': task_id, 'access_token': self.access_token}
                ) as response:
                    text = await response.json()
                continue
        return f"**{text.get('response').get('text')}**" if text.get('response').get('text') else '**Не распознано**'

    async def create(self, url: str, payload: dict) -> str:
        async with ClientSession() as session:
            try:
                async with session.post(url=url, headers=self.headers, json=payload, timeout=self.timeout) as response:
                    response = await response.json()
                    response = response if not 'graphql' in url else response.get('data').get('requestKandinsky2Image').get('queryId')
                    return response.get('predictions')[:2000:] if 'gpt3' in url else (
                        '\n'.join(list(map(lambda x: 'https://img.craiyon.com/' + x, response.get('images')[:4:]))
                                  ) if 'craiyon' in url else f"https://img2.rudalle.ru/images/{''.join([f'{i}{g}/' for i, g in zip(response[:6:2], response[1:6:2])])}{response}_00000.jpg")
            except TimeoutError:
                return f'**TimeoutError:** No response within {self.seconds} seconds'
            