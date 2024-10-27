import telebot
from telebot import types

API_TOKEN = '7631125254:AAGx9b1TAeNu3kHMBIaFf3XkcWjYyy8UG5A'
bot = telebot.TeleBot(API_TOKEN)

# Command to start the bot
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the group manager bot! Use /help to see available commands.")

# Command to list group members
@bot.message_handler(commands=['members'])
def list_members(message):
    chat_id = message.chat.id
    members = bot.get_chat_administrators(chat_id)
    member_names = [f"{member.user.first_name} @{member.user.username}" for member in members]
    bot.reply_to(message, "\n".join(member_names))

# Command to ban a user
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.kick_chat_member(message.chat.id, user_id)
        bot.reply_to(message, f"Banned {message.reply_to_message.from_user.first_name}.")
    else:
        bot.reply_to(message, "Please reply to a message of the user you want to ban.")

# Command to unban a user
@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.unban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, f"Unbanned {message.reply_to_message.from_user.first_name}.")
    else:
        bot.reply_to(message, "Please reply to a message of the user you want to unban.")

# Command to delete a message
@bot.message_handler(commands=['delete'])
def delete_message(message):
    if message.reply_to_message:
        bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        bot.reply_to(message, "Message deleted.")
    else:
        bot.reply_to(message, "Please reply to the message you want to delete.")

# Start polling
bot.polling()
