"""
Configuration file for the Discord bot
Contains token, prefix, and role definitions
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')  # Get token from environment variable
PREFIX = os.getenv('BOT_PREFIX', '!')  # Get prefix from env with fallback to '!'
APPLICATION_ID = int(os.getenv('APPLICATION_ID', '1351980775112704110'))
# PUBLIC_KEY = os.getenv('PUBLIC_KEY', '0546fa0a1223d30abc4b97299bdeb9fcb6234d969bc1c69426a7b90d718469c2')

# Server configuration
SERVER_ID = int(os.getenv('SERVER_ID', '0'))  # Get server ID from environment variable

# WoW Class Colors in hex format
CLASS_COLORS = {
    "Death Knight": 0xC41E3A,  # Red
    "Demon Hunter": 0xA330C9,  # Purple
    "Druid": 0xFF7C0A,        # Orange
    "Evoker": 0x33937F,       # Green-Blue
    "Hunter": 0xAAD372,       # Light Green
    "Mage": 0x3FC7EB,        # Light Blue
    "Monk": 0x00FF98,        # Jade Green
    "Paladin": 0xF48CBA,     # Pink
    "Priest": 0xFFFFFF,      # White
    "Rogue": 0xFFF468,       # Yellow
    "Shaman": 0x0070DD,      # Blue
    "Warlock": 0x8788EE,     # Purple
    "Warrior": 0xC69B6D      # Brown
}

# Role categories and their emoji mappings
ROLE_CATEGORIES = {
    "primary_professions": {
        "title": "Choose Your Primary Professions:",
        "roles": {
            "⚗️": "Alchemy",
            "⚒️": "Blacksmithing",
            "✨": "Enchanting",
            "🛠️": "Engineering",
            "🖋️": "Inscription",
            "💎": "Jewelcrafting",
            "👜": "Leatherworking",
            "🧵": "Tailoring"
        }
    },
    "gathering_professions": {
        "title": "Choose Your Gathering Professions:",
        "roles": {
            "🌿": "Herbalism",
            "⛏️": "Mining",
            "🔪": "Skinning"
        }
    },
    "secondary_professions": {
        "title": "Choose Your Secondary Professions:",
        "roles": {
            "🍳": "Cooking",
            "🎣": "Fishing",
            "🏺": "Archaeology"
        }
    },
    "classes": {
        "title": "Choose Your Class:",
        "roles": {
            "💀": "Death Knight",
            "😈": "Demon Hunter",
            "🐻": "Druid",
            "🐉": "Evoker",
            "🏹": "Hunter",
            "🪄": "Mage",
            "🥋": "Monk",
            "🛡️": "Paladin",
            "🙏": "Priest",
            "🗡️": "Rogue",
            "⚡": "Shaman",
            "🔮": "Warlock",
            "⚔️": "Warrior"
        }
    },
    "timezones": {
        "title": "Choose Your Timezone!",
        "roles": {
            "🌎": "US-Eastern (EST/EDT)",
            "🌍": "US-Central (CST/CDT)",
            "🌏": "US-Mountain (MST/MDT)",
            "🌐": "US-Pacific (PST/PDT)",
            "🕐": "Hawaii (HST)",
            "🕑": "Alaska (AKST/AKDT)",
            "🕒": "Central Europe (CET/CEST)",
            "🕓": "UK & Ireland (GMT/BST)",
            "🕔": "Eastern Europe (EET/EEST)",
            "🕕": "Moscow (MSK)",
            "🕖": "India (IST)",
            "🕗": "China (CST)",
            "🕘": "Japan/Korea (JST/KST)",
            "🕙": "Australia East (AEST)",
            "🕚": "New Zealand (NZST)",
            "🕛": "UTC/GMT"
        }
    },
    "player_types": {
        "title": "How do you play?",
        "roles": {
            "😎": "Casual",
            "🔥": "Competitive",
            "💀": "Hardcore"
        }
    }
}

# Colors for role categories (using Discord color values)
ROLE_COLORS = {
    "primary_professions": 0x3498db,  # Blue
    "gathering_professions": 0x2ecc71,  # Green
    "secondary_professions": 0xe74c3c,  # Red
    "classes": 0x9b59b6,  # Purple (default, will be overridden by class color)
    "timezones": 0xf1c40f,  # Yellow
    "player_types": 0xe67e22   # Orange
}
