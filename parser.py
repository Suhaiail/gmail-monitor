import base64
import re
from typing import Dict, List

from bs4 import BeautifulSoup


class EmailParser:

    def decode(self, data: str) -> str:
        """Decode Gmail Base64 body."""

        try:
            return base64.urlsafe_b64decode(
                data.encode()
            ).decode(errors="ignore")

        except Exception:
            return ""


    def extract_body(self, payload: Dict) -> str:
        """
        Extract plain text body.
        Falls back to HTML if plain text is unavailable.
        """

        if "parts" in payload:

            # --------------------
            # Prefer plain text
            # --------------------

            for part in payload["parts"]:

                if part.get("mimeType") == "text/plain":

                    data = part.get(
                        "body",
                        {}
                    ).get("data")

                    if data:
                        return self.decode(data)

            # --------------------
            # HTML fallback
            # --------------------

            for part in payload["parts"]:

                if part.get("mimeType") == "text/html":

                    data = part.get(
                        "body",
                        {}
                    ).get("data")

                    if data:

                        html = self.decode(data)

                        return BeautifulSoup(
                            html,
                            "html.parser"
                        ).get_text(
                            separator="\n",
                            strip=True
                        )

            # --------------------
            # Recursive search
            # --------------------

            for part in payload["parts"]:

                body = self.extract_body(part)

                if body:
                    return body

        else:

            data = payload.get(
                "body",
                {}
            ).get("data")

            if data:

                return self.decode(data)

        return ""


    def extract_attachments(
        self,
        payload: Dict
    ) -> List[str]:

        attachments = []

        def walk(parts):

            for part in parts:

                filename = part.get("filename")

                if filename:
                    attachments.append(filename)

                if "parts" in part:
                    walk(part["parts"])

        if "parts" in payload:
            walk(payload["parts"])

        return attachments


    def extract_links(
        self,
        text: str
    ) -> List[str]:

        urls = re.findall(
            r'https?://[^\s<>"\']+',
            text
        )

        cleaned = []

        for url in urls:

            url = url.rstrip(").,]>")

            cleaned.append(url)

        return cleaned


    def parse(
        self,
        gmail_message: Dict
    ) -> Dict:

        payload = gmail_message["payload"]

        headers = payload["headers"]

        email = {
            "id": gmail_message["id"],
            "subject": "",
            "from": "",
            "date": "",
            "snippet": gmail_message.get(
                "snippet",
                ""
            ),
            "body": "",
            "links": [],
            "attachments": []
        }

        for header in headers:

            name = header["name"]

            value = header["value"]

            if name == "Subject":
                email["subject"] = value

            elif name == "From":
                email["from"] = value

            elif name == "Date":
                email["date"] = value

        email["body"] = self.extract_body(
            payload
        )

        email["attachments"] = (
            self.extract_attachments(
                payload
            )
        )

        email["links"] = self.extract_links(
            email["body"]
        )

        return email