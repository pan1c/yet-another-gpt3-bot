import os
from .logging import logging

openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_api_token = os.getenv("TELEGRAM_BOT_TOKEN")
gpt_system_role = os.getenv("GPT_SYSTEM_ROLE", "You are a helpful assistant.")
gpt_model_name = os.getenv("GPT_MODEL_NAME", "gpt-3.5-turbo")
log_level = os.getenv("LOG_LEVEL", "INFO")

logging.debug(f"openai_api_key: {openai_api_key}, telegram_api_token: {telegram_api_token}, gpt_system_role: {gpt_system_role}, gpt_model_name: {gpt_model_name}, log_level: {log_level}")
logging.info(f"gpt_system_role: {gpt_system_role}, gpt_model_name: {gpt_model_name}, log_level: {log_level}")

