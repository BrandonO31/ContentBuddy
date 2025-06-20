# ContentBuddy

**ContentBuddy** is a desktop Python application designed to automate and streamline the workflow of recording and uploading YouTube videos, especially for chess content creators. It integrates with OBS Studio via WebSockets, manages video file naming and episode tracking, captures thumbnail poses using OpenCV, and automates thumbnail creation using Photopea and Imgur. It also features Whisper-powered transcription for future use in title, description, and timestamp generation.

## Features

- 🎥 **OBS Remote Control**: Start/stop OBS recording from the GUI.
- 🔢 **Episode Tracking**: Automatically names video files and increments episode count using SQLite.
- 🖼 **Thumbnail Automation**:
  - Captures the best thumbnail pose with OpenCV.
  - Loads the screenshot and template into Photopea via custom script.
- 📝 **Transcription Generator**:
  - Uses Whisper to transcribe videos.
  - Saves transcript files to a `transcripts/` directory.
- 🧠 **Future Expansion**: Designed to support auto title/description generation and timestamp tagging using WhisperX.

## Technologies Used

- Python 3.x
- Dear PyGui for GUI
- OBS WebSocket via `obsws-python`
- SQLite for local storage
- Whisper by OpenAI for transcription
- Photopea scripting for thumbnail automation
- Imgur API for image upload

## Setup Instructions

1. **Install Requirements**

```bash
pip install -r requirements.txt
Set Up .env File

Create a .env file in your root directory:

ini
Always show details

Copy
IMGUR_CLIENT_ID=your_imgur_client_id
Ensure OBS Studio is Installed

Download and install OBS Studio and enable WebSocket support (port 4455).

Run the App

bash
Always show details

Copy
python main.py