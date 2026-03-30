import time

from originator import Originator


def main():
    originator = Originator()

    # Build hives (same as originator main)
    for hive_file in ["hives/research_hive.json", "hives/policy_hive.json", "hives/apex_hive.json"]:
        try:
            originator.build_hive_from_template(hive_file, llm=None)
        except FileNotFoundError:
            continue

    scheduler = originator.agents.get("SchedulerAgent")
    if not scheduler:
        print("[scheduler_loop] SchedulerAgent not available.")
        return

    # Register a daily briefing job (cron-like string is informational for now)
    scheduler.register_job(
        name="DailyBriefingJob",
        schedule="0 7 * * *",
        workflow_name="DailyBriefingWorkflow"
    )

    print("[scheduler_loop] Starting scheduler loop (stub). Press Ctrl+C to stop.")

    while True:
        # In a real implementation, we'd parse the cron schedule and compare to current time.
        # For now, we just run the briefing every N seconds as a demo.
        scheduler.run_due(originator)
        if "DailyBriefingWorkflow" in originator.workflows:
            originator.run_workflow("DailyBriefingWorkflow", agents=originator.agents)
        else:
            print("[scheduler_loop] DailyBriefingWorkflow not registered.")
        time.sleep(3600)  # run every hour as a placeholder


if __name__ == "__main__":
    main()
