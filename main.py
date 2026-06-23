import logging
import os
import sys
from OliverRobot import OliverRobot


def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)

    bot = OliverRobot(api_key)
    robot_answer = bot.get_gpt_response("Do a simple introduce yourself.")
    bot.reply_to_user_by_audio(robot_answer)
    bot.reply_to_user_by_audio(
        "I am Oliver, an office robot. My primary task is to collect and empty trash bins. Ask me anytime if you need help with your trash."
    )
    logging.info("Oliver is now operational...")
    try:
        while True:
            audio_file = bot.listen_and_save_audio()
            user_text = bot.get_text_from_audio(audio_file)
            logging.info("User asked: " + user_text)
            if len(user_text) < 2 or "oliver" not in user_text.lower():
                logging.info(
                    "Ignored user command: Ensure the command includes 'Oliver'."
                )
                continue

            robot_answer = bot.get_gpt_response(user_text)
            bot.reply_to_user_by_audio(robot_answer)
            last_command = bot.get_last_user_command()
            logging.info("User command received: %s", last_command)

            if "empty trash" in last_command.lower():
                logging.info("Oliver is starting to empty the trash.")
                # Empty the trash logic
                pass
            elif "status" in last_command.lower():
                logging.info("User requested status update.")
                bot.reply_to_user_by_audio(
                    "I am fully operational and ready to assist."
                )
                # Provide a status update
                pass
            else:
                logging.info("Unrecognized user command.")

    except KeyboardInterrupt:
        logging.info("Program terminated by user. Shutting down.")
        sys.exit(0)


if __name__ == "__main__":
    main()
