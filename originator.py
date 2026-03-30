# originator.py

from hives.hive import Hive

class Originator:
    """
    Central dispatcher for running workflows.
    """

    def __init__(self):
        self.hive = Hive(self)

    def run_workflow(self, workflow_name, **kwargs):
        workflow = self.hive.get_workflow(workflow_name)

        if kwargs:
            return workflow.run(**kwargs)

        return workflow.run()
