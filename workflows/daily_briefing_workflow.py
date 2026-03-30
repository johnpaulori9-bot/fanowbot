import os
from datetime import datetime


class Workflow:
    def run(self, agents, **kwargs):
        planner = agents.get("PlannerAgent")
        action = agents.get("ActionAgent")
        memory = agents.get("MemoryAgent")
        email_agent = agents.get("EmailAgent")
        calendar_agent = agents.get("CalendarAgent")
        web_agent = agents.get("WebAgent")
        task_manager = agents.get("TaskManagerAgent")

        goal = "Prepare John's daily briefing from email, calendar, web, and tasks."
        steps = planner.plan(goal) if planner else [goal]

        # Email + calendar
        emails = email_agent.fetch_recent_summaries() if email_agent else []
        events = calendar_agent.fetch_today_events() if calendar_agent else []

        # Tasks
        tasks = task_manager.list_tasks() if task_manager else []

        # Pacific weather + news
        weather_info = "Weather: (no WebAgent available)"
        news_info = "News: (no WebAgent available)"

        if web_agent:
            try:
                web_agent.fetch_text("https://www.metservice.com/marine/south-west-pacific")
                weather_info = "Weather: fetched data from MetService South-West Pacific (details not parsed)."
            except Exception as e:
                weather_info = f"Weather: error fetching data ({e})"

            try:
                web_agent.fetch_text("https://www.rnz.co.nz/international/pacific-news")
                news_info = "News: fetched data from RNZ Pacific News (details not parsed)."
            except Exception as e:
                news_info = f"News: error fetching data ({e})"

        if memory:
            memory.remember("last_daily_briefing_goal", goal)

        if action:
            action.execute(steps)

        lines = []
        lines.append("Daily Briefing")
        lines.append(f"Generated at: {datetime.utcnow().isoformat()} UTC")
        lines.append("")
        lines.append("Planned steps:")
        for s in steps:
            lines.append(f"- {s}")
        lines.append("")
        lines.append("Recent Emails:")
        if emails:
            for e in emails:
                lines.append(f"- {e}")
        else:
            lines.append("- (No email data available)")
        lines.append("")
        lines.append("Today's Calendar:")
        if events:
            for ev in events:
                lines.append(f"- {ev}")
        else:
            lines.append("- (No calendar data available)")
        lines.append("")
        lines.append("Tasks:")
        if tasks:
            for t in tasks:
                lines.append(f"- [ ] {t['title']} (source: {t['source']})")
        else:
            lines.append("- (No open tasks)")
        lines.append("")
        lines.append("Web Context:")
        lines.append(f"- {weather_info}")
        lines.append(f"- {news_info}")

        output_path = "/mnt/c/Users/admin/Downloads/daily_briefing.txt"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        print(f"[DailyBriefingWorkflow] Daily briefing written to: {output_path}")
        return output_path
