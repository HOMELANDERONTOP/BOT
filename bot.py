import requests
from telegram import Bot
from telegram.error import TelegramError

# Replace these with your values
TELEGRAM_BOT_TOKEN = "7631125254:AAGx9b1TAeNu3kHMBIaFf3XkcWjYyy8UG5A"
CHAT_ID = "-1001957862866"  # Use the negative chat ID for groups (e.g., -123456789)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def download_file(url, file_path):
    """Downloads a file from a given URL to a specified local file path."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")
        return None
    return file_path

def upload_file_to_telegram(file_path):
    """Uploads a local file to the specified Telegram group."""
    try:
        with open(file_path, "rb") as file:
            bot.send_document(chat_id=CHAT_ID, document=file)
        print(f"Uploaded: {file_path}")
    except TelegramError as e:
        print(f"Failed to upload {file_path}. Error: {e}")

def main(urls):
    """Main function to download files from a list of URLs and upload them to Telegram."""
    for url in urls:
        filename = url.split("/")[-1]  # Get the filename from the URL
        file_path = download_file(url, filename)
        if file_path:
            upload_file_to_telegram(file_path)

if __name__ == "__main__":
    # List of URLs to download and upload
    urls = [
        "https://example.com/file1.pdf",
        "https://example.com/file2.jpg"
    ]
    main(urls)