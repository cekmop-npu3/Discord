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
