"""
Telegram Chat Room Monitor
Monitors Telegram chat rooms and automatically downloads files with surrounding messages
"""

import os
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# Configuration - Loaded from .env file
# ============================================

# Get from https://my.telegram.org
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

# Chat room to monitor (can be username, display name, or numeric ID)
CHAT_TO_MONITOR = os.getenv('CHAT_TO_MONITOR')

# Convert to int if it's a numeric ID
if CHAT_TO_MONITOR and CHAT_TO_MONITOR.lstrip('-').isdigit():
    CHAT_TO_MONITOR = int(CHAT_TO_MONITOR)

# Output directory
OUTPUT_DIR = 'output'

# Settings: Number of messages before and after
MESSAGES_BEFORE = 5
MESSAGES_AFTER = 5

# Settings: File grouping time window (seconds)
GROUP_TIME_WINDOW = 60  # 60 seconds = 1 minute

# ============================================
# Global Variables
# ============================================

# Store file grouping information for each user
user_file_groups = defaultdict(lambda: {
    'first_file_time': None,
    'last_file_time': None,
    'files': [],
    'folder_path': None,
    'messages_saved': False
})

# Message buffer (for getting surrounding messages)
message_buffer = []
MAX_BUFFER_SIZE = 100  # Keep the last 100 messages


# ============================================
# Helper Functions
# ============================================

def sanitize_filename(name):
    """Sanitize filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name


def get_user_display_name(sender):
    """Get user display name"""
    if sender.username:
        return f"@{sender.username}"
    elif sender.first_name or sender.last_name:
        name_parts = []
        if sender.first_name:
            name_parts.append(sender.first_name)
        if sender.last_name:
            name_parts.append(sender.last_name)
        return ' '.join(name_parts)
    else:
        return f"User_{sender.id}"


def format_message_text(message, sender_name):
    """Format message text"""
    timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S')

    # Determine message type
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            media_type = "[Photo]"
        elif isinstance(message.media, MessageMediaDocument):
            media_type = "[File]"
        else:
            media_type = "[Media]"

        text = message.message if message.message else media_type
        return f"[{timestamp}] {sender_name}: {media_type} {text}"
    else:
        text = message.message if message.message else "[No text content]"
        return f"[{timestamp}] {sender_name}: {text}"


async def get_surrounding_messages(client, chat, user_id, center_message):
    """
    Get messages before and after a specified message (only from the same user)
    """
    messages_before = []
    messages_after = []

    # Get messages before
    async for message in client.iter_messages(chat, limit=50, offset_id=center_message.id, reverse=False):
        if message.sender_id == user_id:
            messages_before.append(message)
            if len(messages_before) >= MESSAGES_BEFORE:
                break

    # Get messages after
    async for message in client.iter_messages(chat, limit=50, min_id=center_message.id):
        if message.id == center_message.id:
            continue
        if message.sender_id == user_id:
            messages_after.append(message)
            if len(messages_after) >= MESSAGES_AFTER:
                break

    # Reverse messages_before to maintain chronological order
    messages_before.reverse()

    return messages_before, messages_after


async def save_messages_to_file(client, chat, user_id, user_name, folder_path, center_message):
    """Save surrounding messages to txt file"""
    messages_before, messages_after = await get_surrounding_messages(client, chat, user_id, center_message)

    # Combine all messages
    all_messages = messages_before + [center_message] + messages_after

    # Write to file
    txt_path = os.path.join(folder_path, 'messages.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"=== Telegram Message Log ===\n")
        f.write(f"User: {user_name}\n")
        f.write(f"Record Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*50}\n\n")

        for msg in all_messages:
            sender = await msg.get_sender()
            sender_name = get_user_display_name(sender)
            f.write(format_message_text(msg, sender_name) + '\n')

    print(f"💾 Message log saved: {txt_path}")


def should_create_new_group(user_id, current_time):
    """Determine if a new file group should be created"""
    group_info = user_file_groups[user_id]

    # If this is the first file
    if group_info['first_file_time'] is None:
        return True

    # If time since last file exceeds the time window
    time_diff = (current_time - group_info['last_file_time']).total_seconds()
    if time_diff > GROUP_TIME_WINDOW:
        return True

    return False


async def handle_file_message(client, event):
    """Handle messages containing files (thread-safe)"""
    message = event.message
    sender = await message.get_sender()
    user_id = sender.id
    user_name = sanitize_filename(get_user_display_name(sender))
    current_time = message.date

    # Determine if a new group needs to be created
    if should_create_new_group(user_id, current_time):
        # Create new group
        timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
        folder_path = os.path.join(OUTPUT_DIR, user_name, timestamp)
        os.makedirs(folder_path, exist_ok=True)

        # Update group information
        user_file_groups[user_id] = {
            'first_file_time': current_time,
            'last_file_time': current_time,
            'files': [],
            'folder_path': folder_path,
            'messages_saved': False,
            'first_message': message
        }

        print(f"📂 {user_name} sent a file - Created folder: {user_name}/{timestamp}")
    else:
        # Update existing group
        user_file_groups[user_id]['last_file_time'] = current_time
        print(f"📂 {user_name} sent a file - Added to existing group")

    group_info = user_file_groups[user_id]
    folder_path = group_info['folder_path']

    # Download file
    try:
        file_path = await message.download_media(file=folder_path)
        if file_path:
            filename = os.path.basename(file_path)
            group_info['files'].append(filename)
            print(f"✅ File saved: {filename}")
    except Exception as e:
        print(f"❌ File download failed: {e}")

    # Save messages if not already saved (only for first file)
    if not group_info['messages_saved']:
        first_message = group_info['first_message']
        await save_messages_to_file(
            client,
            event.chat_id,
            user_id,
            user_name,
            folder_path,
            first_message
        )
        group_info['messages_saved'] = True


# ============================================
# Main Program
# ============================================

async def main():
    """Main program"""
    print("="*60)
    print("🚀 Starting Telegram Monitor...")
    print("="*60)

    # Check configuration
    if not API_ID or not API_HASH:
        print("❌ Error: API_ID and API_HASH not found")
        print("   Please create a .env file with your credentials")
        print("   See .env.example for template")
        return

    if not CHAT_TO_MONITOR:
        print("❌ Error: CHAT_TO_MONITOR not found")
        print("   Please set CHAT_TO_MONITOR in your .env file")
        return

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Create Telegram client
    client = TelegramClient('session_name', API_ID, API_HASH)

    print("📱 Connecting to Telegram...")
    await client.start()
    print("✅ Connected successfully!")

    # Get the chat room to monitor
    try:
        chat = await client.get_entity(CHAT_TO_MONITOR)
        chat_title = getattr(chat, 'title', CHAT_TO_MONITOR)
        print(f"👀 Monitoring chat room: {chat_title}")
        print(f"📂 Files save location: {os.path.abspath(OUTPUT_DIR)}")
        print(f"⏱️  File grouping time window: {GROUP_TIME_WINDOW} seconds")
        print("="*60)
        print("Waiting for messages... (Press Ctrl+C to stop)")
        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error: Cannot find chat room '{CHAT_TO_MONITOR}'")
        print(f"   Details: {e}")
        return

    # Register event handler with concurrent processing
    @client.on(events.NewMessage(chats=chat))
    async def handler(event):
        message = event.message

        # Check if message contains media files
        if message.media:
            if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
                # Create task for concurrent processing (non-blocking)
                asyncio.create_task(handle_file_message(client, event))

    # Keep running
    print("✅ Monitor is running (multi-threaded mode enabled)...")
    print("💡 Multiple users can send files simultaneously")
    await client.run_until_disconnected()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitor stopped")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
