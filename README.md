# 📸 Screenshot Automation Bot for Telegram

> **Born out of boredom**

---

### Why Did I Write This?

So here's the thing... for a certain TE3000 (or any other courses arjan V might teach), we students are left with no choice but to screenshot *everything*. After a while, my desktop started looking like a digital junkyard, and organizing those screenshots became a nightmare.

Enter **this bot**, my savior and (now yours too). Born from a blend of boredom, frustration, and the desire to not lose my sanity, this bot automates the process of **monitoring screenshots** and sending them directly to a **Telegram channel or chat** for safe-keeping.😊

---

### What Does It Do?

This bot:
- Monitors a folder on your system (e.g., `C:\Temp\Screenshots`) for new files.
- Validates the files (ensures they’re actual images and not broken).
- Uploads the screenshots directly to a specified Telegram channel or chat.
- Allows you to control the bot via simple Telegram commands (`/start`, `/stop`, `/exit`).

Now you can focus on learning (or pretending to), while this bot ensures your screenshots are always backed up and easily accessible.

---

### How to Use It?

Here’s the **step-by-step guide** to get this bot up and running on your machine:

#### 1️⃣ Prerequisites

- **Python** (version 3.10 or higher). Download it from [python.org](https://www.python.org/downloads/).
- A **Telegram bot** token:
  - Talk to [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
  - Create a new bot and grab the API token.
- A **Telegram channel or chat** where you want the bot to send your files. Add the bot as an admin to this chat or channel.

---

#### 2️⃣ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/telegram-screenshot-bot.git
   cd telegram-screenshot-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the script:
   - Open the `AutoFileBot.py` file.
   - Replace the placeholder `BOT_TOKEN` with your bot's token.
   - Replace `CHANNEL_USERNAME` with your Telegram channel or chat ID.

---

#### 3️⃣ Usage

Run the bot:
```bash
python AutoFileBot.py
```

Then, interact with the bot on Telegram:
- `/start`: Starts monitoring the folder.
- `/stop`: Stops monitoring the folder.
- `/exit`: Shuts down the bot.

Take a screenshot (e.g., `Win + PrtScn`), and watch as the bot uploads it to your Telegram chat!

---

### Folder Monitoring

By default, the bot monitors the folder:
```
C:\Temp\Screenshots
```
Make sure this folder exists. If not, the bot will create it for you.

If you want to change the folder, update the `folder_to_monitor` variable in the script:
```python
folder_to_monitor = r"Your\Custom\Path"
```

---

### Example Workflow

1. You take a screenshot.
2. The file appears in `C:\Temp\Screenshots`.
3. The bot picks it up, validates it, and uploads it to Telegram.
4. Done. Your screenshot is safely stored in the chat.

---

### Features (Why You’ll Love This Bot)

- 🛠 **Hands-Free Management**: Automatically uploads screenshots as you take them.
- 📤 **Telegram Integration**: Store and organize your files in a Telegram chat or channel.
- ✅ **File Validation**: Ensures only valid images are processed.
- 🤖 **Command Control**: Start, stop, and shut down the bot using Telegram commands.
- 💤 **Boredom Slayer**: Because we all need projects that make life a little easier (and a lot more fun).

---

### Fun Fact

This bot was built in moments of procrastination. It might not solve world hunger, but it does help organize your screenshots. 🎉

---

### Contribution

Want to improve this bot or add features? Fork this repo, make your changes, and submit a pull request! Let’s make this bot even more awesome together. 💻

---

### Future Plans

I might try adding Task Scheduler integration to allow the bot to run in the background automatically after system startup. Stay tuned for updates! 😊

---

### Need Help?

If you have any questions or suggestions, feel free to reach out to me on GitHub.

---
### License

This project is open-source under the **MIT License**. Go ahead, tweak it, break it, and have fun with it. 😊

---

