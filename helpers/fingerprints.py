import json
import random
import yaml
from tls_client import Session

# Load configuration from config.yaml
with open("config.yaml", "r") as c:
    config = yaml.safe_load(c)
proxyless = config.get("proxyless", True)

# Load JA3 configurations from the JSON file
with open("helpers/ja3.json", "r") as f:
    ja_3s = json.load(f)

# Load proxies from the file
with open("input/proxies.txt", "r") as p:
    proxies = [proxy.strip() for proxy in p.readlines()]

def get_ja3_session():
    """
    Initializes a TLS session with JA3 configuration and proxy settings.
    Returns the session, x_super_properties, and user-agent.
    """
    # Select a random JA3 configuration
    ja_prop = random.choice(ja_3s)
    chrome_version = str(random.randint(118, 126))
    
    # Initialize TLS session
    session = Session(
        ja3_string=ja_prop["ja3"],
        client_identifier=f"chrome_{chrome_version}",
        random_tls_extension_order=True,
    )
    
    if not proxyless and proxies:
        proxy = random.choice(proxies)  
        session.proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}",
        }
    else:
        session.proxies = None

    x_super_properties = ja_prop.get("x-super-properties")
    user_agent = ja_prop.get("user-agent")

    return session, x_super_properties, user_agent

def obtain_cookies(session: Session) -> dict:
    """
    Obtains cookies from a session's response.
    """
    cookies = {}
    try:
        response = session.get("https://discord.com")
        for cookie in response.cookies:
            if cookie.name.startswith("__") and cookie.name.endswith("uid"):
                cookies[cookie.name] = cookie.value
        return cookies
    except Exception as e:
        print(f"Error obtaining cookies: {e}")
        return {}

def get_headers(token: str, x_super_properties: str, user_agent: str) -> dict:
    """
    Returns the headers needed for a Discord API request.
    """
    headers = {
        "authority": "discord.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "content-type": "application/json",
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": user_agent,
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "Europe/Budapest",
        "x-super-properties": x_super_properties,
    }
    return headers