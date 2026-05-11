import logging
from sql_generator import generate_sql
from answer_generator import generate_answer
from db import run_query
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

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in EXIT_COMMANDS:
                print("\nShop Bot: Goodbye, thank you for visiting!\n")
                logger.info("User exited the chat")
                break

            sql, sql_success, sql_error = generate_sql(user_input)
            
            if not sql_success:
                if sql == "INVALID":
                    print(f"\nShop Bot: Sorry, I can only answer questions about the store.\n")
                else:
                    print(f"\nShop Bot: {sql_error}\n")
                continue

            columns, results, db_success, db_error = run_query(sql)
            
            if not db_success:
                print(f"\nShop Bot: Sorry, something went wrong: {db_error}\n")
                continue

            answer, answer_success, answer_error = generate_answer(user_input, columns, results)
            
            if not answer_success:
                print(f"\nShop Bot: {answer_error}\n")
                continue

            print(f"\nShop Bot: {answer}\n")

        except KeyboardInterrupt:
            print("\n\nShop Bot: Interrupted. Goodbye!\n")
            logger.info("User interrupted the chat")
            break
        except Exception as e:
            log_error("Unexpected error in CLI", e)
            print("\nShop Bot: An unexpected error occurred. Please try again.\n")


if __name__ == "__main__":
    main()
