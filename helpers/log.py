from colorama import Fore, Style, init
from datetime import datetime
import pytz
import yaml
import os
import sys
from discord.ext import commands, tasks

init(autoreset=True)

failed = Fore.RED
success = Fore.GREEN
warn = Fore.YELLOW
mcolor = Fore.MAGENTA
info = Fore.CYAN
light_pink = Fore.LIGHTMAGENTA_EX
medium_pink = Fore.MAGENTA
white = Fore.WHITE

# Load the configuration
with open("config.yaml") as f:
    config = yaml.safe_load(f)

def get_timestamp():
    """Returns the current timestamp in a readable format."""
    tz = pytz.timezone("Asia/Kolkata")  # Adjust time zone as per your needs
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def uiprint(state, message):
    timestamp = get_timestamp()
    if state == "success":
        print(f"{success}[SUCCESS] {mcolor}{message}")
    elif state == "failed":
        print(f"{failed}[FAILED] {mcolor}{message}")
    elif state == "warn":
        print(f"{warn}[WARNING] {mcolor}{message}")
    elif state == "info":
        print(f"{info}[INFO] {mcolor}{message}")
    else:
        print(f"{white}[UNKNOWN] {mcolor}{message}")


