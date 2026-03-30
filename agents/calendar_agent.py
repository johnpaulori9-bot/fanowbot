import os
from datetime import datetime, timedelta

import requests
from ics import Calendar


class Agent:
    def __init__(self):
        # Outlook ICS URL from environment
        self.outlook_ics_url = os.getenv("OUTLOOK_ICS_URL")
        if not self.outlook_ics_url:
            print("[CalendarAgent] OUTLOOK_ICS_URL not set; using stub events.")

    def _fetch_ics(self):
        """Fetch ICS text from Outlook calendar subscription URL."""
        if not self.outlook_ics_url:
            return None
        try:
            resp = requests.get(self.outlook_ics_url, timeout=10)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"[CalendarAgent] Error fetching ICS: {e}")
            return None

    def fetch_today_events(self):
        """
        Returns a list of human-readable events for today.
        If ICS is not configured or fails, returns stub events.
        """
        ics_text = self._fetch_ics()

        # If ICS missing or failed → stub events
        if not ics_text:
            print("[CalendarAgent] Using stub events (no ICS).")
            events = [
                "09:00 - Stubbed standup meeting.",
                "14:00 - Stubbed deep work block."
            ]
        else:
            # Parse ICS
            cal = Calendar(ics_text)
            today = datetime.utcnow().date()
            tomorrow = today + timedelta(days=1)

            events = []
            for event in cal.events:
                if not event.begin:
                    continue
                start = event.begin.datetime
                if not (today <= start.date() < tomorrow):
                    continue
                time_str = start.strftime("%H:%M")
                title = event.name or "(No title)"
                events.append(f"{time_str} - {title}")

            if not events:
                events = ["No events scheduled for today (from Outlook calendar)."]

        # Priority tagging: early (<9) or late (>=17)
        prioritized = []
        for ev in events:
            try:
                time_part = ev.split(":", 1)[0]
                hour = int(time_part)
                if hour < 9 or hour >= 17:
                    prioritized.append(f"[PRIORITY] {ev}")
                else:
                    prioritized.append(ev)
            except Exception:
                prioritized.append(ev)

        return prioritized
