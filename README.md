# Telegram Eavesdropper

Automatically monitors Telegram chat rooms, detects files, and records surrounding messages.

## Features

- 🎯 Real-time monitoring of specified Telegram chat rooms
- 📁 Automatic download of files sent by users
- 💬 Record messages before and after files (configurable count)
- 🗂️ Organize files by user and timestamp
- ⏱️ Smart grouping: Files sent within 1 minute are grouped together
- 📝 Generate readable message log txt files
- 🔄 Multi-threaded: Multiple users can send files simultaneously

## Output Structure

```
output/
└── Username/
    └── 2025-12-24_14-30-25/
        ├── file1.jpg
        ├── file2.pdf
        └── messages.txt
```

## Installation

### 1. Install Python

Python 3.7 or newer is required.

Download: https://www.python.org/downloads/

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Telegram API Credentials

1. Visit https://my.telegram.org
2. Log in with your phone number
3. Click "API development tools"
4. Create a new application
5. Copy your **API ID** and **API Hash**

### 4. Configure .env File

Edit the `.env` file:

```env
API_ID=12345678
API_HASH=your_api_hash_here
CHAT_TO_MONITOR=@groupname
```

**CHAT_TO_MONITOR** accepts:
- Username: `@groupname`
- Display name: `My Group Name`
- Numeric ID: `5081822247` or `-1001234567890`

**Tip**: Run `python get_chat_id.py` to list all your chats and their IDs

## Usage

### Start Monitor

**Windows**: Double-click `start_monitor.bat`

**Command Line**:
```bash
python telegram_monitor.py
```

### First Run

On first execution, you'll be prompted for:
1. Phone number (with country code, e.g., +886912345678)
2. Verification code from Telegram
3. Password (if two-step verification enabled)

Session is saved automatically for subsequent runs.

## Configuration

### Advanced Settings

Edit `telegram_monitor.py` to customize:

```python
MESSAGES_BEFORE = 5          # Messages to capture before file
MESSAGES_AFTER = 5           # Messages to capture after file
GROUP_TIME_WINDOW = 60       # File grouping window (seconds)
OUTPUT_DIR = 'output'        # Output directory
```

## How It Works

**File Grouping**: Files from the same user sent within 60 seconds are grouped in one folder

**Message Recording**: Captures 5 messages before and after the first file (same user only)

**Output Example** (`messages.txt`):

```
=== Telegram Message Log ===
User: @username
Record Time: 2025-12-24 14:30:25
==================================================

[2025-12-24 14:29:30] @username: I'll send you a file
[2025-12-24 14:30:00] @username: This is important data
[2025-12-24 14:30:15] @username: Please check
[2025-12-24 14:30:25] @username: [Photo] photo.jpg
[2025-12-24 14:30:30] @username: And this one
[2025-12-24 14:30:35] @username: [File] document.pdf
[2025-12-24 14:31:00] @username: Did you get it?
```

## FAQ

**Q: Can I monitor multiple chat rooms?**
Run multiple script instances with different `.env` configurations.

**Q: How to find chat ID?**
Run `python get_chat_id.py` to list all your chats with their IDs.

**Q: What file types are supported?**
All types: images, documents, videos, audio, etc.

**Q: Need to keep Telegram desktop open?**
No. This is an independent Telegram client.

**Q: How to stop monitoring?**
Press `Ctrl + C` in the terminal.

## Disclaimer

This tool is for educational and legitimate monitoring purposes only. Ensure you have proper authorization before monitoring any chat room. Comply with Telegram's Terms of Service and applicable laws.

## License

MIT License
