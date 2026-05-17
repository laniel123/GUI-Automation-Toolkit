try:
    from telethon import TelegramClient
except ImportError:
    TelegramClient = None
import asyncio
import os


def op():
    with open("./auth.txt") as f:
        api_id = f.readline().strip()
        api_hash = f.readline().strip()
    return api_id, api_hash


async def sendTel():
    if TelegramClient is None:
        raise ImportError("telethon library is required for Telegram sending.")
    api_id, api_hash = op()
    async with TelegramClient('my_session', api_id, api_hash) as client:
        await client.connect()
        channel = await client.get_entity('telegram channel link')
        for video in os.listdir('./vids'):
            await client.send_file(channel, os.path.join('./vids', video))


def sendTelmain():
    try:
        api_id, api_hash = op()
        if not api_id or not api_hash:
            print("Telegram not configured — skipping.")
            return
        asyncio.run(sendTel())
    except Exception as err:
        print(f"Telegram skipped: {err}")


if __name__ == '__main__':
    print(op())