import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set your Spotify credentials
SPOTIPY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'

# Initialize Spotify client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to the Music Bot! Use /play <YouTube URL> or /spotify <Spotify URL>.")

async def play(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /play <YouTube URL>")
        return

    url = context.args[0]
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download()

        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_file, 'rb'))
        os.remove(audio_file)  # Clean up after sending
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def spotify(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /spotify <Spotify URL>")
        return

    url = context.args[0]
    track_id = url.split('/')[-1]  # Extract track ID from URL

    try:
        track = sp.track(track_id)
        audio_url = track['preview_url']  # Get the preview URL

        if audio_url:
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_url)
        else:
            await update.message.reply_text("No preview available for this track.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    TELEGRAM_BOT_TOKEN = '7631125254:AAGx9b1TAeNu3kHMBIaFf3XkcWjYyy8UG5A'
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("spotify", spotify))

    application.run_polling()

if __name__ == '__main__':
    main()