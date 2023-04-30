from firebase_admin import initialize_app
from firebase_admin import credentials
from firebase_admin import db
import firebase_admin

import Discord.config as config


class Base:
    def __init__(self, name):
        self.url = config.database_url
        self.cert = config.database_cert
        self.name = name
        self._connect()

    def _connect(self):
        initialize_app(credentials.Certificate(self.cert), {'databaseURL': self.url}, name='[DEFAULT]')

    @staticmethod
    def get_data(ref_path: str):
        ref = db.reference(ref_path)
        return ref.get()

    @staticmethod
    def update_data(ref_path: str, json: dict):
        ref = db.reference(ref_path)
        ref.update(json)

    @staticmethod
    def push_data(ref_path: str, data):
        ref = db.reference(ref_path)
        ref.push(data)
