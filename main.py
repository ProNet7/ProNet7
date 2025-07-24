import os
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# کانال‌های تلگرام که کانفیگ‌ها رو می‌خوانیم
CHANNELS = [
    'ConfigsHubPlus',
    'meli_proxyy',
    'Farah_VPN',
    'freakconfig',
    'prrofile_purple',
    'DailyV2RY'
]

# نام فایل خروجی
OUTPUT_FILE = 'ProNet7_Collector.txt'

# مدت زمانی که پیام‌ها بررسی می‌شن (۲ روز گذشته)
DAYS_BACK = 2

async def main():
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')
    phone = os.getenv('PHONE')

    client = TelegramClient('session', api_id, api_hash)

    await client.start(phone)

    # اگر نیاز به رمز دو مرحله‌ای بود
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input('Enter the code you received on Telegram: ')
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input('Two step verification enabled. Please enter your password: ')
            await client.sign_in(password=password)

    cutoff_date = datetime.utcnow() - timedelta(days=DAYS_BACK)

    collected_configs = []

    for channel in CHANNELS:
        print(f'Fetching messages from {channel}...')
        try:
            async for message in client.iter_messages(channel, reverse=True):
                if message.date < cutoff_date:
                    break
                if message.message and ('v2ray' in message.message.lower() or 'vmess' in message.message.lower()):
                    collected_configs.append(message.message)
        except Exception as e:
            print(f'Error fetching from {channel}: {e}')

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(collected_configs))

    print(f'Done! Collected {len(collected_configs)} configs.')

if __name__ == '__main__':
    asyncio.run(main())
