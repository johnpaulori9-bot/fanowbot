from originator import Originator

originator = Originator()
originator.build_hive_from_template("hives/apex_hive.json", llm=None)

originator.run_workflow(
    "PrincipleIngestionWorkflow",
    agents=originator.agents,
    url="https://www.shoaf.dev"
)
