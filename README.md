# Discord Role Management Bot

A Discord bot designed to manage roles through reactions, specifically tailored for gaming communities with features for managing professions, classes, timezones, and player types. The bot uses a reaction-based system allowing users to self-assign roles by clicking on emojis.

## Features

### Role Categories
- **Primary Professions**: Alchemy, Blacksmithing, Enchanting, Engineering, Inscription, Jewelcrafting, Leatherworking, Tailoring
- **Gathering Professions**: Herbalism, Mining, Skinning
- **Secondary Professions**: Cooking, Fishing, Archaeology
- **Classes** (with class-specific colors):
  - Death Knight (Red)
  - Demon Hunter (Purple)
  - Druid (Orange)
  - Evoker (Green-Blue)
  - Hunter (Light Green)
  - Mage (Light Blue)
  - Monk (Jade Green)
  - Paladin (Pink)
  - Priest (White)
  - Rogue (Yellow)
  - Shaman (Blue)
  - Warlock (Purple)
  - Warrior (Brown)
- **Timezones**: Comprehensive coverage of global timezones including US, Europe, Asia, and Oceania regions
- **Player Types**: Casual, Competitive, Hardcore

## Setup

### Prerequisites
- Python 3.8 or higher
- Discord.py library
- A Discord Bot Token
- Server Admin permissions

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd discordBot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following content:
```env
DISCORD_TOKEN=your_bot_token_here
BOT_PREFIX=!
APPLICATION_ID=your_application_id_here
PUBLIC_KEY=your_public_key_here
SERVER_ID=your_server_id
```

4. Enable Required Bot Intents:
- Go to the [Discord Developer Portal](https://discord.com/developers/applications)
- Select your application
- Go to the "Bot" section
- Copy your Application ID and Public Key
- Enable the following Privileged Gateway Intents:
  - PRESENCE INTENT
  - SERVER MEMBERS INTENT
  - MESSAGE CONTENT INTENT

5. Invite the bot to your server using the OAuth2 URL generator in the Discord Developer Portal
   - Required permissions: Manage Roles, Send Messages, Read Message History, Add Reactions

### Running the Bot
```bash
python src/main.py
```

## Commands

All commands require administrator permissions:

- `!setup_roles` - Creates all roles defined in the configuration
- `!create_role_messages` - Creates all reaction role messages in the current channel
- `!setup_category [category] #channel` - Sets up roles for a specific category in the specified channel
- `!repost_category [category] #channel` - Reposts a category's role message (useful after making changes)
- `!scan_roles [#channel]` - Scans and reconnects existing role messages to the bot

Available categories:
- `primary_professions`
- `gathering_professions`
- `secondary_professions`
- `classes`
- `timezones`
- `player_types`

## Usage Examples

1. Set up all roles in the server:
```
!setup_roles
```

2. Create role selection messages in a specific channel:
```
!create_role_messages #role-selection
```

3. Set up a specific category in a dedicated channel:
```
!setup_category classes #class-selection
!setup_category timezones #timezone-select
```

4. Update a category's message after making changes:
```
!repost_category timezones #timezone-select
```

5. Reconnect existing role messages after bot restart:
```
!scan_roles #role-selection
```

## Project Structure

```
discordBot/
├── src/
│   ├── main.py              # Main bot file and startup logic
│   ├── commands/
│   │   ├── events.py        # Event handlers (reactions, joins)
│   │   └── setup.py         # Role setup and management commands
│   ├── config/
│   │   └── config.py        # Role definitions and bot settings
│   ├── handlers/
│   │   └── role_handler.py  # Core role management logic
│   └── utils/
│       └── role_utils.py    # Helper functions for role operations
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables (private)
└── .env.example           # Environment variable template
```

## Customization

The bot's configuration can be modified in `src/config/config.py`:
- Role categories and their emoji mappings
- Role colors
- Class-specific colors
- Command prefix

## Error Handling

The bot includes comprehensive error handling for common issues:
- Missing permissions
- Invalid categories
- Channel not found
- Rate limiting
- API errors

## Recovery and Maintenance

### Reconnecting Role Messages
If the bot restarts or loses connection to role messages, you can use the `!scan_roles` command to reconnect them:
- Scans the specified channel (or current channel if none specified)
- Finds and reconnects role messages to the bot
- Adds any missing reactions
- Useful after:
  - Bot restarts
  - Moving role messages to a different channel
  - Verifying role message functionality

Example:
```bash
# Scan current channel
!scan_roles

# Scan specific channel
!scan_roles #role-selection
```

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Committing your changes
4. Opening a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
