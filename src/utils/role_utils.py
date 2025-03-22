"""
Utility functions for role management
"""
import discord
import asyncio
from typing import List, Dict, Any, Optional

async def batch_process_roles(
    guild: discord.Guild,
    role_names: List[str],
    color: discord.Color,
    chunk_size: int = 5,
    delay: float = 1.0
) -> List[discord.Role]:
    """
    Process role creation in batches to avoid rate limits

    Args:
        guild: The guild to create roles in
        role_names: List of role names to create
        color: Color to apply to the roles
        chunk_size: Number of roles to create per batch
        delay: Delay between batches in seconds

    Returns:
        List of created role objects
    """
    created_roles = []

    # Process in chunks to avoid rate limits
    for i in range(0, len(role_names), chunk_size):
        chunk = role_names[i:i + chunk_size]

        # Create roles in this chunk
        for role_name in chunk: 
            existing_role = discord.utils.get(guild.roles, name=role_name)
            if existing_role:
                created_roles.append(existing_role)
            else:
                try:
                    new_role = await guild.create_role(
                        name=role_name,
                        color=color,
                        mentionable=True
                    )
                    created_roles.append(new_role)
                except discord.HTTPException as e:
                    print(f"Error creating role {role_name}: {e}")

        # Wait between chunks to avoid rate limits
        if i + chunk_size < len(role_names):
            await asyncio.sleep(delay)

    return created_roles

async def safely_add_reaction(
    message: discord.Message,
    emoji: str,
    delay: float = 0.5
) -> bool:
    """
    Safely add a reaction to a message with rate limiting consideration

    Args:
        message: The message to add reaction to
        emoji: The emoji to react with
        delay: Delay after adding reaction

    Returns:
        Success status as boolean
    """
    try:
        await message.add_reaction(emoji)
        await asyncio.sleep(delay)
        return True
    except discord.HTTPException as e:
        print(f"Error adding reaction {emoji}: {e}")
        return False

def build_role_embed(
    title: str,
    roles: Dict[str, str],
    color: discord.Color,
    footer_text: Optional[str] = None
) -> discord.Embed:
    """
    Build an embed for role selection message

    Args:
        title: Title of the embed
        roles: Dictionary mapping emoji to role names
        color: Color of the embed
        footer_text: Optional text for the embed footer

    Returns:
        Discord Embed object
    """
    embed = discord.Embed(
        title=title,
        description="React to get your roles!",
        color=color
    )

    # Add role descriptions to embed
    role_descriptions = []
    for emoji, role_name in roles.items():
        role_descriptions.append(f"{emoji} - {role_name}")

    embed.description = "\n".join(role_descriptions)

    if footer_text:
        embed.set_footer(text=footer_text)

    return embed

async def get_or_fetch_channel(
    bot: Any,
    channel_id: int
) -> Optional[discord.TextChannel]:
    """
    Get or fetch a channel by ID

    Args:
        bot: Bot instance
        channel_id: ID of the channel

    Returns:
        Channel object or None if not found
    """
    channel = bot.get_channel(channel_id)

    if not channel:
        try:
            channel = await bot.fetch_channel(channel_id)
        except discord.HTTPException:
            return None

    return channel
