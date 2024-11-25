import logging
from rembg import remove
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import io

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Developer info
DEVELOPER_NAME = "Frx Shooter"
DEVELOPER_CONTACT = "@Frx_Shooter"
BOT_NAME = "Background Removal Bot"
BOT_DESCRIPTION = "This bot removes the background from images."

# Command handlers
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f"Hello! I am {BOT_NAME}.\n\n"
        f"{BOT_DESCRIPTION}\n\n"
        f"Send me a photo and I'll remove the background for you!\n\n"
        f"Developer Info:\n"
        f"Name: {DEVELOPER_NAME}\n"
        f"Contact: {DEVELOPER_CONTACT}"
    )

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f"To use this bot, simply send an image, and I will remove the background for you."
    )

def remove_background(update: Update, context: CallbackContext) -> None:
    # Ensure the user sent an image
    if update.message.photo:
        # Get the highest quality image
        file = update.message.photo[-1].get_file()
        image_file = file.download_as_bytearray()

        # Remove background using rembg
        output = remove(image_file)

        # Send the result back to the user
        bio = io.BytesIO(output)
        bio.name = 'output.png'
        bio.seek(0)
        update.message.reply_photo(photo=bio)
    else:
        update.message.reply_text("Please send an image to remove the background.")

def main():
    # Telegram Bot Token
    TELEGRAM_TOKEN = '7784549884:AAGzkZ-E1Hlr3aR-FtX5zEIkrtlna3AdHT0'

    # Create Updater and Dispatcher
    updater = Updater(TELEGRAM_TOKEN)

    # Add handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(Filters.photo, remove_background))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()