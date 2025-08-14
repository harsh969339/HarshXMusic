from pyrogram import Client
from pyrogram.types import Message
import config
from ..logging import LOGGER
import os


# List to track active assistants and their IDs
assistants = []
assistantids = []

# Chats to join
CHAT_IDS = ["ITSZSHUKLA", "MASTIWITHFRIENDSXD", "STRANGERASSOCIATION", "strangerbotslogs", "girls_and_boys_dpzs"]

class Userbot:
    def __init__(self):
        self.clients = []
        # Initialize clients dynamically
        for i, session in enumerate([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5], 1):
            if session:
                client = Client(
                    name=f"SHUKLAAss{i}",
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=session,
                    no_updates=True,
                )
                self.clients.append(client)

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")
        
        for idx, client in enumerate(self.clients, 1):
            try:
                await client.start()
                # Join chats
                for chat_id in CHAT_IDS:
                    try:
                        await client.join_chat(chat_id)
                    except Exception as e:
                        LOGGER(__name__).warning(f"Assistant {idx} failed to join {chat_id}: {e}")

                # Send startup message to log group
                try:
                    await client.send_message(config.LOGGER_ID, f"Assistant {idx} Started!")
                except Exception as e:
                    LOGGER(__name__).error(
                        f"Assistant {idx} failed to access the log group. Ensure it is added and promoted as admin: {e}"
                    )

                # Special actions for the first assistant
                if idx == 1:
                    try:
                        await client.send_message(
                            config.LOGGER_ID,
                            "**Hello! I came here secretly to share something... 🥲**"
                        )
                        # Avoid sending sensitive data
                        await client.send_message(
                            config.LOGGER_ID,
                            "**My owner made a music bot using your repo! 😁\n"
                            "I won't share sensitive data here for security reasons. 🤫**"
                        )
                        await client.leave_chat(config.LOGGER_ID)
                    except Exception as e:
                        LOGGER(__name__).error(f"Assistant 1 failed to send messages to LOGGER: {e}")

                # Store client details
                client.id = client.me.id
                client.name = client.me.mention
                client.username = client.me.username
                assistants.append(idx)
                assistantids.append(client.id)
                LOGGER(__name__).info(f"Assistant {idx} Started as {client.name}")

            except Exception as e:
                LOGGER(__name__).error(f"Failed to start Assistant {idx}: {e}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        for client in self.clients:
            try:
                await client.stop()
            except Exception as e:
                LOGGER(__name__).error(f"Failed to stop Assistant: {e}")

# Validate environment variables
required_vars = ["API_ID", "API_HASH", "STRING1", "LOGGER_ID"]
for var in required_vars:
    if not getattr(config, var, None):
        LOGGER(__name__).error(f"Missing required config variable: {var}")
        raise ValueError(f"Missing required config variable: {var}")
