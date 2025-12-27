import os
from src.interface.discord.message import bot
import logging

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
token = os.getenv("DISCORD_TOKEN", "")

def main():
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)
    print("Hello from my-asssitant-discord-bot!")


if __name__ == "__main__":
    main()
