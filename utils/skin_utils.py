import requests
import base64
import json
from PIL import Image
from io import BytesIO

class SkinUtils:
    @staticmethod
    def get_skin_url(uuid):
        url = f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for property in data['properties']:
                if property['name'] == 'textures':
                    texture_data = base64.b64decode(property['value']).decode('utf-8')
                    texture_json = json.loads(texture_data)
                    return texture_json['textures']['SKIN']['url']
        else:
            raise Exception("Failed to get skin URL")

    @staticmethod
    def get_skin_image(url):
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            raise Exception("Failed to download skin")

    @staticmethod
    def extract_head(skin):
        head_coords = (8, 8, 16, 16)
        head = skin.crop(head_coords).convert('RGBA')
        return head
