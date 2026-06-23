import io
import logging
from pathlib import Path

import pygame
import speech_recognition as sr
from openai import OpenAI


COMMAND_CATEGORIES = {"Empty Trash", "General", "Status", "Other"}


class OliverRobot:
    def __init__(
        self,
        openai_api_key,
        *,
        model="gpt-4o-mini",
        transcription_model="whisper-1",
        tts_model="tts-1",
        voice="alloy",
        audio_dir="audio",
    ):
        self.openai = OpenAI(api_key=openai_api_key)
        self.recognizer = sr.Recognizer()
        self.model = model
        self.transcription_model = transcription_model
        self.tts_model = tts_model
        self.voice = voice
        self.audio_dir = Path(audio_dir)
        self.audio_dir.mkdir(parents=True, exist_ok=True)

        logging.info("Oliver is calibrating the microphone...")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
        logging.info("Audio calibration finished.")

        pygame.mixer.init()
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are Oliver, an office robot. Your primary task is to collect "
                    "and empty trash bins. You are equipped with mobility components "
                    "for efficient movement."
                ),
            },
            {
                "role": "system",
                "content": "Interact politely and efficiently with office staff.",
            },
            {
                "role": "system",
                "content": "Use very mild humor only when it fits an office environment.",
            },
            {
                "role": "system",
                "content": "Respond concisely and clearly.",
            },
            {
                "role": "system",
                "content": (
                    "If asked about checking another floor, respond politely that the "
                    "office is busy and you will attend to it later."
                ),
            },
            {
                "role": "system",
                "content": (
                    "Communicate primarily in English and occasionally use short German "
                    "expressions that fit your Bavarian origin."
                ),
            },
        ]

    def listen_and_save_audio(
        self,
        file_name="user_input.wav",
        *,
        timeout=None,
        phrase_time_limit=None,
    ):
        output_path = self.audio_dir / file_name
        try:
            with sr.Microphone() as source:
                logging.info("Oliver is listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
                logging.info("Oliver stopped listening.")

            output_path.write_bytes(audio.get_wav_data())
            return output_path
        except sr.WaitTimeoutError:
            logging.info("No speech detected before timeout.")
        except Exception:
            logging.exception("Error while listening or saving audio.")

        return None

    def get_text_from_audio(self, file_name):
        if not file_name:
            return ""

        logging.info("Processing audio...")
        try:
            with Path(file_name).open("rb") as audio_file:
                response = self.openai.audio.transcriptions.create(
                    model=self.transcription_model,
                    file=audio_file,
                )
        except Exception:
            logging.exception("Error in audio transcription.")
            return ""

        return response.text.strip()

    def get_gpt_response(self, text):
        logging.info("Getting model response...")
        self.messages.append({"role": "user", "content": text})
        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=self.messages,
            )
        except Exception:
            logging.exception("Error getting model response.")
            return "I had trouble processing that request."

        answer = response.choices[0].message.content.strip()
        self.messages.append({"role": "assistant", "content": answer})
        return answer

    def classify_last_user_command(self):
        logging.info("Classifying the last user command...")
        user_messages = [message for message in self.messages if message["role"] == "user"]
        if not user_messages:
            return "Other"

        prompt = [
            {
                "role": "system",
                "content": (
                    "Classify the latest user request. Respond with exactly one category: "
                    "Empty Trash, General, Status, or Other."
                ),
            },
            user_messages[-1],
        ]

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=prompt,
            )
            category = response.choices[0].message.content.strip()
        except Exception:
            logging.exception("Error classifying command.")
            return "Other"

        return category if category in COMMAND_CATEGORIES else "Other"

    def reply_to_user_by_audio(self, robot_answer, file_name="robot_output.wav"):
        output_path = self.audio_dir / file_name
        logging.info("Converting Oliver's response to audio...")
        try:
            response = self.openai.audio.speech.create(
                model=self.tts_model,
                voice=self.voice,
                input=robot_answer,
            )
            audio_content = response.content
            output_path.write_bytes(audio_content)
            self.play_audio(io.BytesIO(audio_content))
        except Exception:
            logging.exception("Error converting response to audio.")

    def play_audio(self, audio_stream):
        logging.info("Playing audio to user.")
        try:
            pygame.mixer.music.load(audio_stream)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception:
            logging.exception("Error playing audio.")
