from datetime import datetime


class Agent:
    def __init__(self):
        self.jobs = []

    def register_job(self, name: str, schedule: str, workflow_name: str):
        """
        schedule: cron-like string (e.g. '0 7 * * *')
        For now we just store it; real scheduling can be done via cron or a loop.
        """
        self.jobs.append({
            "name": name,
            "schedule": schedule,
            "workflow": workflow_name
        })
        print(f"[SchedulerAgent] Registered job '{name}' for workflow '{workflow_name}' at '{schedule}'.")

    def list_jobs(self):
        return self.jobs

    def run_due(self, originator):
        """
        Placeholder: in a real loop, this would check current time vs schedule.
        For now, it just prints what would be run.
        """
        now = datetime.utcnow().isoformat()
        print(f"[SchedulerAgent] (stub) At {now}, would evaluate and run scheduled jobs.")
        for job in self.jobs:
            print(f" - Would run workflow: {job['workflow']} (job: {job['name']}, schedule: {job['schedule']})")
