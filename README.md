# Telegram Eavesdropper

Automatically monitors Telegram chat rooms, detects files, and records surrounding messages.

## Features

- 🎯 Real-time monitoring of specified Telegram chat rooms
- 📁 Automatic download of files sent by users
- 💬 Record messages before and after files (configurable count)
- 🗂️ Organize files by user and timestamp
- ⏱️ Smart grouping: Files sent within 1 minute are grouped together
- 📝 Generate readable message log txt files

## File Structure

```
TelegramEavesdropper/
├── telegram_monitor.py    # Main program
├── start_monitor.bat      # Windows launcher
├── requirements.txt       # Python dependencies
├── .env                  # Your configuration (DO NOT commit)
├── .env.example          # Configuration template
├── .gitignore            # Git ignore rules
├── README.md             # Documentation
└── output/               # Output folder (auto-created)
    └── Username/
        └── 2025-12-24_14-30-25/
            ├── file1.jpg
            ├── file2.pdf
            └── messages.txt
```

## Installation

### 1. Install Python

Ensure Python 3.7 or newer is installed on your computer.

- Download: https://www.python.org/downloads/
- Remember to check "Add Python to PATH" during installation

### 2. Get Telegram API Credentials

1. Go to https://my.telegram.org
2. Log in with your phone number
3. Click "API development tools"
4. Create a new application and note down:
   - **API ID** (numeric)
   - **API Hash** (string)

### 3. Configure Environment Variables

A `.env` file has been created for you. Edit it and fill in your credentials:

```bash
# Edit the .env file
notepad .env
```

Fill in your information:

```env
# Your API ID (numeric value)
API_ID=12345678

# Your API Hash (string value)
API_HASH=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

# Chat room to monitor
CHAT_TO_MONITOR=@groupname
```

**Important:**
- ⚠️ **Never commit the `.env` file to Git** (it's already in `.gitignore`)
- The `.env.example` file is a template for reference
- You can use username (`@groupname`), display name, or numeric ID for `CHAT_TO_MONITOR`

### 4. Install Dependencies

Open Command Prompt and run:

```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Using .bat file (Recommended)

Simply double-click `start_monitor.bat` to start the monitor.

### Method 2: Using Command Line

```bash
python telegram_monitor.py
```

### First Run

On first execution, the program will ask for:

1. Your phone number (with country code, e.g.: +886912345678)
2. Verification code sent by Telegram
3. Password (if two-step verification is enabled)

Subsequent runs will use the saved session, no need to log in again.

## Configuration Options

### Environment Variables (in `.env` file)

```env
API_ID=12345678                    # Your Telegram API ID
API_HASH=your_api_hash_here        # Your Telegram API Hash
CHAT_TO_MONITOR=@groupname         # Chat room to monitor
```

### Advanced Settings (in `telegram_monitor.py`)

You can adjust the following parameters by editing the Python script:

```python
# Number of messages before and after
MESSAGES_BEFORE = 5  # Messages before file
MESSAGES_AFTER = 5   # Messages after file

# File grouping time window (seconds)
GROUP_TIME_WINDOW = 60  # 60 seconds = 1 minute

# Output directory
OUTPUT_DIR = 'output'
```

## How It Works

### File Grouping Logic

- When a user sends a file, a new timestamped folder is created
- If the same user sends another file **within 1 minute**, it's grouped in the same folder
- After 1 minute, a new folder is created

### Message Recording Logic

- Messages are only recorded when the **first file** appears
- Only messages from the **same user** are recorded
- Records 5 messages before + 5 messages after by default

### Output Example

`messages.txt` content:

```
=== Telegram Message Log ===
User: @username
Record Time: 2025-12-24 14:30:25
==================================================

[2025-12-24 14:28:10] @username: Previous message 1
[2025-12-24 14:28:45] @username: Previous message 2
[2025-12-24 14:29:30] @username: I'll send you a file
[2025-12-24 14:30:00] @username: This is important data
[2025-12-24 14:30:15] @username: Please check
[2025-12-24 14:30:25] @username: [Photo] photo.jpg
[2025-12-24 14:30:30] @username: And this one
[2025-12-24 14:30:35] @username: [File] document.pdf
[2025-12-24 14:31:00] @username: Did you get it?
[2025-12-24 14:31:20] @username: Please confirm
[2025-12-24 14:31:45] @username: Thanks
```

## FAQ

### Q: Can I monitor multiple chat rooms?

Currently, only one chat room can be monitored at a time. To monitor multiple:
- Modify `CHAT_TO_MONITOR` to a list
- Or run multiple script instances

### Q: How do I find the chat room name or ID?

`CHAT_TO_MONITOR` can use:
- Username (if available): `@groupname`
- Display name: `'My Group Name'`
- Numeric ID: `-1001234567890`

### Q: Will all file types be downloaded?

Yes, including:
- Images (jpg, png, gif, etc.)
- Documents (pdf, docx, xlsx, etc.)
- Videos, audio files
- All other file types

### Q: Do I need to keep desktop Telegram open?

**No**. This script is an independent Telegram client.

### Q: How secure is it?

- API credentials are stored in the `.env` file locally (not committed to Git)
- Session data is stored in `*.session` files (also not committed to Git)
- Do not share your `.env` file or `*.session` files with anyone
- The `.gitignore` file is configured to prevent accidental commits of sensitive data

## Stopping the Monitor

Press `Ctrl + C` in the terminal window to stop the program.

## License

MIT License

## Disclaimer

⚠️ Please comply with Telegram's Terms of Service and local laws.
⚠️ This tool is for legitimate use only. Do not use for unauthorized monitoring.
⚠️ Only use in chat rooms where you have permission.
