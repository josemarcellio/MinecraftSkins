import os
import json
from PIL import Image

class ImageUtils:
    @staticmethod
    def get_front_skin_positions():
        with open('data/position.json', 'r') as file:
            data = json.load(file)
        
        front_parts_coords = {key: tuple(value) for key, value in data['front_parts_coords'].items()}
        front_positions = {key: tuple(value) for key, value in data['front_positions'].items()}

        return front_parts_coords, front_positions

    @staticmethod
    def generate_front_body(skin, output_image, scale_factor=10):
        front_parts_coords, front_positions = ImageUtils.get_front_skin_positions()

        for part, coords in front_parts_coords.items():
            part_image = skin.crop(coords).convert('RGBA')
            scaled_size = (coords[2] - coords[0]) * scale_factor, (coords[3] - coords[1]) * scale_factor
            part_image = part_image.resize(scaled_size, Image.NEAREST)
            output_position = (front_positions[part][0] * scale_factor, front_positions[part][1] * scale_factor)
            output_image.paste(part_image, output_position, part_image)

    @staticmethod
    def print_image_in_console(image, scale_factor=10):
        image = image.resize((image.width // scale_factor, image.height // scale_factor), Image.NEAREST)
        for y in range(image.height):
            for x in range(image.width):
                r, g, b, a = image.getpixel((x, y))
                if a == 0:
                    print(' ', end='')
                else:
                    print(f'\033[38;2;{r};{g};{b}m█\033[0m', end='')
            print()

    @staticmethod
    def save_image(image, path):
        image.save(path)

    @staticmethod
    def create_folder(username):
        if not os.path.exists(username):
            os.makedirs(username)

    @staticmethod
    def check_and_save_image(image, path):
        if os.path.exists(path):
            replace = input(f"{path} already exists. Do you want to replace it? (y/n): ")
            if replace.lower() != 'y':
                print(f"Skipped saving {path}.")
                return
        ImageUtils.save_image(image, path)
        print(f"Image saved as {path}.")
