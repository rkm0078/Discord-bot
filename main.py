from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from response import get_response
from keep_alive import keep_alive

# Step 0: Load our token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Print the token to verify it is loaded (for debugging purposes only, remove in production)
print(f"Token: {TOKEN}")

if TOKEN is None:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Step 2: Message functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Step 3: Handling the startup for our bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is on!')

# Step 4: Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Step 5: Main entry point
def main() -> None:
    client.run(TOKEN)

keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    main()
