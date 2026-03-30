class Agent:
    def __init__(self):
        pass

    def plan(self, goal: str):
        print(f"[PlannerAgent] Planning for goal: {goal}")
        return [
            f"Clarify goal: {goal}",
            "Check relevant context from MemoryAgent",
            "Decide which workflows to run",
            "Execute steps via ActionAgent"
        ]
