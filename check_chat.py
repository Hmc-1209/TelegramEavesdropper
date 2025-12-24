"""
Check specific chat/user ID to diagnose issues
"""

import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

async def check_chat(chat_id_to_check):
    """Check if a specific chat ID is valid and accessible"""
    print("="*60)
    print("🔍 Telegram Chat ID Checker")
    print("="*60)

    if not API_ID or not API_HASH:
        print("❌ Error: API_ID and API_HASH not found in .env")
        return

    client = TelegramClient('session_name', API_ID, API_HASH)

    print(f"\n🔐 Logging in to Telegram...")
    await client.start()
    print("✅ Login successful!\n")

    print(f"🔎 Checking ID: {chat_id_to_check}")
    print("="*60)

    try:
        # Try to get the entity
        entity = await client.get_entity(chat_id_to_check)

        # Determine entity type
        entity_type = "Unknown"
        if hasattr(entity, 'broadcast'):
            entity_type = "Channel" if entity.broadcast else "Group/Supergroup"
        elif hasattr(entity, 'first_name'):
            entity_type = "User"

        # Get name/title
        if hasattr(entity, 'title'):
            name = entity.title
        elif hasattr(entity, 'first_name'):
            name = f"{entity.first_name or ''} {entity.last_name or ''}".strip()
        else:
            name = "Unknown"

        # Get username
        username = getattr(entity, 'username', None)
        username_str = f"@{username}" if username else "No username"

        # Display results
        print(f"✅ Successfully found!")
        print(f"\n📋 Details:")
        print(f"   Name/Title: {name}")
        print(f"   Type: {entity_type}")
        print(f"   ID: {entity.id}")
        print(f"   Username: {username_str}")

        # Additional info
        if entity_type == "User":
            print(f"\n💡 This is a personal chat/user")
            if entity.id == (await client.get_me()).id:
                print(f"   ⭐ This is YOUR account (Saved Messages)")
        elif entity_type in ["Group/Supergroup", "Channel"]:
            print(f"\n💡 This is a {entity_type.lower()}")
            print(f"   You can monitor this chat")

        # Check permissions
        print(f"\n🔓 Access Status:")
        print(f"   ✅ You have access to this chat")

        # Suggest .env configuration
        print(f"\n📝 .env Configuration:")
        print(f"   Option 1 (by ID): CHAT_TO_MONITOR={entity.id}")
        if username:
            print(f"   Option 2 (by username): CHAT_TO_MONITOR=@{username}")
        print(f"   Option 3 (by name): CHAT_TO_MONITOR={name}")

    except ValueError as e:
        print(f"❌ Error: Cannot find chat with ID {chat_id_to_check}")
        print(f"   Details: {e}")
        print(f"\n💡 Possible reasons:")
        print(f"   - This ID doesn't exist")
        print(f"   - You don't have access to this chat")
        print(f"   - The chat was deleted")
        print(f"\n💡 Suggestion: Run 'python get_chat_id.py' to see all your chats")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*60)
    await client.disconnect()


if __name__ == '__main__':
    # Get chat ID from user
    print("\n" + "="*60)
    chat_to_check = input("Enter Chat ID to check (or press Enter for 5081822247): ").strip()

    if not chat_to_check:
        chat_to_check = "5081822247"

    # Try to convert to int if it's a number
    try:
        chat_to_check = int(chat_to_check)
    except ValueError:
        pass  # Keep as string if not a number

    try:
        asyncio.run(check_chat(chat_to_check))
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
