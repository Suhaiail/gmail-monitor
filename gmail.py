from typing import List, Dict

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import (
    SCOPES,
    GMAIL_QUERY,
    MAX_RESULTS
)


class GmailReader:

    def __init__(self):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

        self.service = build(
            "gmail",
            "v1",
            credentials=creds
        )

    def get_recent_messages(
        self,
        max_results: int = MAX_RESULTS
    ) -> List[Dict]:

        try:

            results = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    q=GMAIL_QUERY,
                    maxResults=max_results
                )
                .execute()
            )

            return results.get("messages", [])

        except HttpError as e:

            print(f"Gmail API Error: {e}")
            return []

        except Exception as e:

            print(f"Unexpected Error: {e}")
            return []

    def get_message(
        self,
        message_id: str
    ) -> Dict:

        try:

            return (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="full"
                )
                .execute()
            )

        except HttpError as e:

            print(f"Unable to fetch email {message_id}")
            print(e)

            return {}

        except Exception as e:

            print(e)
            return {}