# agents/telegram_agent.py

class TelegramAgent:
    """
    Handles Telegram messages and triggers workflows.
    Originator is passed in from the outside to avoid circular imports.
    """

    def __init__(self, originator):
        self.originator = originator

    def handle_message(self, text):
        text = text.strip().lower()

        if text == "briefing":
            return self.originator.run_workflow("DailyBriefingWorkflow")

        elif text == "principles":
            return self.originator.run_workflow("PrinciplesBriefingWorkflow")

        elif text.startswith("principle "):
            url = text.replace("principle ", "").strip()
            return self.originator.run_workflow("PrincipleIngestionWorkflow", url=url)

        elif text == "review":
            return self.originator.run_workflow("DesignReviewWorkflow")

        else:
            return (
                "Unknown command.\n"
                "Try:\n"
                "- briefing\n"
                "- principles\n"
                "- principle <url>\n"
                "- review"
            )
