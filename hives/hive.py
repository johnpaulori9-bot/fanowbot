# hives/hive.py

from agents.principle_memory_agent import PrincipleMemoryAgent

from workflows.principles_briefing_workflow import PrinciplesBriefingWorkflow
from workflows.principle_ingestion_workflow import PrincipleIngestionWorkflow
from workflows.design_review_workflow import DesignReviewWorkflow

class Hive:
    """
    Central registry for agents and workflows.
    """

    def __init__(self, originator):
        self.originator = originator

        self.agents = {
            "PrincipleMemoryAgent": PrincipleMemoryAgent,
        }

        self.workflows = {
            "PrinciplesBriefingWorkflow": PrinciplesBriefingWorkflow,
            "PrincipleIngestionWorkflow": PrincipleIngestionWorkflow,
            "DesignReviewWorkflow": DesignReviewWorkflow,
        }

    def get_agent(self, name):
        agent_class = self.agents.get(name)
        if not agent_class:
            raise ValueError(f"Agent not found: {name}")
        return agent_class()

    def get_workflow(self, name):
        workflow_class = self.workflows.get(name)
        if not workflow_class:
            raise ValueError(f"Workflow not found: {name}")
        return workflow_class()
