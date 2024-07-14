import requests
import hashlib

class UUIDUtils:
    @staticmethod
    def get_uuid(username):
        url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['id']
        else:
            raise Exception("Failed to get UUID")

    @staticmethod
    def construct_offline_player_uuid(username):
        md5_hash = hashlib.md5(("OfflinePlayer:" + username).encode('utf-8')).hexdigest()
        data = bytearray.fromhex(md5_hash)
        data[6] = (data[6] & 0x0f) | 0x30
        data[8] = (data[8] & 0x3f) | 0x80
        return UUIDUtils.create_java_uuid(data.hex())

    @staticmethod
    def create_java_uuid(striped):
        components = [
            striped[:8],
            striped[8:12],
            striped[12:16],
            striped[16:20],
            striped[20:]
        ]
        return '-'.join(components)
