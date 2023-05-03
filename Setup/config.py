bot_token = 'MTAyODYwOTYzNzU4MDI3OTgzOA.G7lh8C.iRO7Gq4hLkdIKrqnjIz0yFX385z9BRkRXNL2yI'
access_token = 'vk1.a.SQwKyzh3fqIhsw5HBwSoYL9j6dk-zxGas1kZ8rny_aNti1KEp-RbMEv2OewK9lGGw3wzCydirr-UxXF4U_e4XiSPLoYbSwKftyxsW9kYTbc_xvFEx6pqEd5oEq9M6C6i2FqKaC6sjDqMdNUaAazXiVW0D_30SKCe-PNHpm2n5M7hJmovG_U1RZdtaRNoIwrXrM6CJ8cRbkQVvLfJgmHxeg'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0',
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'content-type': 'application/json',
    'origin': 'https://russiannlp.github.io',
    'referer': 'https://russiannlp.github.io/',
    'sec-ch-ua-platform': 'Windows'
}
vk_urls = {
    'get_upload': 'https://api.vk.com/method/asr.getUploadUrl?v=5.123&client_id=51431207',
    'process': 'https://api.vk.com/method/asr.process?v=5.123&client_id=51431207',
    'check_status': 'https://api.vk.com/method/asr.checkStatus?v=5.123&client_id=51431207',
    'get_short_link': 'https://api.vk.com/method/utils.getShortLink',
    'get_link_stats': 'https://api.vk.com/method/utils.getLinkStats',
    'get_city_by_id': 'https://api.vk.com/method/database.getCitiesById',
    'get_country_by_id': 'https://api.vk.com/method/database.getCountriesById'
}

database_url = 'https://project-66708-default-rtdb.europe-west1.firebasedatabase.app'
database_cert = {
    "type": "service_account",
    "project_id": "project-66708",
    "private_key_id": "a7609fcce3e7d153df73811451721653990b34f8",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCi6gkk6jd8XeBe\n2iisZgjrWDV4hpCtqhrMYp9nEVa8/6Mo3qjMP20r2Xd5G9OtjtP4O18SfWnrz++E\nC9C5xIpC94Ed3C7Ydo79TkGYnS9NMZA7uoxVDQUst+6DdU96U5POVsuo/aR11mJe\nCiIoUapRAXgutp3OMA+5IXWLVgsovcAcjxzbHDzoG3HpVE2fJyurWouz1uyQBzru\nCAuYtWCtRtG2DUquf0ZyhJByb5XxK/ElqNW8al+7IHALfsK9MI5SzYK+gV0ibYGS\nJsPMLsy9tgw+4hmHxCudZWgaCmdXJoN8DYJCnSA7g0Ws5HOKa7AJL8+ddXBgcdLU\nRHX9kJqpAgMBAAECggEABPQUvxiYA0y0wRg6WwjnMIYIFNgSl2qFUhLq7IQBx9Fb\nW/zD08yskcQU9ou6uJuPz7Zjwk4p5aT25WRD6RdpaiEtvdivW/Q5jh4jrx49t/J6\ng4u9L0DWwsX87JD+j6ZG546KtrgE7h2h9Ate1SxWf2FfZBw4BB2V/M0K+Tzug0M6\noiwkM0BOLcTPE22POYI89BAYp8/+rV4+l4fbwvIz52DrRd11HoKLClgblktnbylK\n619d+DXvW02xfXnpFoEHNGDPL7mhVBvMKAfCewsUlPNkUtHA41nbXHw+0amhzk82\nOKHjTIsfI291f9UQi7P+FV6i7X0IQ+eGI41Ob15S2QKBgQDTsefgRmTLgb4Vyb9Y\nwIJjj06rf9khVw58OA/EE9LQFOyYpeJ8W1uamNY3ywudOW8DHtnAXMSWITo/xaF4\ngq6xBPEYO3ZeiPkN9ym4GNZ6FMqlhJUyi9LetovGiqjJhWAPsQEf4r+/7bncF5id\nxkcxE5BYKDVzNn2X8K49c6UMLwKBgQDFApPrCXmB65c8D5HgAXxL98SyOOAY0LS+\n/yP2/iqSGtvlHRd+l1uoI55WzbgGxuPNpu7FmsGtsTtORUGYoNdK1nd+ZikXukjS\nsjWtula+ZnXmknboNm3/QuLMkR847zFbkzE4scZ2rAH9rENOr/I/k6Ku2xb+15ac\npU6JIcLYpwKBgEJ62yu2T48NRomHGt0fT5M+fOEkvCZZNYZTALh91TVdbNOfPJn7\nArBxEMziqdoNIEylkpJzT5UqCCXgxY2X1I5o0+HdQpX7g+Mb3HEg87HQ97a1BTmj\naWxhfVGzV8A5b2peFtFRnxAB8t0oV9gsXU0PLMRSlD6DPTvK7J0FxS4nAoGAa5jR\n0o81JojV6z6RrCcDjLYAXloDwmnSHXJZYR9FftBego5V85SUwYragowOUt0zM3FV\nfOTdnJBsVH4sqkBF9SCW2JjRHp1mAnTELmLT1188SzZ47LA1eTE9jv4/cCfq7BnC\nyzUEsHGXEMWRaRtdEe3+7sLHl12Fa345G1ouAYcCgYB+n5YJDFqOIUZ9YAbbVHan\n+8tRsRbZia3s7K5BWpljNkKhRZ1HnlnoCbejoyCrU8sNK48OPGNq9Lp0HKwD1pxb\nXcZtYqhtn4WPyuZYxmASmw8L9rvdlzI/942MNHZWZdCvaZNPyIZ9h5juYXsYXeuD\nVu8EjwtLBaFuSCgqekPcNQ==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-yhh5y@project-66708.iam.gserviceaccount.com",
    "client_id": "102558281984619488722",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-yhh5y%40project-66708.iam.gserviceaccount.com"
}

styles = {
    'без стиля': 'no_style',
    'новый год': 'christmas',
    'портретное фото': 'portrait',
    'студийное фото': 'professional_studio',
    'цифровая живопись': 'high_quality_art',
    '3D рендер': '3d_render',
    'советский мультфильм': 'soviet_cartoon',
    'мультфильм': 'cartoon',
    'рисунок карандашом': 'pencil_drawing',
    'мозайка': 'mosaic',
    'иконопись': 'christian_icon',
    'картина маслом': 'oil_painting',
    'ренессанс': 'renaissance',
    'классицизм': 'classicism',
    'хохлома': 'khokhloma',
    'пикассо': 'picasso',
    'малевич': 'malevich',
    'гончарова': 'gonharova',
    'айвазовский': 'aivazovsky',
    'кандинский': 'kandinsky'
}
imagine_payload = {
    'operationName': 'requestKandinsky2Image',
    'query': 'mutation requestKandinsky2Image($input: RequestImageInput!) {\n  requestKandinsky2Image(input: $input) '
             '{\n    ...ImageRequest\n   __typename\n  }\n}\n'
             'fragment ImageRequest on ImageRequestEntity {\n  queryId\n}',
    'variables': {
        'input': {
            'bf': '601294688103192',
            'height': 768,
            'requestText': '',
            'style': '',
            'width': ''
        }
    }
}

short_link_payload = {
    'access_token': access_token,
    'url': '',
    'private': '1',
    'v': '5.131'
}
stats_link_payload = {
    'access_key': '',
    'key': '',
    'access_token': access_token,
    'interval': '',
    'extended': '1',
    'v': '5.131',
}
spare_payload = {
    'access_token': access_token,
    'v': '5.131'
}