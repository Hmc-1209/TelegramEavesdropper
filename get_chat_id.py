"""
Simple script to list all your Telegram chats and their IDs
Run this to find the CHAT_TO_MONITOR value
"""

import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

async def main():
    print("="*60)
    print("📋 Telegram Chat List")
    print("="*60)

    if not API_ID or not API_HASH:
        print("❌ Error: Please set API_ID and API_HASH in .env file first")
        return

    client = TelegramClient('session_name', API_ID, API_HASH)

    print("\n🔐 Logging in to Telegram...")
    await client.start()
    print("✅ Login successful!\n")

    print("="*60)
    print("Your Chats/Groups/Channels:")
    print("="*60)

    # Get all dialogs (chats)
    dialogs = await client.get_dialogs()

    for i, dialog in enumerate(dialogs, 1):
        chat = dialog.entity
        chat_type = "Unknown"

        # Determine chat type
        if hasattr(chat, 'broadcast'):
            chat_type = "Channel" if chat.broadcast else "Group"
        elif hasattr(chat, 'first_name'):
            chat_type = "User"

        # Get title/name
        title = getattr(chat, 'title', None) or \
                f"{getattr(chat, 'first_name', '')} {getattr(chat, 'last_name', '')}".strip()

        # Get username if available
        username = getattr(chat, 'username', None)
        username_str = f"@{username}" if username else "No username"

        # Get ID
        chat_id = chat.id

        print(f"\n{i}. {title}")
        print(f"   Type: {chat_type}")
        print(f"   ID: {chat_id}")
        print(f"   Username: {username_str}")
        print(f"   -" * 30)

    print("\n" + "="*60)
    print("💡 Tips:")
    print("   - Use '@username' if available (e.g., @groupname)")
    print("   - Or use the exact title name")
    print("   - Or use the numeric ID")
    print("="*60)

    await client.disconnect()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
