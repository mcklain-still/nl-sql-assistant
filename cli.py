import logging
from chat_engine import process_message
from config import EXIT_COMMANDS
from utils import log_error

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main CLI loop for Shop Bot."""
    print("\n" + "=" * 50)
    print("         🏪 Shop Bot 🏪")
    print("=" * 50)
    print("Ask me anything about the store!")
    print("(Type 'quit' to exit)\n")

    chat_history = []

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in EXIT_COMMANDS:
                print("\nShop Bot: Goodbye, thank you for visiting!\n")
                logger.info("User exited the chat")
                break

            response, success, _ = process_message(user_input, chat_history)
            print(f"\nShop Bot: {response}\n")

        except KeyboardInterrupt:
            print("\n\nShop Bot: Interrupted. Goodbye!\n")
            logger.info("User interrupted the chat")
            break
        except Exception as e:
            log_error("Unexpected error in CLI", e)
            print("\nShop Bot: An unexpected error occurred. Please try again.\n")


if __name__ == "__main__":
    main()