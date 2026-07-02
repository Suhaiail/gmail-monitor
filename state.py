import json
import os
from datetime import datetime, timedelta
from typing import Dict

from config import (
    STATE_FILE,
    STATE_RETENTION_DAYS
)


class StateManager:

    def __init__(self):

        os.makedirs("work", exist_ok=True)

        self.default_state = {
            "processed": {},
            "last_run": None,
            "processed_count": 0
        }

        if os.path.exists(STATE_FILE):
            self.load()
        else:
            self.state = self.default_state.copy()
            self.save()

        self.cleanup()

    def load(self):

        try:

            with open(STATE_FILE, "r") as f:
                self.state = json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):

            print("State file missing or corrupted.")

            self.state = self.default_state.copy()

            self.save()

    def save(self):

        with open(STATE_FILE, "w") as f:

            json.dump(
                self.state,
                f,
                indent=4
            )

    def cleanup(self):

        cutoff = (
            datetime.now()
            - timedelta(days=STATE_RETENTION_DAYS)
        )

        processed = self.state.get(
            "processed",
            {}
        )

        cleaned = {}

        for message_id, timestamp in processed.items():

            try:

                ts = datetime.fromisoformat(timestamp)

                if ts >= cutoff:
                    cleaned[message_id] = timestamp

            except Exception:
                continue

        self.state["processed"] = cleaned

        self.save()

    def is_processed(
        self,
        message_id: str
    ) -> bool:

        return (
            message_id
            in self.state["processed"]
        )

    def mark_processed(
        self,
        message_id: str
    ):

        if not self.is_processed(message_id):

            self.state["processed"][message_id] = (
                datetime.now().isoformat()
            )

            self.state["processed_count"] += 1

            self.state["last_run"] = (
                datetime.now().isoformat()
            )

            self.save()

    def clear(self):

        self.state = self.default_state.copy()

        self.save()

    def total_processed(self) -> int:

        return len(
            self.state["processed"]
        )

    def stats(self) -> Dict:

        return {
            "processed": self.total_processed(),
            "processed_count": self.state["processed_count"],
            "last_run": self.state["last_run"]
        }