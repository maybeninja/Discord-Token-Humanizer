import random
from helpers.fingerprints import get_ja3_session, get_headers
from helpers.log import uiprint

def get_random_pronoun(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            pronouns = [line.strip() for line in file.readlines() if line.strip()]
        if not pronouns:
            uiprint('warn', 'No pronouns found in the file.')
            return "they/them"  
        return random.choice(pronouns)
    except Exception as e:
        uiprint('failed', f"Error reading pronouns file: {e}")
        return "they/them"  
def update_pronoun(token: str) -> bool:
    """Update the user's pronouns with a random pronoun from the pronouns.txt file."""
    try:
        session, x_super_properties, user_agent = get_ja3_session()
        headers = get_headers(token, x_super_properties, user_agent)

        pronoun = get_random_pronoun("input/pronouns.txt")
        
        if not pronoun:  
            uiprint('failed', "No valid pronoun to update.")
            return False

        url = "https://discord.com/api/v9/users/@me/profile"
        payload = {"pronouns": pronoun}

        response = session.patch(url, json=payload, headers=headers)

        if response.status_code == 200:
            uiprint('success', f"Pronouns updated to '{pronoun}'")
            return True
        else:
            uiprint('failed', f"Failed to update pronouns. Response: {response.text}")
            return False
    except Exception as e:
        uiprint('failed', f"Error encountered while updating pronouns: {e}")
        return False
