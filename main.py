import yaml
import threading
import os,requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.bio import update_bio
from core.avatars import update_avatar
from core.pronouns import update_pronoun
from helpers.log import uiprint  # Your custom logger

# Load configuration
with open('config.yaml') as f:
    config = yaml.safe_load(f)

BIO = config.get('Customization', {}).get('Bio', True)  # Boolean for Bio
AVATAR = config.get('Customization', {}).get('Avatar', True)  # Boolean for Avatar
PRONOUNS = config.get('Customization', {}).get('Pronouns', True)  # Boolean for Pronouns
THREADS = int(config.get('Threads', 10))  # Default to 10 if not specified

# Token handling
tokens = []
with open('input/tokens.txt') as f:
    for line in f:
        line = line.strip()
        tokens.append(line.split(':')[-1])  # Extract token from email:pass:token or plain token

# Counters for success and failures
success_count = 0
failure_count = 0

# Lock for thread-safe counter updates and file operations
lock = threading.Lock()

# Create the output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

def save_token(filename, token):
    """Save a token to the specified file."""
    with lock:
        with open(f"output/{filename}", "a", encoding="utf-8") as file:
            file.write(token + "\n")

def process_token(token):
    """Process a single token with the configured functions."""
    global success_count, failure_count
    try:
        local_success = True

        # Bio update
        if BIO:
            result = update_bio(token)
            if result:
                uiprint('success', f'Bio Updated , {token[:25]}')
            else:
                local_success = False
                uiprint('failed', f'Bio Update Failed , {token[:25]}')

        # Avatar update
        if AVATAR:
            result = update_avatar(token)
            if result:
                uiprint('success', f'Avatar Changed , {token[:25]}')
            else:
                local_success = False
                uiprint('failed', f'Avatar Update Failed , {token[:25]}')

        # Pronouns update
        if PRONOUNS:
            result = update_pronoun(token)
            if result:
                uiprint('success', f'Pronouns Changed , {token[:25]}')
            else:
                local_success = False
                uiprint('failed', f'Pronouns Update Failed , {token[:25]}')

        # Update global counters and save tokens
        with lock:
            if local_success:
                success_count += 1
                save_token("success.txt", token)
                uiprint("success", f"{token[:25]}: Humanized")
            else:
                failure_count += 1
                save_token("failed.txt", token)
                uiprint("failed", f"{token[:25]}: Tried Humanizing")

    except (requests.exceptions.RequestException, Exception) as e:
        # Catch network-related errors and other exceptions
        with lock:
            failure_count += 1
            save_token("failed.txt", token)
            uiprint("failed", f"{token[:25]}: Error Encountered - {e}")

def main():
    """Main function to process tokens using threading."""
    uiprint("info", "Starting token processing...")

    # Create a thread pool to process tokens concurrently
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(process_token, token): token for token in tokens}

        # Wait for all futures to complete
        for future in as_completed(futures):
            token = futures[future]
            try:
                future.result()  # Ensure we catch exceptions raised in threads
            except Exception as e:
                uiprint("failed", f"Unexpected error with token {token}: {e}")

    # Log summary
    uiprint("info", f"Processing complete: {success_count} tokens succeeded, {failure_count} tokens failed.")
    print(f"Processing complete: {success_count} tokens succeeded, {failure_count} tokens failed.")

if __name__ == "__main__":
    main()
