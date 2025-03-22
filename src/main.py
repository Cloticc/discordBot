"""
Discord Bot for Role Management
Main entry point for the bot
"""
import os
import sys
import discord
from discord.ext import commands
import config.config as config
from handlers.role_handler import RoleHandler
import logging
import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')
    ]
)

class RoleManagementBot(commands.Bot):
    """
    Main bot class that handles initialization and event processing
    """
    def __init__(self):
        # Set up required intents
        try:
            intents = discord.Intents.default()
            intents.message_content = True  # Privileged intent
            intents.members = True          # Privileged intent
            intents.reactions = True

            super().__init__(
                command_prefix=commands.when_mentioned_or(config.PREFIX),
                intents=intents,
                help_command=None
            )

            self.role_handler = RoleHandler(self)
            self.last_reconnect_time = None
            self.reconnect_attempts = 0

        except Exception as e:
            logging.error("Error initializing bot: %s", str(e))
            raise

    async def setup_hook(self):
        """
        Loads all commands when the bot starts
        """
        try:
            # Load all command modules
            for filename in os.listdir('./src/commands'):
                if filename.endswith('.py'):
                    await self.load_extension(f'commands.{filename[:-3]}')
                    logging.info('Loaded command module: %s', filename[:-3])
        except Exception as e:
            logging.error("Error loading extensions: %s", str(e))
            raise

    async def on_ready(self):
        """
        Called when the bot is ready and connected to Discord
        """
        self.last_reconnect_time = datetime.datetime.now()
        self.reconnect_attempts = 0
        logging.info(f'{self.user} has connected to Discord!')
        logging.info(f'Bot is active in {len(self.guilds)} servers.')

        # Set bot status
        try:
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="for role reactions"
                )
            )

            # Auto-scan for role messages
            logging.info("Scanning for existing role messages...")
            results = await self.role_handler.auto_scan_all_guilds()

            total_reconnected = sum(results.values())
            if (total_reconnected > 0):
                logging.info(f"✅ Successfully reconnected {total_reconnected} role messages across {len(results)} servers!")
            else:
                logging.info("No existing role messages found to reconnect.")

        except Exception as e:
            logging.error(f"Error during startup: {e}")

    async def on_connect(self):
        """Called when the bot connects to Discord"""
        logging.info("Bot connected to Discord!")

    async def on_disconnect(self):
        """Called when the bot disconnects from Discord"""
        logging.warning("Bot disconnected from Discord. Will attempt to reconnect...")
        self.reconnect_attempts += 1

    async def on_resumed(self):
        """Called when the bot resumes a session"""
        logging.info("Session resumed successfully")

def check_token():
    """
    Validates that the bot token is set
    """
    if not config.TOKEN:
        print("Error: Bot token not found!")
        print("Please make sure to:")
        print("1. Create a .env file in the root directory")
        print("2. Add your bot token as DISCORD_TOKEN=your_token_here")
        sys.exit(1)

def check_intents():
    """
    Prints instructions for enabling privileged intents
    """
    print("\nIMPORTANT: This bot requires privileged intents!")
    print("Please enable the following in the Discord Developer Portal:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Select your application")
    print("3. Go to the 'Bot' section")
    print("4. Enable the following Privileged Gateway Intents:")
    print("   - SERVER MEMBERS INTENT")
    print("   - MESSAGE CONTENT INTENT")
    print("\nAfter enabling the intents, restart the bot.")

if __name__ == "__main__":
    try:
        # Check if token is configured
        check_token()

        # Create bot instance
        bot = RoleManagementBot()

        # Start the bot
        bot.run(config.TOKEN)
    except discord.errors.PrivilegedIntentsRequired:
        print("\nError: Privileged Intents are not enabled!")
        check_intents()
        sys.exit(1)
    except Exception as e:
        print(f"Error starting bot: {e}")
        sys.exit(1)
