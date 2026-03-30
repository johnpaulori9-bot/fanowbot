import sys

from originator import Originator


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 task_cli.py \"Task title\"")
        return

    title = " ".join(sys.argv[1:])
    originator = Originator()

    # Build hives so TaskManagerAgent is registered
    for hive_file in ["hives/apex_hive.json"]:
        try:
            originator.build_hive_from_template(hive_file, llm=None)
        except FileNotFoundError:
            continue

    task_manager = originator.agents.get("TaskManagerAgent")
    if not task_manager:
        print("TaskManagerAgent not available.")
        return

    task_manager.add_task(title, source="cli")


if __name__ == "__main__":
    main()
