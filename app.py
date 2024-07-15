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

        choice = input("Choose an option:\n1. Download skin\n2. Change body\nEnter your choice (1 or 2): ")

        if choice == '1':
            download_choice = input("Type to download:\n1. Skin texture\n2. Skin 2D output image\n3. Head image\n4. Download all\nEnter your choice (1, 2, 3, or 4): ")

            ImageUtils.create_folder(username)

            if download_choice == '1':
                path = f'{username}/{username}_skin_texture.png'
                ImageUtils.check_and_save_image(skin, path)
            elif download_choice == '2':
                path = f'{username}/{username}_skin_2d_output.png'
                ImageUtils.check_and_save_image(output_image, path)
            elif download_choice == '3':
                head = SkinUtils.extract_head(skin)
                path = f'{username}/{username}_head.png'
                ImageUtils.check_and_save_image(head, path)
            elif download_choice == '4':
                path = f'{username}/{username}_skin_texture.png'
                ImageUtils.check_and_save_image(skin, path)
                path = f'{username}/{username}_skin_2d_output.png'
                ImageUtils.check_and_save_image(output_image, path)
                head = SkinUtils.extract_head(skin)
                path = f'{username}/{username}_head.png'
                ImageUtils.check_and_save_image(head, path)
            else:
                print("Invalid choice. No files were saved.")

        elif choice == '2':
            new_username = input("Enter the username for the new body: ")
            new_uuid = UUIDUtils.get_uuid(new_username)
            new_skin_url = SkinUtils.get_skin_url(new_uuid)
            new_skin = SkinUtils.get_skin_image(new_skin_url)
            print("New body skin texture URL retrieved successfully.")

            if new_skin.mode != 'RGBA':
                new_skin = new_skin.convert('RGBA')

            new_skin_with_old_head = ImageUtils.replace_body_with_new(new_skin, skin)
            ImageUtils.create_folder(f'{username}_{new_username}_body')

            path = f'{username}_{new_username}_body/{username}_{new_username}_body.png'
            ImageUtils.check_and_save_image(new_skin_with_old_head, path)
            print(f"New body with old head saved as {path}")

            scale_factor = 12
            output_image = Image.new('RGBA', (216, 408), (0, 0, 0, 0))
            ImageUtils.generate_front_body(new_skin_with_old_head, output_image, scale_factor)

            ImageUtils.print_image_in_console(output_image, scale_factor)

        else:
            print("Invalid choice. No action taken.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
