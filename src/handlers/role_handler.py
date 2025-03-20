"""
Role handler module for managing role creation and role assignment via reactions
"""
import discord
from discord.ext import commands
from config.config import ROLE_CATEGORIES, ROLE_COLORS, CLASS_COLORS

class RoleHandler:
    """
    Handler class for role-related operations
    """
    def __init__(self, bot):
        self.bot = bot
        self.role_messages = {}  # Tracks message IDs for reaction role messages

    async def create_roles(self, guild):
        """
        Creates all roles defined in the config if they don't already exist

        Args:
            guild (discord.Guild): The guild to create roles in

        Returns:
            dict: Categories mapped to lists of created role objects
        """
        created_roles = {}

        for category, data in ROLE_CATEGORIES.items():
            category_roles = []
            category_color = ROLE_COLORS.get(category, 0x808080)  # Default to gray if no color set

            for emoji, role_name in data["roles"].items():
                # Check if role already exists
                existing_role = discord.utils.get(guild.roles, name=role_name)

                if existing_role:
                    category_roles.append(existing_role)
                else:
                    # Determine role color
                    if category == "classes" and role_name in CLASS_COLORS:
                        role_color = CLASS_COLORS[role_name]
                    else:
                        role_color = category_color

                    # Create new role
                    new_role = await guild.create_role(
                        name=role_name,
                        color=discord.Color(role_color),
                        mentionable=True
                    )
                    category_roles.append(new_role)

            created_roles[category] = category_roles

        return created_roles

    async def send_reaction_message(self, channel, category, roles):
        """
        Sends a message with reactions for role selection

        Args:
            channel (discord.TextChannel): Channel to send the message to
            category (str): Category name from the config
            roles (list): List of role objects

        Returns:
            discord.Message: The sent message
        """
        category_data = ROLE_CATEGORIES.get(category)

        if not category_data:
            return None

        # Create embed for roles
        embed = discord.Embed(
            title=category_data["title"],
            description="React to get your roles!",
            color=discord.Color(ROLE_COLORS.get(category, 0x808080))
        )

        # Add roles to embed description
        role_descriptions = []
        for emoji, role_name in category_data["roles"].items():
            # Simply display emoji and role name without color codes
            role_descriptions.append(f"{emoji} - {role_name}")

        embed.description = "\n".join(role_descriptions)

        # Send message with embed
        message = await channel.send(embed=embed)

        # Add reactions to message
        for emoji in category_data["roles"].keys():
            await message.add_reaction(emoji)

        # Store message ID for reaction handling
        self.role_messages[message.id] = {
            "category": category,
            "roles": {emoji: role_name for emoji, role_name in category_data["roles"].items()}
        }

        return message

    async def handle_reaction(self, payload, add=True):
        """
        Handles reaction addition/removal and updates user roles

        Args:
            payload (discord.RawReactionActionEvent): Reaction event payload
            add (bool): Whether to add or remove the role
        """
        # Check if the reaction is on one of our role messages
        if payload.message_id not in self.role_messages:
            return

        # Get message data
        message_data = self.role_messages[payload.message_id]
        emoji = str(payload.emoji)

        # Check if the emoji is valid for this message
        if emoji not in message_data["roles"]:
            return

        # Get the role name and find the corresponding role object
        role_name = message_data["roles"][emoji]
        guild = self.bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=role_name)

        if not guild or not role:
            return

        # Get the member
        member = guild.get_member(payload.user_id)

        # Skip if the reactor is the bot
        if member.id == self.bot.user.id:
            return

        # Add or remove role
        try:
            if add:
                await member.add_roles(role)
            else:
                await member.remove_roles(role)
        except discord.HTTPException:
            # Handle permission errors
            pass

    async def scan_channel_roles(self, channel: discord.TextChannel) -> int:
        """
        Scans a channel for role messages and reconnects them
        
        Args:
            channel: The channel to scan
            
        Returns:
            Number of messages reconnected
        """
        reconnected = 0
        
        try:
            # Get bot's messages in the channel
            async for message in channel.history(limit=100):
                if message.author == self.bot.user and message.embeds:
                    embed = message.embeds[0]
                    if not embed.title:
                        continue
                    
                    # Find matching category by title
                    matching_category = None
                    for category, data in ROLE_CATEGORIES.items():
                        if data["title"] == embed.title:
                            matching_category = category
                            break
                    
                    if matching_category:
                        # Register message for reaction handling
                        self.role_messages[message.id] = {
                            "category": matching_category,
                            "roles": ROLE_CATEGORIES[matching_category]["roles"]
                        }
                        reconnected += 1
                        
                        # Verify/add reactions
                        existing_reactions = {str(reaction.emoji) for reaction in message.reactions}
                        needed_reactions = set(ROLE_CATEGORIES[matching_category]["roles"].keys())
                        
                        # Add missing reactions
                        for emoji in needed_reactions - existing_reactions:
                            await message.add_reaction(emoji)
        
        except discord.HTTPException as e:
            print(f"Error scanning channel {channel.name}: {e}")
        
        return reconnected

    async def auto_scan_all_guilds(self) -> dict:
        """
        Automatically scans all guilds for role messages and reconnects them
        
        Returns:
            Dictionary mapping guild IDs to number of reconnected messages
        """
        results = {}
        scanned_channels = set()  # Track channels we've already scanned
        
        for guild in self.bot.guilds:
            guild_total = 0
            
            # First check channels that typically contain role messages
            potential_channels = []
            
            # Look for channels with relevant names
            role_channel_keywords = ['role', 'select', 'assign', 'reaction', 'class', 'profession']
            for channel in guild.text_channels:
                if any(keyword in channel.name.lower() for keyword in role_channel_keywords):
                    potential_channels.append(channel)
            
            # If no channels found by name, check recent message history in all channels
            if not potential_channels:
                potential_channels = guild.text_channels
            
            # Scan channels
            for channel in potential_channels:
                if channel.id not in scanned_channels:
                    reconnected = await self.scan_channel_roles(channel)
                    if reconnected > 0:
                        guild_total += reconnected
                        print(f"Reconnected {reconnected} role messages in #{channel.name}")
                    scanned_channels.add(channel.id)
            
            if guild_total > 0:
                results[guild.id] = guild_total
                print(f"Total reconnected messages in {guild.name}: {guild_total}")
        
        return results
