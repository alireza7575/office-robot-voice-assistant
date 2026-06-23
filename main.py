import argparse
import logging
import os
import sys

from OliverRobot import OliverRobot


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Oliver voice robot assistant prototype.")
    parser.add_argument("--wake-word", default=os.environ.get("OLIVER_WAKE_WORD", "oliver"))
    parser.add_argument("--model", default=os.environ.get("OLIVER_MODEL", "gpt-4o-mini"))
    parser.add_argument("--tts-model", default=os.environ.get("OLIVER_TTS_MODEL", "tts-1"))
    parser.add_argument(
        "--transcription-model",
        default=os.environ.get("OLIVER_TRANSCRIPTION_MODEL", "whisper-1"),
    )
    parser.add_argument("--voice", default=os.environ.get("OLIVER_VOICE", "alloy"))
    parser.add_argument("--audio-dir", default=os.environ.get("OLIVER_AUDIO_DIR", "audio"))
    parser.add_argument("--listen-timeout", type=float, default=None)
    parser.add_argument("--phrase-time-limit", type=float, default=10)
    return parser.parse_args()


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def create_bot(args):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)

    return OliverRobot(
        api_key,
        model=args.model,
        transcription_model=args.transcription_model,
        tts_model=args.tts_model,
        voice=args.voice,
        audio_dir=args.audio_dir,
    )


def handle_command(bot, category):
    if category == "Empty Trash":
        logging.info("Oliver is starting to empty the trash.")
        return

    if category == "Status":
        logging.info("User requested status update.")
        bot.reply_to_user_by_audio("I am fully operational and ready to assist.")
        return

    logging.info("Command category: %s", category)


def main():
    args = parse_args()
    configure_logging()
    bot = create_bot(args)

    intro = bot.get_gpt_response("Introduce yourself in one short sentence.")
    bot.reply_to_user_by_audio(intro)
    bot.reply_to_user_by_audio(
        "I am Oliver, an office robot. My primary task is to collect and empty trash bins. "
        "Ask me anytime if you need help with your trash."
    )

    logging.info("Oliver is now operational.")
    try:
        while True:
            audio_file = bot.listen_and_save_audio(
                timeout=args.listen_timeout,
                phrase_time_limit=args.phrase_time_limit,
            )
            user_text = bot.get_text_from_audio(audio_file)
            if not user_text:
                continue

            logging.info("User said: %s", user_text)
            if args.wake_word.lower() not in user_text.lower():
                logging.info("Ignored command because wake word '%s' was missing.", args.wake_word)
                continue

            robot_answer = bot.get_gpt_response(user_text)
            bot.reply_to_user_by_audio(robot_answer)
            handle_command(bot, bot.classify_last_user_command())

    except KeyboardInterrupt:
        logging.info("Program terminated by user. Shutting down.")


if __name__ == "__main__":
    main()
