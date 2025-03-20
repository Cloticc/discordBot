"""
Setup command module for creating roles and setting up reaction messages
"""
import discord
from discord.ext import commands
from discord import app_commands
from config.config import ROLE_CATEGORIES

class Setup(commands.Cog):
    """
    Setup commands for creating roles and reaction messages
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setup_roles(self, ctx):
        """
        Creates all roles defined in the config
        """
        await ctx.send("📋 Setting up roles... This may take a moment.")

        try:
            # Create all roles
            created_roles = await self.bot.role_handler.create_roles(ctx.guild)

            # Send confirmation with count of roles created
            total_roles = sum(len(roles) for roles in created_roles.values())
            await ctx.send(f"✅ Successfully set up {total_roles} roles across {len(created_roles)} categories!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to manage roles. Please check my permissions and try again.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def create_role_messages(self, ctx, channel: discord.TextChannel = None):
        """
        Creates reaction role messages in the specified channel

        Args:
            channel: The channel to send messages to (defaults to current channel)
        """
        if channel is None:
            channel = ctx.channel

        await ctx.send(f"📝 Creating role messages in {channel.mention}...")

        try:
            # Create roles first to ensure they exist
            created_roles = await self.bot.role_handler.create_roles(ctx.guild)

            # Send a reaction message for each category
            sent_messages = []
            for category in ROLE_CATEGORIES:
                message = await self.bot.role_handler.send_reaction_message(
                    channel,
                    category,
                    created_roles.get(category, [])
                )
                if message:
                    sent_messages.append(message)

            await ctx.send(f"✅ Successfully created {len(sent_messages)} role selection messages!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to send messages or manage roles. Please check my permissions and try again.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setup_category(self, ctx, category: str, channel: discord.TextChannel = None):
        """
        Creates roles and reaction message for a specific category

        Args:
            category: The category to set up (e.g., 'classes', 'timezones')
            channel: The channel to send message to (defaults to current channel)
        """
        if category not in ROLE_CATEGORIES:
            await ctx.send(f"❌ Category '{category}' not found. Available categories: {', '.join(ROLE_CATEGORIES.keys())}")
            return

        if channel is None:
            channel = ctx.channel

        await ctx.send(f"📝 Setting up {category} roles and message in {channel.mention}...")

        try:
            # Create roles for this category
            created_roles = await self.bot.role_handler.create_roles(ctx.guild)
            category_roles = created_roles.get(category, [])

            # Send reaction message
            message = await self.bot.role_handler.send_reaction_message(channel, category, category_roles)

            if message:
                await ctx.send(f"✅ Successfully set up {category} roles and reaction message!")
            else:
                await ctx.send(f"❌ Failed to set up {category} message.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to send messages or manage roles. Please check my permissions and try again.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def repost_category(self, ctx, category: str, channel: discord.TextChannel = None):
        """
        Reposts a category's role message by deleting the old one and creating a new one
        Useful when you've made changes to roles and want to update the message

        Usage:
        !repost_category [category] #channel
        Example: !repost_category timezones #timezone-select

        Args:
            category: The category to repost (e.g., 'classes', 'timezones')
            channel: The channel to send message to (defaults to current channel)
        """
        if category not in ROLE_CATEGORIES:
            categories_list = ", ".join(f"`{cat}`" for cat in ROLE_CATEGORIES.keys())
            await ctx.send(f"❌ Category '{category}' not found.\nAvailable categories: {categories_list}")
            return

        if channel is None:
            channel = ctx.channel

        await ctx.send(f"🔄 Reposting {category} roles message in {channel.mention}...")

        try:
            # Find and delete existing message for this category
            existing_message_id = None
            for msg_id, data in self.bot.role_handler.role_messages.items():
                if data.get("category") == category:
                    try:
                        existing_message = await channel.fetch_message(msg_id)
                        await existing_message.delete()
                        del self.bot.role_handler.role_messages[msg_id]
                        break
                    except (discord.NotFound, discord.Forbidden):
                        continue

            # Create roles for this category
            created_roles = await self.bot.role_handler.create_roles(ctx.guild)
            category_roles = created_roles.get(category, [])

            # Send new reaction message
            message = await self.bot.role_handler.send_reaction_message(channel, category, category_roles)

            if message:
                await ctx.send(f"✅ Successfully reposted {category} roles message in {channel.mention}!")
            else:
                await ctx.send(f"❌ Failed to repost {category} message.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to manage messages or roles. Please check my permissions and try again.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def scan_roles(self, ctx, channel: discord.TextChannel = None):
        """
        Scans a channel for existing role messages and reconnects them to the bot

        Usage:
        !scan_roles [#channel]
        If no channel is specified, scans the current channel

        Args:
            channel: The channel to scan for role messages
        """
        if channel is None:
            channel = ctx.channel

        await ctx.send(f"🔍 Scanning {channel.mention} for role messages...")

        try:
            # Get bot's messages in the channel
            messages = []
            async for message in channel.history(limit=100):  # Scan last 100 messages
                if message.author == self.bot.user and message.embeds:
                    messages.append(message)

            if not messages:
                await ctx.send("❌ No role messages found in this channel.")
                return

            reconnected = 0

            # Check each message for role category titles
            for message in messages:
                if not message.embeds:
                    continue

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
                    self.bot.role_handler.role_messages[message.id] = {
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

            if reconnected > 0:
                await ctx.send(f"✅ Successfully reconnected {reconnected} role messages!")
            else:
                await ctx.send("❌ No matching role messages found in this channel.")

        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to read message history or add reactions.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @repost_category.error
    async def repost_category_error(self, ctx, error):
        """Error handler for repost_category command"""
        if isinstance(error, commands.MissingRequiredArgument):
            categories_list = ", ".join(f"`{cat}`" for cat in ROLE_CATEGORIES.keys())
            await ctx.send(
                "❌ Please specify a category and optionally a channel.\n"
                f"Usage: `!repost_category [category] #channel`\n"
                f"Available categories: {categories_list}"
            )
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send("❌ Could not find the specified channel. Please mention a valid channel.")

async def setup(bot):
    """
    Setup function for loading the cog
    """
    await bot.add_cog(Setup(bot))
