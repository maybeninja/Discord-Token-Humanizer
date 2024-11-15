import base64
import random
import os
from base64 import b64encode
from helpers.fingerprints import get_ja3_session, get_headers
import requests
from helpers.log import uiprint

def image_to_base64(image_path):
    """Convert image file to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = b64encode(image_file.read()).decode("utf-8")
        return encoded_image
    except Exception as e:
        uiprint('failed', f'Error converting image to base64: {e}')
        return None

def update_avatar(token: str) -> bool:
    """Update the user's avatar with a random image from the input folder"""
    try:
        session, x_super_properties, user_agent = get_ja3_session()
        headers = get_headers(token, x_super_properties, user_agent)

        avatar_folder = 'input/avatars/'
        image_files = [f for f in os.listdir(avatar_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            uiprint('warn', 'Avatars Folder Is Empty')
            return False  
        
        random_image = random.choice(image_files)
        image_path = os.path.join(avatar_folder, random_image)

        avatar_base64 = image_to_base64(image_path)
        if avatar_base64 is None:
            return False   

        file_extension = random_image.split('.')[-1].lower()
        if file_extension in ['png', 'jpg', 'jpeg']:
            mime_type = f"image/{file_extension}"
        else:
            mime_type = "image/png" 

        payload = {"avatar": f"data:{mime_type};base64,{avatar_base64}"}

        url = "https://discord.com/api/v9/users/@me"

        response = session.patch(url, json=payload, headers=headers)

        if response.status_code == 200:
            uiprint('success', f"Avatar updated successfully for {token[:25]}")
            return True
        else:
            uiprint('failed', f"Failed to update avatar for {token[:25]}, Response: {response.text}")
            return False
    except Exception as e:
        uiprint('failed', f"Error encountered while updating avatar for {token[:25]}: {e}")
        return False
