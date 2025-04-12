from telethon import TelegramClient
import asyncio
import os


# Function to read API credentials from a file
def op():
    with open("./auth.txt") as f:
        api_id = f.readline().strip()
        api_hash = f.readline().strip()
    return api_id, api_hash


# Asynchronous function to send files to a Telegram channel
async def sendTel():
    api_id, api_hash = op()

    # Use a unique session name, like 'my_session'
    async with TelegramClient('my_session', api_id, api_hash) as client:
        # Connect to the client (this is generally optional inside 'async with')
        await client.connect()

        # Replace 'telegram channel link' with the actual username or link to the channel
        channel = await client.get_entity('telegram channel link')

        # Loop through the files in the './vids' directory and send them to the channel
        for video in os.listdir('./vids'):
            await client.send_file(channel, os.path.join('./vids', video))


# Main function to run the async function in an event loop
def sendTelmain():
    try:
        asyncio.run(sendTel())  # Uses asyncio.run() to manage the event loop safely
    except Exception as err:
        print(err)
        exit(1)


# Testing the op() function
if __name__ == '__main__':
    print(op())