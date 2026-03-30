import json
import os
from datetime import datetime


class Agent:
    def __init__(self, path: str = "tasks.json"):
        self.path = path
        self.tasks = []
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    self.tasks = json.load(f)
            except Exception:
                self.tasks = []
        else:
            self.tasks = []

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, title: str, source: str = "manual"):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "source": source,
            "created_at": datetime.utcnow().isoformat(),
            "completed": False,
            "completed_at": None
        }
        self.tasks.append(task)
        self._save()
        print(f"[TaskManagerAgent] Added task: {title}")
        return task

    def list_tasks(self, include_completed=False):
        if include_completed:
            return self.tasks
        return [t for t in self.tasks if not t["completed"]]

    def complete_task(self, task_id: int):
        for t in self.tasks:
            if t["id"] == task_id:
                t["completed"] = True
                t["completed_at"] = datetime.utcnow().isoformat()
                self._save()
                print(f"[TaskManagerAgent] Completed task {task_id}: {t['title']}")
                return t
        print(f"[TaskManagerAgent] Task {task_id} not found.")
        return None
