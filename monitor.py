import time

from gmail import GmailReader
from parser import EmailParser
from classifier import classify
from whatsapp import WhatsApp
from state import StateManager

from config import (
    PHONE_NUMBER,
    IMPORTANT_CATEGORIES,
    MAX_RESULTS
)


def build_message(email, result):

    message = f"""
📬 Gmail Alert

📌 Category:
{result.category.replace("_", " ").title()}

👤 From:
{email['from']}

📖 Subject:
{email['subject']}

📝 Summary:
{result.summary}

⚠ Action Required:
{result.action_required}
""".strip()

    # -------------------------
    # Attachments
    # -------------------------

    if email["attachments"]:

        message += "\n\n📎 Attachments:\n"

        for file in email["attachments"]:

            message += f"• {file}\n"

    # -------------------------
    # Links
    # -------------------------

    if email["links"]:

        message += "\n🔗 Links:\n"

        for link in email["links"][:5]:

            message += f"{link}\n"

    return message


def classify_with_retry(email):

    retries = 3

    for attempt in range(retries):

        try:

            return classify(email)

        except Exception as e:

            if "429" in str(e):

                wait = 35 * (attempt + 1)

                print(
                    f"Gemini rate limit."
                )

                print(
                    f"Waiting {wait} seconds..."
                )

                time.sleep(wait)

            else:

                raise e

    raise Exception(
        "Gemini failed after retries."
    )


def main():

    gmail = GmailReader()

    parser = EmailParser()

    whatsapp = WhatsApp()

    state = StateManager()

    print("=" * 60)

    print("Checking Gmail...")

    print("=" * 60)

    messages = gmail.get_recent_messages()

    if not messages:

        print("No unread emails found.")

        return

    print(
        f"{len(messages)} unread email(s).\n"
    )

    for msg in messages:

        message_id = msg["id"]

        if state.is_processed(message_id):

            print(
                "Already processed:",
                message_id
            )

            continue

        gmail_message = gmail.get_message(
            message_id
        )

        if not gmail_message:

            continue

        email = parser.parse(
            gmail_message
        )

        print("-" * 60)

        print(
            f"Subject : {email['subject']}"
        )

        print(
            f"From    : {email['from']}"
        )

        try:

            result = classify_with_retry(
                email
            )

        except Exception as e:

            print(
                "Classification failed:"
            )

            print(e)

            continue

        print(
            f"Category : {result.category}"
        )

        if result.category in IMPORTANT_CATEGORIES:

            print(
                "Important email."
            )

            success = whatsapp.send(
                PHONE_NUMBER,
                build_message(
                    email,
                    result
                )
            )

            if success:

                print(
                    "WhatsApp sent."
                )

                state.mark_processed(
                    message_id
                )

            else:

                print(
                    "WhatsApp failed."
                )

        else:

            print(
                "Ignored."
            )

            state.mark_processed(
                message_id
            )

    print("\nDone.")

    print(
        state.stats()
    )


if __name__ == "__main__":

    print("Gmail Monitor Started...")
    print("Checking every 2 minutes.\n")

    while True:

        try:
            main()

        except Exception as e:
            print(f"Error: {e}")

        print("\nSleeping for 2 minutes...\n")

        time.sleep(120)