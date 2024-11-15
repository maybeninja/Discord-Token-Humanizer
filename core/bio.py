from helpers.fingerprints import get_ja3_session, get_headers
import random
from helpers.log import uiprint

def get_random_bio():
    """Get a random bio from the bio.txt file."""
    try:
        with open("input/bio.txt", "r", encoding="utf-8") as file:
            bios = [line.strip() for line in file if line.strip()]
        if bios:
            return random.choice(bios)
        else:
            uiprint('warn', "No valid bios found in bio.txt, using default bio.")
            return "Default bio text"
    except FileNotFoundError:
        uiprint('warn', "bio.txt file not found, using default bio.")
        return "Default bio text"
    except Exception as e:
        uiprint('failed', f"Error reading bio.txt: {e}")
        return "Default bio text"

def update_bio(token: str) -> bool:
    """Update the bio of a Discord account."""
    bio = get_random_bio()

    session, x_super_properties, user_agent = get_ja3_session()
    headers = get_headers(token, x_super_properties, user_agent)

    url = "https://discord.com/api/v9/users/@me"
    payload = {"bio": bio}

    try:
        response = session.patch(url, json=payload, headers=headers)
        if response.status_code == 200:
            uiprint('success', f"Bio updated successfully for {token[:25]}")
            return True
        else:
            uiprint('failed', f"Failed to update bio for {token[:25]}, Response: {response.text}")
            return False
    except Exception as e:
        uiprint('failed', f"Error encountered while updating bio for {token[:25]}: {e}")
        return False
