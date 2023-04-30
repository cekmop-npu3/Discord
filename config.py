bot_token = 'MTAyODYwOTYzNzU4MDI3OTgzOA.G_yF1U.gllWW5N6DSGir2JopmDqJY0G9Z6mX8H70Ymemo'
access_token = 'vk1.a.OUjrQ08fbN-2ms5FcVInuAvmWAPPKQ0ZcIhD4WC6EwL_xs0eZn_DOCIq1j_tDZ-ilfIWFEqlctZ0EJ74eaZPooEu_ckxuYjZXeEgTWqsgqE9de16vV-ZRjN16uHm9rTKjsICsDOs9ISrePm1tBYM8JDj-yYFzS8UnWZQHZx0Dd0TsuK-LrukxChgG9pRdrYdWFdjwQHzk8-yYSqD93cXUQ'

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
    'check_status': 'https://api.vk.com/method/asr.checkStatus?v=5.123&client_id=51431207'
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
