class Workflow:
    def __init__(self):
        self.name = "RouterWorkflow"

    def execute(self, agents):
        if "AdvisorAgent" in agents:
            result = agents["AdvisorAgent"].act("route decision")
            print(f"RouterWorkflow executed: {result}")
