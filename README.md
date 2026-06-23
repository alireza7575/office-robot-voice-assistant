# Office Robot Voice Assistant

## Overview

Oliver is a voice-interactive office robot assistant prototype. It uses microphone input, speech transcription, OpenAI chat completions, and text-to-speech playback to demonstrate a conversational robot workflow.

## Prerequisites

- Python 3.10 or newer
- Internet connection
- Microphone and audio output device
- OpenAI API key provided through the `OPENAI_API_KEY` environment variable

## Installation

Clone the repository:

```bash
git clone https://github.com/alireza7575/office-robot-voice-assistant.git
cd office-robot-voice-assistant
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set your OpenAI API key before running the application:

```bash
set OPENAI_API_KEY=your-openai-api-key
```

For PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-openai-api-key"
```

## Running the Application

Run the application with Python:

```bash
python main.py
```

Optional runtime settings:

```bash
python main.py --wake-word oliver --voice alloy --phrase-time-limit 10
```

Environment variables are also supported:

```bash
OLIVER_MODEL=gpt-4o-mini
OLIVER_TTS_MODEL=tts-1
OLIVER_TRANSCRIPTION_MODEL=whisper-1
OLIVER_VOICE=alloy
OLIVER_AUDIO_DIR=audio
```

## Usage

Begin commands with "Oliver" so the robot knows the request is directed at it. The prototype can respond conversationally, provide status updates, and recognize example commands such as "empty trash."

For example:

```text
Oliver, can you pick up the trash on the first floor?
```

## Demonstration

Watch Oliver in action:

[![Oliver Robot](https://github.com/alireza7575/Oliver-Robot/assets/41507280/e2231655-53b0-4954-8154-5d56f54e43ee)](https://youtu.be/bHiHujXHWiA "Oliver Robot")

## Troubleshooting

- Ensure your microphone and audio output device are configured correctly.
- On some systems, `PyAudio` requires OS-level PortAudio dependencies before `pip install -r requirements.txt` succeeds.
- Check your internet connection before starting the application.
- Confirm that `OPENAI_API_KEY` is set in the same terminal session used to run the app.
- If OpenAI API calls fail, check your account, key permissions, and usage limits.

## Notes

- Generated audio files are written to `audio/` by default and ignored by Git.
- This is a prototype interaction layer. Physical robot navigation and trash-collection logic are represented as command hooks, not full autonomy.
