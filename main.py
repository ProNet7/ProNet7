import asyncio
import os
from telethon import TelegramClient

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE_NUMBER")

client = TelegramClient("anon", api_id, api_hash)

async def main():
    await client.start(phone=phone)
    print("✅ Logged in successfully.")

asyncio.run(main())
