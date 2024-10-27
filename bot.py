import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Replace with your admin user ID
ADMIN_ID = 5436530930  # Change this to your own Telegram user ID

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("You do not have permission to use this bot.")
        return

    update.message.reply_text(
        'Welcome! Please provide the channel owner name, channel link, and your feedback in the following format:\n'
        'Owner: [Owner Name]\n'
        'Link: [Channel Link]\n'
        'Feedback: [Your Feedback]'
    )

# Feedback handler
def handle_feedback(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("You do not have permission to use this bot.")
        return

    feedback_message = update.message.text.split('\n')

    if len(feedback_message) < 3:
        update.message.reply_text('Please provide all details: Owner, Link, and Feedback.')
        return

    try:
        owner_line = feedback_message[0].split(': ', 1)[1]
        link_line = feedback_message[1].split(': ', 1)[1]
        feedback_line = feedback_message[2].split(': ', 1)[1]

        feedback_entry = f"Owner: {owner_line}\nLink: {link_line}\nFeedback: {feedback_line}\n{'-' * 40}\n"

        # Save feedback to a file
        with open('feedback.txt', 'a') as file:
            file.write(feedback_entry)

        update.message.reply_text('Thank you for your feedback!')

    except IndexError:
        update.message.reply_text('Please ensure your message follows the correct format.')

def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your bot token
    updater = Updater("7631125254:AAGx9b1TAeNu3kHMBIaFf3XkcWjYyy8UG5A")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_feedback))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()