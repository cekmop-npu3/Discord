from firebase_admin import initialize_app, credentials, db, storage

import Discord.Setup.config as config


class Base:
    def __init__(self, name):
        self.url = config.database_url
        self.storage_url = config.database_storage_url
        self.cert = config.database_cert
        self.name = name
        self.app = None
        self._connect()

    def _connect(self):
        initialize_app(credentials.Certificate(self.cert), {'databaseURL': self.url, 'storageBucket': self.storage_url}, name=self.name)

    @staticmethod
    def get_data(ref_path: str):
        ref = db.reference(ref_path)
        return ref.get()

    @staticmethod
    def push_data(ref_path: str, json: dict):
        ref = db.reference(ref_path)
        ref.update(json)

    @staticmethod
    def delete_data(ref_path: str):
        ref = db.reference(ref_path)
        ref.delete()

    @staticmethod
    def upload_file(blob_name: str, data: bytes):
        bucket = storage.bucket()
        blob = bucket.blob(blob_name)
        blob.upload_from_string(data=data)


#base = Base('[DEFAULT]')
#base.push_data('Discord', {'Cookies': [
#    'getimgauth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImI2N2UyNTYxLTQ0ODYtNGI4My1iYmVlLTg5NWJkMzllMzU0ZCIsImlhdCI6MTY4NTQzNTc5MywiZXhwIjoxNjg2MDQwNTkzfQ.M0E8RCQFIml46VvzqYk8LWG5BPGedjLUndAmuhspnA4',
#    'getimgauth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImRhMmJjZjJhLTU5NzQtNDYyZS04OWY4LWE3MmIxZTM2MDQ2NCIsImlhdCI6MTY4NTUzMzM3NiwiZXhwIjoxNjg2MTM4MTc2fQ.hmcfk5oXVeSODe8wp0VwED8_frIdkO_Q2CmMdC8CR6I',
#    'getimgauth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImM1MDk3NmFjLTc0ZDktNGYxYi1hODA1LTMzNTZkZDI2NGFjNCIsImlhdCI6MTY4NTU1NDEyMCwiZXhwIjoxNjg2MTU4OTIwfQ.3QdmVn-6xLJ6ZUbeIJopB9nd8E-ASnxK8bdvfHgjCtA',
#    'getimgauth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg5MzZmZGIwLTE2MGMtNGVjNy04NzYzLThlZjE4NWI2NWUzMyIsImlhdCI6MTY4NTU1NTE1MywiZXhwIjoxNjg2MTU5OTUzfQ.gjFTjjaJYjHAsSxAifh0bNXWHhqJNs9I00d8dOPAPgE',
#    'getimgauth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjZkNTNmOTExLTA3NzUtNDk4YS1hNTU4LTVlYjZiYzM5ZWI3NSIsImlhdCI6MTY4NTM3MTg1NSwiZXhwIjoxNjg1OTc2NjU1fQ.LQfC2yXVGrNHIukdhhKO834LFm2kWuwMONes7ZROqWU',
#    'getimgauth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNhYjQ4NWE1LTQ3NWMtNGZmNi1hN2QyLWNmMmU4YTQ1ZDAwZiIsImlhdCI6MTY4NTcyODQ3NywiZXhwIjoxNjg2MzMzMjc3fQ.A0H6h7tEw27-BgQYcdUCj3VPBLaNJe0pBGxhFPaOLOg',
#    'getimgauth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImUxNmM3ZDZmLTIwYTMtNDkyOC05OTcxLWU0Y2YxMjNkMzU0YSIsImlhdCI6MTY4NTczNTgwMiwiZXhwIjoxNjg2MzQwNjAyfQ.auD-LaHukvK8ylsG_KzBoJ6bKv7ZKorfrMohRXwuf2M',
#]})
