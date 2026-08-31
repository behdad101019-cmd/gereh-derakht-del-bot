import os, json
from datetime import datetime, time
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Application, ContextTypes

from posts import POSTS

load_dotenv()
TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL_ID"]  # example: @gerehderakhtedel
TZ = ZoneInfo("Asia/Tehran")
STATE_FILE = "state.json"

TIMES = [time(9, 0, tzinfo=TZ), time(18, 0, tzinfo=TZ), time(23, 0, tzinfo=TZ)]

def get_index():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("index", 0)
    except FileNotFoundError:
        return 0

def set_index(i):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"index": i}, f)

async def publish(context: ContextTypes.DEFAULT_TYPE):
    i = get_index()
    if i >= len(POSTS):
        i = 0
    await context.bot.send_message(chat_id=CHANNEL, text=POSTS[i])
    set_index(i + 1)

def main():
    app = Application.builder().token(TOKEN).build()
    for t in TIMES:
        app.job_queue.run_daily(publish, time=t, name=f"post_{t.hour}_{t.minute}")
    app.run_polling()

if __name__ == "__main__":
    main()
