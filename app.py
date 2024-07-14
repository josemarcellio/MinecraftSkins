from utils.uuid_utils import UUIDUtils
from utils.skin_utils import SkinUtils
from utils.image_utils import ImageUtils
from PIL import Image

def main():
    username = input("Enter Minecraft username: ")
    try:
        uuid = UUIDUtils.get_uuid(username)
        offline_uuid = UUIDUtils.construct_offline_player_uuid(username)
        print(f"Online UUID for {username}: {uuid}")
        print(f"Offline UUID for {username}: {offline_uuid}")

        skin_url = SkinUtils.get_skin_url(uuid)
        skin = SkinUtils.get_skin_image(skin_url)
        print("Skin texture URL retrieved successfully.")

        if skin.mode != 'RGBA':
            skin = skin.convert('RGBA')

        scale_factor = 12
        output_image = Image.new('RGBA', (216, 408), (0, 0, 0, 0))
        ImageUtils.generate_front_body(skin, output_image, scale_factor)

        ImageUtils.print_image_in_console(output_image, scale_factor)

        choice = input("Type to download:\n1. Skin texture\n2. Skin 2D output image\n3. Head image\n4. Download all\nEnter your choice (1, 2, 3, or 4): ")

        ImageUtils.create_folder(username)

        if choice == '1':
            path = f'{username}/{username}_skin_texture.png'
            ImageUtils.check_and_save_image(skin, path)
        elif choice == '2':
            path = f'{username}/{username}_skin_2d_output.png'
            ImageUtils.check_and_save_image(output_image, path)
        elif choice == '3':
            head = SkinUtils.extract_head(skin)
            path = f'{username}/{username}_head.png'
            ImageUtils.check_and_save_image(head, path)
        elif choice == '4':
            path = f'{username}/{username}_skin_texture.png'
            ImageUtils.check_and_save_image(skin, path)
            path = f'{username}/{username}_skin_2d_output.png'
            ImageUtils.check_and_save_image(output_image, path)
            head = SkinUtils.extract_head(skin)
            path = f'{username}/{username}_head.png'
            ImageUtils.check_and_save_image(head, path)
        else:
            print("Invalid choice. No files were saved.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
