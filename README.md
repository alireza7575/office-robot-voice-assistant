# Oliver Robot Application

## Overview

Oliver Robot is a voice-interactive office assistant prototype. It uses speech recognition, audio playback, and OpenAI models to respond to voice commands and demonstrate robot interaction flows.

## Prerequisites

- Python 3.11 or lower
- Internet connection
- Microphone and audio output device
- OpenAI API key provided through the `OPENAI_API_KEY` environment variable

## Installation

Clone the repository:

```bash
git clone https://github.com/alireza7575/Oliver-Robot.git
cd Oliver-Robot
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
- Check your internet connection before starting the application.
- Confirm that `OPENAI_API_KEY` is set in the same terminal session used to run the app.
- If OpenAI API calls fail, check your account, key permissions, and usage limits.
