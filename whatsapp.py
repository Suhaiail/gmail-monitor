import time
import requests

from config import (
    GREEN_API_URL,
    GREEN_API_ID,
    GREEN_API_TOKEN,
    MAX_RETRIES,
    RETRY_DELAYS
)


class WhatsApp:

    def __init__(self):

        self.url = (
            f"{GREEN_API_URL}/waInstance"
            f"{GREEN_API_ID}/sendMessage/"
            f"{GREEN_API_TOKEN}"
        )

    def send(
        self,
        phone: str,
        message: str
    ) -> bool:

        payload = {
            "chatId": f"{phone}@c.us",
            "message": message
        }

        for attempt in range(MAX_RETRIES):

            try:

                response = requests.post(
                    self.url,
                    json=payload,
                    timeout=20
                )

                if response.status_code == 200:

                    print("✅ WhatsApp message sent.")

                    return True

                print(
                    f"Attempt {attempt + 1} failed "
                    f"({response.status_code})"
                )

                print(response.text)

            except requests.exceptions.Timeout:

                print(
                    f"Timeout "
                    f"(Attempt {attempt + 1})"
                )

            except requests.exceptions.ConnectionError:

                print(
                    f"Connection Error "
                    f"(Attempt {attempt + 1})"
                )

            except Exception as e:

                print(
                    f"Unexpected Error: {e}"
                )

            if attempt < MAX_RETRIES - 1:

                wait = RETRY_DELAYS[attempt]

                print(
                    f"Retrying in {wait} seconds..."
                )

                time.sleep(wait)

        print("❌ Failed after all retry attempts.")

        return False


if __name__ == "__main__":

    wa = WhatsApp()

    success = wa.send(
        "919573338048",
        "✅ Gmail Monitor Test"
    )

    print(success)