# ContentBuddy

**ContentBuddy** is a desktop Python application designed to automate and streamline the workflow of recording and uploading YouTube videos, specifically tailored to people working on a series. It integrates with OBS Studio via WebSockets, manages video file naming and episode tracking, captures thumbnail poses using OpenCV, and automates thumbnail creation using Photopea and Imgur. It also features Whisper powered transcription for future use in title, description, and timestamp generation.


How I'm Using it:

https://www.youtube.com/@ojedi_chess

I started recording Chess game videos 5-7x a week as a way of measuring and sharing my progress. Being my first time uploading consistently to YouTube, I realized how many tedious some of the tasks were that go into uploading videos, especially with creating videos. So I began developing ContentBuddy as a means of reducing the workload and saving time.


## Features

- 🎥 **OBS Remote Control**: Start/stop OBS recording from the GUI.
- 🔢 **Episode Tracking**: Automatically names video files and increments episode count using SQLite.
- 🖼 **Thumbnail Automation**:
  - Captures the best thumbnail pose with OpenCV.
  - Loads the screenshot and template into Photopea via custom script.
- 📝 **Transcription Generator**:
  - Uses Whisper to transcribe videos.
  - Saves transcript files to a `transcripts/` directory.
- 🧠 **Future Plans**: Designed to support auto title/description generation and timestamp tagging using WhisperX.

## Technologies Used

- Python
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
Set Up .env File with the following:

    IMGUR_CLIENT_ID=your_imgur_client_id

Ensure OBS Studio is Installed

Download and install OBS Studio and enable WebSocket support (port 4455).

Create config.toml file with following format:
    [connection]
    host = "localhost"
    port = 4455
    password = "###############"

Run the App

    python main.py