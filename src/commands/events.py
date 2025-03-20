"""
Event handler module for Discord events like reactions
"""
import discord
from discord.ext import commands

class Events(commands.Cog):
    """
    Cog to handle various Discord events
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        Event handler for when a reaction is added to a message

        Args:
            payload (discord.RawReactionActionEvent): Reaction data
        """
        # Forward to role handler
        await self.bot.role_handler.handle_reaction(payload, add=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """
        Event handler for when a reaction is removed from a message

        Args:
            payload (discord.RawReactionActionEvent): Reaction data
        """
        # Forward to role handler
        await self.bot.role_handler.handle_reaction(payload, add=False)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        Event handler for when the bot joins a new guild

        Args:
            guild (discord.Guild): The guild the bot joined
        """
        print(f"Joined a new guild: {guild.name} (ID: {guild.id})")

        # If the guild has a system channel, send a welcome message
        if guild.system_channel:
            embed = discord.Embed(
                title="👋 Hello!",
                description=(
                    "The Bear has arrived.Thanks for adding me to your server! "
                    "I'm designed to help manage roles through reactions.\n\n"
                    "**Commands**:\n"
                    "• `!setup_roles` - Creates all the roles\n"
                    "• `!create_role_messages` - Creates all reaction role messages\n"
                    "• `!setup_category [category] [channel]` - Sets up roles for a specific category\n\n"
                    "You need admin permissions to use these commands."
                ),
                color=discord.Color.blue()
            )

            try:
                await guild.system_channel.send(embed=embed)
            except discord.HTTPException:
                pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Global error handler for command errors

        Args:
            ctx (commands.Context): The invocation context
            error (commands.CommandError): The error that was raised
        """
        # Handle permission errors
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")

        # Handle missing required arguments
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: `{error.param.name}`.")

        # Handle command not found
        elif isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors

        # Handle all other errors
        else:
            await ctx.send(f"❌ An error occurred: {str(error)}")
            # Log the error for debugging
            print(f"Error in command {ctx.command}: {error}")

async def setup(bot):
    """
    Setup function for loading the cog
    """
    await bot.add_cog(Events(bot))
