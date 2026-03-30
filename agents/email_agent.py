import os
import imaplib
import email
from email.header import decode_header


class IMAPClient:
    def __init__(self, host, user, password, label):
        self.host = host
        self.user = user
        self.password = password
        self.label = label

    def _connect(self):
        m = imaplib.IMAP4_SSL(self.host)
        m.login(self.user, self.password)
        return m

    def fetch_recent_subjects(self, mailbox="INBOX", limit=5):
        try:
            m = self._connect()
        except Exception as e:
            print(f"[EmailAgent:{self.label}] IMAP connection failed: {e}")
            return []

        subjects = []
        try:
            m.select(mailbox)
            status, data = m.search(None, "ALL")
            if status != "OK":
                return []

            ids = data[0].split()
            ids = ids[-limit:]
            for msg_id in reversed(ids):
                status, msg_data = m.fetch(msg_id, "(RFC822)")
                if status != "OK":
                    continue
                msg = email.message_from_bytes(msg_data[0][1])
                raw_subj = msg.get("Subject", "")
                decoded, enc = decode_header(raw_subj)[0]
                if isinstance(decoded, bytes):
                    try:
                        decoded = decoded.decode(enc or "utf-8", errors="ignore")
                    except Exception:
                        decoded = decoded.decode("utf-8", errors="ignore")
                subjects.append(decoded)
        finally:
            try:
                m.close()
                m.logout()
            except Exception:
                pass

        return subjects


class Agent:
    def __init__(self):
        # Outlook IMAP config (set these in your environment)
        self.outlook_client = None
        outlook_host = os.getenv("OUTLOOK_IMAP_HOST")
        outlook_user = os.getenv("OUTLOOK_IMAP_USER")
        outlook_pass = os.getenv("OUTLOOK_IMAP_PASS")

        if outlook_host and outlook_user and outlook_pass:
            self.outlook_client = IMAPClient(outlook_host, outlook_user, outlook_pass, "Outlook")
        else:
            print("[EmailAgent] Outlook IMAP not configured (using env OUTLOOK_IMAP_HOST/USER/PASS).")

        # Proton IMAP config (set these in your environment)
        self.proton_client = None
        proton_host = os.getenv("PROTON_IMAP_HOST")
        proton_user = os.getenv("PROTON_IMAP_USER")
        proton_pass = os.getenv("PROTON_IMAP_PASS")

        if proton_host and proton_user and proton_pass:
            self.proton_client = IMAPClient(proton_host, proton_user, proton_pass, "Proton")
        else:
            print("[EmailAgent] Proton IMAP not configured (using env PROTON_IMAP_HOST/USER/PASS).")

    def fetch_recent_summaries(self, limit=5):
        """
        Returns a combined list of recent email subjects from Outlook + Proton.
        If IMAP is not configured, falls back to stubbed data.
        """
        summaries = []  # FIX: ensure variable always exists

        # Outlook
        if self.outlook_client:
            outlook_subjects = self.outlook_client.fetch_recent_subjects(limit=limit)
            for subj in outlook_subjects:
                summaries.append(f"[Outlook] {subj}")

        # Proton
        if self.proton_client:
            proton_subjects = self.proton_client.fetch_recent_subjects(limit=limit)
            for subj in proton_subjects:
                summaries.append(f"[Proton] {subj}")

        # Fallback
        if not summaries:
            print("[EmailAgent] No IMAP accounts configured or no messages found; returning stub data.")
            summaries = [
                "Stub: Email 1 about project updates.",
                "Stub: Email 2 about meeting schedule."
            ]

        # Priority tagging
        priority_keywords = ["urgent", "asap", "important", "deadline", "overdue", "chuuk", "pacific"]
        tagged = []
        for subj in summaries:
            lower = subj.lower()
            if any(k in lower for k in priority_keywords):
                tagged.append(f"[PRIORITY] {subj}")
            else:
                tagged.append(subj)

        return tagged
