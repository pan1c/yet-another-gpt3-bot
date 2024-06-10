import re
from .logging import logging
from .settings import telegram_api_token, help_text, welcome_text, allowed_chat_ids, country_code
from .openai_conversation_handler import generate_response, generate_image
from .csv_writer import write_csv

from telegram import __version__ as TG_VER
from telegram import ForceReply
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import filters
from telegram.ext import MessageHandler
#from telegram.helpers import escape_markdown
#MarkDownV2 is broken, mayebe in future it will be fixed

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

# Define a few command handlers. These usually take the two arguments update and context.
allowed_chat_ids_filter = filters.Chat(allowed_chat_ids) if "any" not in allowed_chat_ids else None


def get_message_from_command(text: str) -> str:
    """Get the message from a command."""
    if " " in text:
        return text.split(" ", 1)[1].strip()
    else:
        return ""

def check_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if chat ID is allowed
    # Convert update.message.chat_id to a string
    chat_id_str = str(update.message.chat_id)
    if "any" not in allowed_chat_ids and chat_id_str not in allowed_chat_ids:
        logging.info(f"Chat ID {chat_id_str} not allowed")
        return False
    logging.info(f"Chat ID {chat_id_str} allowed")
    return True



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""


    await update.message.reply_html(help_text, disable_web_page_preview=True)

async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when a new user joins the chat."""
    users = update.message.new_chat_members if update.message.new_chat_members else [update.effective_user]
    for user in users:
        await update.message.reply_html(
            rf"Hi {user.mention_html()} {welcome_text}", disable_web_page_preview=True
        )

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and generate a response using GPT"""
    # Check if chat ID is allowed
    if not check_group(update, context):
        return

    if update.message.reply_to_message.caption:
        logging.info("Caption detected, skipping message")
        logging.info(update.message.reply_to_message.caption)
        return

    logging.info(update)
    prev_message = update.message.reply_to_message.text if update.message.reply_to_message else ""
    question = update.message.text
    logging.info(f"Question: {question}")
    if prev_message:
        logging.info(f"Previous message: {prev_message}")
        prev_message = f'Previous your message was: {prev_message}'
    response_text = await generate_response(question, prev_message)
    await update.message.reply_html(response_text, disable_web_page_preview=True)


async def image_generation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate image using DALLE."""
    if not check_group(update, context):
        return

    message = get_message_from_command(update.effective_message.text)
    if message == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No message provided. Please specify your message like this: /imagine a cat"
        )
        return
    logging.info(message)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Generating image for your prompt. Please wait..."
    )
    # send prompt to openai image generation and get image url
    image_url, revised_prompt, error_message  = generate_image(message)
    logging.info(image_url)
    logging.info(error_message)
    if image_url is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Error: {error_message}"
        )
    else:
        # sending typing action
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="upload_document"
        )
        # send file to user
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image_url,
            parse_mode="MarkdownV2",
            caption = f"```\n{revised_prompt}\n```\n",
        )


async def postcode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Save user's postcode."""
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    user_firstname = update.effective_user.first_name
    user_lastname = update.effective_user.last_name

    label = ""
    if user_firstname:
        label += user_firstname
    if user_lastname:
        if label: # Add space if first name is not empty
            label += " "
        label += user_lastname

    message = get_message_from_command(update.effective_message.text)
    if message == "":
        responce_text = "No postcode provided. Please specify first part of your UK postcode like this: /postcode SW1"
    else:
        message = re.sub(r'[^A-Z0-9]', '', message.upper().replace(" ", ""))
        if message == "":
            responce_text = "Invalid postcode. Please specify first part of your UK postcode like this: /postcode SW1"
        else:
            logging.info(str(user_id) + " " + country_code + " " + message + " " + label)
            write_csv([{"id": user_id, "country": country_code, "postcode": message, "label": label}])
            responce_text = f"Thank you {user_name} for your UK postcode"

    await update.message.reply_text(responce_text)



def main() -> None:
    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token(telegram_api_token).build()

    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CommandHandler("imagine", image_generation))

    application.add_handler(CommandHandler("welcome", welcome_message))

    application.add_handler(CommandHandler("postcode", postcode))


    # on non command i.e message - run "handle_message"

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    # on new chat members - send welcome message

    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))

    # Run the bot until the user presses Ctrl-C

    application.run_polling()

if __name__ == "__main__":

    main()
