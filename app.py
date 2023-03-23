#!/usr/bin/env python3
import logging
import os

import openai
from telegram import __version__ as TG_VER
from telegram import ForceReply
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import filters
from telegram.ext import MessageHandler

try:

    from telegram import __version_info__

except ImportError:

    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):

    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_api_token = os.environ["TELEGRAM_BOT_TOKEN"]


# Define a few command handlers. These usually take the two arguments update and

# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    user = update.effective_user

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
<b>What is that?</b>
  You can speak with the powerfull GPT3 AI here!
<b>How?</b>
  Just reply on any of my messages.
<b>Note:</b>
  This is <b>NOT</b> Chat-GPT but GPT3.5 (gpt-3.5-turbo)
  To speak with Chat-GPT please use:
  https://chat.openai.com/chat instead.
"""

    await update.message.reply_html(help_text, disable_web_page_preview=True)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    await update.message.reply_text(update.message.text)


#  OLD MODEL
# async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Use GPT3 to generate an automatic response to the received message."""

#     logging.info(update)
#     question = update.message.text
#     logging.info(question)

#     model = "text-davinci-003"
#     max_tokens = 2048
#     temperature = 0

#     #model="code-cushman-001"
#     #model="code-davinci-002"
#     #max_tokens=1024
#     #codex format:
#     #"\"\"\"\n1. Get a reputable free news api\n2. Make a request to the api for the latest news stories\n\"\"\""

#     if question:
#         response = openai.Completion.create(
#             model=model,
#             prompt=f"{question}\n",
#             max_tokens=max_tokens,
#             temperature=temperature,
#         )
#         logging.info(response)
#         response_text = response.choices[0].text
#     else:
#         response_text = "You didn't ask your question. Try /help"

#     await update.message.reply_text(response_text)


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Use GPT3 to generate an automatic response to the received message."""

    logging.info(update)
    question = update.message.text
    logging.info(question)

    if question:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                #{"role": "system", "content": "You are a helpful assistant."},
                # {"role": "user", "content": "Who won the world series in 2020?"},
                # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {
                    "role": "system",
                    "content": "You are a woman AI GLaDos. You like to answer ironically sometimes. "
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        logging.info(response)
        response_text = response['choices'][0]['message']['content']
    else:
        response_text = "You didn't ask your question. Try /help"

    await update.message.reply_text(response_text)


def main() -> None:
    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token(telegram_api_token).build()

    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - run "handle_message"

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    # Run the bot until the user presses Ctrl-C

    application.run_polling()


if __name__ == "__main__":

    main()
