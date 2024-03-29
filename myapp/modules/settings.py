import os
from .logging import logging

openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_api_token = os.getenv("TELEGRAM_BOT_TOKEN")
gpt_system_role = os.getenv("GPT_SYSTEM_ROLE", "You are a helpful assistant.")
gpt_model_name = os.getenv("GPT_MODEL_NAME", "gpt-3.5-turbo-1106")
log_level = os.getenv("LOG_LEVEL", "INFO")
allowed_chat_ids = os.getenv("ALLOWED_CHAT_IDS", "any").split(",")
locations_file_name = os.getenv("LOCATIONS_FILE_NAME", "/tmp/data/locations.csv")
country_code = os.getenv("COUNTRY_CODE", "GB")

try:
    # Open the help text file and read its contents
    with open('data/help.txt', 'r') as f:
        help_text = f.read()
except FileNotFoundError:
    # If the file does not exist, set a default help text
    help_text = "Sorry, the help file is not available at the moment."

try:
    with open('data/welcome.txt', 'r') as f:
        welcome_text = f.read()
except FileNotFoundError:
    welcome_text = "Welcome to the chat!"


logging.debug(f"openai_api_key: {openai_api_key}, telegram_api_token: {telegram_api_token}, gpt_system_role: {gpt_system_role}, gpt_model_name: {gpt_model_name}, log_level: {log_level}, allowed_chat_ids: {allowed_chat_ids}")
logging.info(f"gpt_system_role: {gpt_system_role}, gpt_model_name: {gpt_model_name}, log_level: {log_level}, allowed_chat_ids: {allowed_chat_ids}")

