import os
import requests
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔐 Better: use environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")  # export BOT_TOKEN=your_token

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama2"

# Call Ollama
def call_ollama(prompt):
    res = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    return res.json().get("response", "Error")

# Handle messages
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    # 📊 Disk usage
    if "disk" in user_text:
        result = subprocess.getoutput("df -h")
        reply = f"Disk Usage:\n{result}"

    # 🧠 Memory usage
    elif "memory" in user_text or "ram" in user_text:
        result = subprocess.getoutput("free -h")
        reply = f"Memory Usage:\n{result}"

    # ⚡ CPU usage
    elif "cpu" in user_text:
        result = subprocess.getoutput("top -bn1 | head -5")
        reply = f"CPU Usage:\n{result}"

    # ⏱️ Uptime
    elif "uptime" in user_text:
        result = subprocess.getoutput("uptime")
        reply = f"System Uptime:\n{result}"

    # 📁 Files
    elif "files" in user_text or "ls" in user_text:
        result = subprocess.getoutput("ls -lh")
        reply = f"Files:\n{result}"

    # 🤖 Default → LLM
    else:
        reply = call_ollama(user_text)

    await update.message.reply_text(reply)

# Start bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot is running...")
app.run_polling()
