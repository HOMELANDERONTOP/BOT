from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_API_TOKEN' with your actual Telegram Bot API token
API_TOKEN = '7395213244:AAFvcf16F84HAHi8O97DTGZrdZU8VhSwA3Q'

# Channel links
CHANNEL_LINKS = [
    "https://t.me/your_channel_1",  # Replace with your first channel link
    "https://t.me/your_channel_2",  # Replace with your second channel link
    "https://t.me/your_channel_3",  # Replace with your third channel link
    "https://t.me/your_channel_4",  # Replace with your fourth channel link
    "https://t.me/your_channel_5",  # Replace with your fifth channel link
]

# Flower emojis to decorate the channel links
FLOWER_EMOJIS = "🌸🌺🌼🌻💐"

# Function to greet the user and send the decorated channel links
def greet_user(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()  # Convert the message to lowercase for easy comparison
    if "bot welcome" in user_message:
        user_name = update.message.from_user.first_name
        greeting = f"Hello {user_name}, welcome to the bot! Here are the links to our amazing channels, decorated with flowers! {FLOWER_EMOJIS}\n"

        # Adding the channel links with flowers
        for idx, link in enumerate(CHANNEL_LINKS, 1):
            greeting += f"{FLOWER_EMOJIS} Channel {idx}: {link}\n"
        
        update.message.reply_text(greeting)

# Start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Type 'bot welcome' to receive a greeting and links to our channels.")

# Main function to set up the bot
def main():
    # Create the Updater object and pass it your bot's API token
    updater = Updater(API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command handler for the start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Message handler for any message
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, greet_user))

    # Start polling to receive updates
    updater.start_polling()

    # Run the bot until you send a stop signal
    updater.idle()

if __name__ == '__main__':
    main()()    