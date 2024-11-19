import os
import time
from threading import Thread, Event, Lock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import shutil
from PIL import Image

# Telegram Bot Token and Channel Username
BOT_TOKEN = '7770281904:AAHAVAMNpoFOt4__rFzCTauAVrLchSW10RY'
CHANNEL_USERNAME = '@princomTE3000'

# Thread safety variables
lock = Lock()
is_running = False
last_processed_file = None

# Graceful shutdown event
stop_event = Event()

# Function to check if a file is ready
def wait_for_file_existence(file_path, retries=5, delay=1):
    """Wait for a file to appear and be ready."""
    for attempt in range(retries):
        if os.path.exists(file_path) and os.access(file_path, os.R_OK):
            print(f"File {file_path} is ready.")
            return True
        print(f"File {file_path} not ready. Retrying in {delay} seconds...")
        time.sleep(delay)
    print(f"File {file_path} still not ready after {retries} retries.")
    return False

# Validate image file
def validate_image(file_path):
    """Validate the image file."""
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify the image is valid
        return True
    except Exception as e:
        print(f"File {file_path} is not a valid image. Error: {e}")
        return False

# Copy to temporary folder
def copy_to_temp(file_path):
    """Copy the file to a temporary location."""
    temp_path = os.path.join(os.path.dirname(file_path), "temp_" + os.path.basename(file_path))
    try:
        shutil.copy(file_path, temp_path)
        return temp_path
    except Exception as e:
        print(f"Failed to copy file {file_path}. Error: {e}")
        return None

# Function to send a file to Telegram
def send_to_telegram(file_path):
    if not wait_for_file_existence(file_path):
        print(f"File {file_path} does not exist. Skipping.")
        return

    if not validate_image(file_path):
        print(f"File {file_path} is invalid. Skipping.")
        return

    temp_file = copy_to_temp(file_path)
    if not temp_file:
        print(f"Failed to copy file for sending. Skipping {file_path}.")
        return

    try:
        with open(temp_file, 'rb') as file:
            if temp_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                files = {'photo': file}
            else:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                files = {'document': file}

            data = {'chat_id': CHANNEL_USERNAME}
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            print(f"File {file_path} sent successfully!")
    except Exception as e:
        print(f"Failed to send file {file_path}. Error: {e}")
    finally:
        os.remove(temp_file)  # Clean up the temporary file

# File System Watcher Class
class Watcher:
    def __init__(self, folder_to_watch):
        self.folder_to_watch = folder_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.folder_to_watch, recursive=False)
        self.observer.start()
        try:
            stop_event.wait()  # Wait until `stop_event` is set
        finally:
            self.observer.stop()
            self.observer.join()

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        self.process_file(event)

    def on_modified(self, event):
        self.process_file(event)

    def process_file(self, event):
        global is_running, last_processed_file

        if not event.is_directory:  # Only handle files
            file_path = event.src_path
            if "temp_" in os.path.basename(file_path):  # Ignore temporary files
                print(f"Ignoring temporary file: {file_path}")
                return

            print(f"File detected or modified: {file_path}")

            time.sleep(1)  # Wait to ensure the file is fully created

            with lock:
                if is_running and file_path != last_processed_file:
                    send_to_telegram(file_path)
                    last_processed_file = file_path
                elif not is_running:
                    print("Bot is stopped. File will not be sent.")

# Telegram bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_running
    with lock:
        if is_running:
            await update.message.reply_text("The bot is already running.")
        else:
            is_running = True
            await update.message.reply_text("Bot started. Monitoring files.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_running
    with lock:
        if not is_running:
            await update.message.reply_text("The bot is already stopped.")
        else:
            is_running = False
            await update.message.reply_text("Bot stopped. Monitoring paused.")

async def exit_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_event.set()  # Signal to stop the folder watcher thread
    await update.message.reply_text("Exiting the bot. Bye!")
    application.stop()

# Main execution
if __name__ == "__main__":
    # Folder to monitor
    folder_to_monitor = r"C:\Temp\Screenshots"
    if not os.path.exists(folder_to_monitor):
        os.makedirs(folder_to_monitor)
        print(f"Created folder: {folder_to_monitor}")

    print(f"Monitoring folder: {folder_to_monitor}")
    w = Watcher(folder_to_monitor)

    # Run the folder watcher in a separate thread
    Thread(target=w.run, daemon=True).start()

    # Set up Telegram bot
    application = Application.builder().token(BOT_TOKEN).build()

    # Register bot commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("exit", exit_bot))

    print("Bot is running... Use /start, /stop, or /exit to control it.")
    application.run_polling()
