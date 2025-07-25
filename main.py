import os
import re
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
import subprocess

# تنظیمات اولیه
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
OUTPUT_FILE = "ProNet7_Collector.txt"

client = TelegramClient("anon", api_id, api_hash)

# خواندن لیست کانال‌ها از فایل
def load_channels():
    with open("channels.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# استخراج کانفیگ‌ها از متن
def extract_configs(text):
    patterns = [
        r"vmess://[a-zA-Z0-9+/=]+",
        r"vless://[a-zA-Z0-9:/?=_.&%-]+",
        r"trojan://[a-zA-Z0-9:/?=_.&%-]+",
        r"ss://[a-zA-Z0-9:/?=_.&%-]+"
    ]
    configs = []
    for pattern in patterns:
        configs += re.findall(pattern, text)
    return configs

# عملکرد اصلی
async def main():
    await client.start(phone=phone)
    print("✅ Logged in successfully!")

    since = datetime.now() - timedelta(days=2)
    collected = []
    channels = load_channels()

    for channel in channels:
        try:
            entity = await client.get_entity(channel)
            async for msg in client.iter_messages(entity, limit=200):
                if msg.date < since:
                    break
                if msg.message:
                    found = extract_configs(msg.message)
                    collected.extend(found)
        except Exception as e:
            print(f"[!] خطا در {channel}: {e}")

    collected = list(set(collected))  # حذف تکراری‌ها

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in collected:
            f.write(item + "\n")

    print(f"✅ جمع‌آوری کامل شد، {len(collected)} کانفیگ ذخیره شد.")

    git_push()

# پوش خودکار به گیت‌هاب
def git_push():
    subprocess.run(["git", "config", "--global", "user.email", f"{os.getenv('GITHUB_USERNAME')}@users.noreply.github.com"])
    subprocess.run(["git", "config", "--global", "user.name", os.getenv("GITHUB_USERNAME")])
    subprocess.run(["git", "add", OUTPUT_FILE])
    subprocess.run(["git", "commit", "-m", "🔄 Update ProNet7_Collector.txt"])
    subprocess.run(["git", "push", f"https://{os.getenv('GITHUB_USERNAME')}:{os.getenv('PERSONAL_GITHUB_TOKEN')}@github.com/{os.getenv('GITHUB_USERNAME')}/ProNet7.git"])

# اجرای برنامه
asyncio.run(main())
