## System Monitoring Bot

This project allows you to check basic system properties such as:

1. Free Memory
2. Disk Space
3. Uptime
4. List files in a directory
5. CPU Usage

---

## Approach

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. **Ensure Ollama is running**

```bash
ollama list
```

3. **Install Python (if not installed)**

4. **Install required dependencies**

```bash
pip install python-telegram-bot requests
```

5. **Set your Telegram Bot Token**

```bash
export BOT_TOKEN=your_token
```

6. **Run the bot**

```bash
python bot.py
```
